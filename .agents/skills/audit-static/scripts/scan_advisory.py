#!/usr/bin/env python3
"""Advisory scanner runner for Cppcheck and Include-What-You-Use in Anvil.

Runs advisory static analysis against compile_commands.json without mutating
CMake cache variables or rebuilding targets. Persists structured JSON reports
to production_artifacts/ for consumption by sync_manifest.py and verifiers.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from typing import Any


def find_compile_commands(repo_root: pathlib.Path) -> pathlib.Path | None:
    candidates = [
        repo_root / "build" / "Clang_Custom_Debug" / "compile_commands.json",
        repo_root / "build" / "GNU_Custom_Debug" / "compile_commands.json",
        repo_root / "build" / "Clang_Tidy" / "compile_commands.json",
    ]
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def run_cppcheck(
    repo_root: pathlib.Path,
    compile_commands: pathlib.Path,
    target_filter: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    cppcheck_bin = shutil.which("cppcheck")
    if not cppcheck_bin:
        print("Warning: cppcheck binary not found in PATH.", file=sys.stderr)
        return {}

    cmd = [
        cppcheck_bin,
        f"--project={compile_commands}",
        "--enable=style,performance,portability",
        "--inline-suppr",
        "--suppress=missingIncludeSystem",
        "--suppress=unusedStructMember",
        f"--suppress=*:{repo_root}/build/*",
        "--xml",
    ]

    if target_filter:
        cmd.append(f'--file-filter=*targets/{target_filter}/*')

    proc = subprocess.run(
        cmd,
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    # Cppcheck writes XML diagnostics to stderr
    xml_data = proc.stderr
    results_by_target: dict[str, list[dict[str, Any]]] = {}

    try:
        root = ET.fromstring(xml_data)
        errors = root.find("errors")
        if errors is not None:
            for err in errors.findall("error"):
                eid = err.get("id", "unknown")
                severity = err.get("severity", "style")
                msg = err.get("msg", "")
                cwe = err.get("cwe")

                locations = []
                target_name = "global"
                for loc in err.findall("location"):
                    file_path = loc.get("file", "")
                    line_no = loc.get("line", "0")
                    locations.append(f"{file_path}:{line_no}")
                    m = re.search(r"targets/([A-Za-z0-9_]+)/", file_path)
                    if m:
                        target_name = m.group(1)

                if target_name not in results_by_target:
                    results_by_target[target_name] = []

                results_by_target[target_name].append({
                    "id": eid,
                    "severity": severity,
                    "message": msg,
                    "cwe": cwe,
                    "locations": locations,
                })
    except ET.ParseError:
        pass

    return results_by_target


def run_iwyu(
    repo_root: pathlib.Path,
    compile_commands: pathlib.Path,
    target_filter: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    iwyu_tool = shutil.which("iwyu_tool.py") or shutil.which("iwyu_tool")
    if not iwyu_tool:
        print("Warning: iwyu_tool binary not found in PATH.", file=sys.stderr)
        return {}

    mapping_file = repo_root / "production_artifacts" / "iwyu_mappings.imp"
    mapping_arg = f"-Xiwyu --mapping_file={mapping_file}" if mapping_file.is_file() else ""

    build_dir = compile_commands.parent
    cmd = [
        sys.executable,
        iwyu_tool,
        "-p",
        str(build_dir),
    ]

    target_paths: list[str] = []
    targets_dir = repo_root / "targets"
    if target_filter:
        comp_dir = targets_dir / target_filter
        if comp_dir.is_dir():
            target_paths.append(str(comp_dir))
    else:
        for d in sorted(targets_dir.iterdir()):
            if d.is_dir() and (d / "CMakeLists.txt").is_file():
                target_paths.append(str(d))

    if not target_paths:
        return {}

    cmd.extend(target_paths)
    if mapping_arg:
        cmd.extend(["--", mapping_arg])

    proc = subprocess.run(
        cmd,
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    output = proc.stdout + "\n" + proc.stderr
    results_by_target: dict[str, list[dict[str, Any]]] = {}

    current_file = None
    current_suggestions: list[str] = []

    for line in output.splitlines():
        if " should add these lines:" in line or " should remove these lines:" in line:
            m = re.match(r"^(.*?)\s+should\s+(add|remove)\s+these lines:", line)
            if m:
                current_file = m.group(1).strip()
                action = m.group(2)
                continue
        if line.startswith("#include") or line.startswith("@") or line.startswith("class ") or line.startswith("struct "):
            if current_file:
                t_match = re.search(r"targets/([A-Za-z0-9_]+)/", current_file)
                tname = t_match.group(1) if t_match else "global"
                if tname not in results_by_target:
                    results_by_target[tname] = []
                results_by_target[tname].append({
                    "file": current_file,
                    "suggestion": line.strip(),
                })
        elif line.startswith("---") or line.startswith("The full include-list"):
            current_file = None

    return results_by_target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run advisory code scanners (Cppcheck and IWYU) against Anvil targets."
    )
    parser.add_argument(
        "--cppcheck",
        action="store_true",
        help="Run Cppcheck advisory scan against compile_commands.json.",
    )
    parser.add_argument(
        "--iwyu",
        action="store_true",
        help="Run Include-What-You-Use advisory scan against targets.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all advisory scanners.",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Scope scan to a single component directory under targets/<name>/.",
    )
    parser.add_argument(
        "--sync-manifest",
        action="store_true",
        help="Resynchronize production_artifacts/manifest.json after scanning.",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(__file__).resolve().parents[4]
    compile_commands = find_compile_commands(repo_root)

    if not compile_commands:
        print(
            "Error: compile_commands.json not found in build directories. Run cmake --preset Clang_Custom_Debug first.",
            file=sys.stderr,
        )
        return 1

    run_both = args.all or (not args.cppcheck and not args.iwyu)
    artifacts_dir = repo_root / "production_artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    if args.cppcheck or run_both:
        print(f"[Anvil Scanner] Running Cppcheck against {compile_commands.relative_to(repo_root)}...")
        cppcheck_results = run_cppcheck(repo_root, compile_commands, args.target)
        report_file = artifacts_dir / "cppcheck_report.json"
        report_file.write_text(json.dumps(cppcheck_results, indent=2), encoding="utf-8")
        total_findings = sum(len(v) for v in cppcheck_results.values())
        print(f"[Anvil Scanner] Cppcheck completed: {total_findings} finding(s) across {len(cppcheck_results)} target(s).")
        for tname, items in cppcheck_results.items():
            print(f"  * targets/{tname}: {len(items)} suggestion(s)")

    if args.iwyu or run_both:
        print("[Anvil Scanner] Running Include-What-You-Use...")
        iwyu_results = run_iwyu(repo_root, compile_commands, args.target)
        report_file = artifacts_dir / "iwyu_report.json"
        report_file.write_text(json.dumps(iwyu_results, indent=2), encoding="utf-8")
        total_suggestions = sum(len(v) for v in iwyu_results.values())
        print(f"[Anvil Scanner] IWYU completed: {total_suggestions} suggestion(s) across {len(iwyu_results)} target(s).")
        for tname, items in iwyu_results.items():
            print(f"  * targets/{tname}: {len(items)} include recommendation(s)")

    if args.sync_manifest:
        sync_script = repo_root / ".agents" / "skills" / "architect" / "scripts" / "sync_manifest.py"
        subprocess.run([sys.executable, str(sync_script), "--check"], cwd=repo_root)

    return 0


if __name__ == "__main__":
    sys.exit(main())
