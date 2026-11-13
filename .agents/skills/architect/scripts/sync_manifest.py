#!/usr/bin/env python3
"""Deterministic bottom up ACCC manifest generator and invariant verifier for Anvil."""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import subprocess
import sys
from typing import Any

SCHEMA_VERSION = 1
B_MAX_TOKENS = 16384
ANCHOR_TARGETS = {"journal", "perf_scope", "journal_signal_adapter", "app"}
VALID_CANDIDATE_KINDS = {
    "topology_repartition",
    "kernel_acceleration",
    "contract_insulation",
    "verification_sync",
}

DEFAULT_TOXICITY: dict[str, float] = {
    "libsystemd": 0.25,
    "protobuf": 0.85,
    "tbb": 0.65,
    "GTEST": 0.50,
    "zstd": 0.20,
    "sqlite3": 0.25,
    "xxhash": 0.15,
    "OpenSSL": 0.60,
    "liburing": 0.30,
    "curl": 0.45,
    "eigen3": 0.90,
}

HEAVY_STD_HEADERS = {
    "iostream",
    "fstream",
    "sstream",
    "filesystem",
    "regex",
    "map",
    "unordered_map",
    "set",
    "unordered_set",
    "thread",
    "future",
}


def run_git(repo_root: pathlib.Path, args: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout.strip()
    except OSError:
        return 1, ""


def estimate_tokens(path: pathlib.Path) -> int:
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    stripped = re.sub(r"//.*|/\*[\s\S]*?\*/", "", text)
    tokens = re.findall(r"[A-Za-z0-9_]+|[^\sA-Za-z0-9_]", stripped)
    return len(tokens)


def parse_dependencies_cmake(cmake_path: pathlib.Path) -> dict[str, dict[str, Any]]:
    palette: dict[str, dict[str, Any]] = {}
    if not cmake_path.is_file():
        return palette

    content = cmake_path.read_text(encoding="utf-8")
    pending_toxicity: dict[str, float] = dict(DEFAULT_TOXICITY)

    for match in re.finditer(
        r"#\s*@anvil_toxicity:\s*([A-Za-z0-9_+-]+)\s*=\s*([0-9.]+)", content
    ):
        pending_toxicity[match.group(1)] = float(match.group(2))

    for match in re.finditer(
        r"pkg_check_modules\(\s*([A-Za-z0-9_+-]+)\s+([^)]+)\)", content
    ):
        pkg_alias = match.group(1)
        args_str = match.group(2)
        if pkg_alias == "GTEST":
            continue
        required = "REQUIRED" in args_str.split()
        palette[pkg_alias] = {
            "imported_target": f"PkgConfig::{pkg_alias}",
            "required": required,
            "toxicity": round(pending_toxicity.get(pkg_alias, 0.35), 3),
        }

    for match in re.finditer(r"find_package\(\s*([A-Za-z0-9_+-]+)\s*([^)]*)\)", content):
        pkg_name = match.group(1)
        if pkg_name == "PkgConfig":
            continue
        args_str = match.group(2)
        required = "REQUIRED" in args_str.split()
        palette[pkg_name] = {
            "imported_target": pkg_name,
            "required": required,
            "toxicity": round(pending_toxicity.get(pkg_name, 0.40), 3),
        }

    return palette


def parse_target_cmake(
    target_dir: pathlib.Path,
) -> dict[str, Any]:
    name = target_dir.name
    cmake_file = target_dir / "CMakeLists.txt"
    content = cmake_file.read_text(encoding="utf-8") if cmake_file.is_file() else ""

    is_executable = bool(re.search(r"add_executable\(\s*\$\{DIR_NAME\}", content))
    is_system_codegen = bool(re.search(r"SYSTEM\s+ON", content)) and bool(
        re.search(r"\.proto\b", content)
    )

    has_target_props = "include(${CMAKE_BINARY_DIR}/target_properties.cmake)" in content
    has_compile_opts = (
        "include(${CMAKE_BINARY_DIR}/target_compile_options.cmake)" in content
    )
    has_forbidden_pkg_calls = bool(
        re.search(r"\b(find_package|pkg_check_modules)\s*\(", content)
    )

    compiler_regime: list[str] = []
    if re.search(r"cxx_std_23", content):
        compiler_regime.append("cxx_std_23")
    if re.search(r"-fno-fast-math", content):
        compiler_regime.append("-fno-fast-math")
    for simd_flag in ("-mavx2", "-mavx512f", "-mfma", "-msse4.2"):
        if simd_flag in content:
            compiler_regime.append(simd_flag)
    if is_system_codegen:
        compiler_regime.append("SYSTEM_ON_CODEGEN")

    internal_edges: list[dict[str, str]] = []
    vendor_edges: list[dict[str, str]] = []

    for block_match in re.finditer(
        r"target_link_libraries\(\s*\$\{DIR_NAME\}(.*?)\)", content, re.DOTALL
    ):
        block = block_match.group(1)
        block_clean = re.sub(r"#.*", "", block)
        tokens = block_clean.split()
        visibility = "PRIVATE"
        for tok in tokens:
            if tok in ("PUBLIC", "PRIVATE", "INTERFACE"):
                visibility = tok
                continue
            if tok.startswith("${PROJECT_NAME}::"):
                dep_name = tok.split("::", 1)[1].strip()
                internal_edges.append(
                    {"target": dep_name, "linkage": visibility, "target_kind": "component"}
                )
            elif tok.startswith("PkgConfig::"):
                lib_name = tok.split("::", 1)[1].strip()
                vendor_edges.append(
                    {"target": lib_name, "linkage": visibility, "target_kind": "vendor"}
                )
            elif tok.startswith("OpenSSL::"):
                vendor_edges.append(
                    {"target": "OpenSSL", "linkage": visibility, "target_kind": "vendor"}
                )

    has_test = (target_dir / f"{name}TEST" / "CMakeLists.txt").is_file()
    has_bench = (target_dir / f"{name}BENCH" / "CMakeLists.txt").is_file()

    return {
        "target_type": "executable" if is_executable else "static_library",
        "is_system_codegen": is_system_codegen,
        "has_target_properties_include": has_target_props,
        "has_compile_options_include": has_compile_opts,
        "has_forbidden_pkg_calls": has_forbidden_pkg_calls,
        "compiler_regime": sorted(set(compiler_regime)),
        "internal_edges": internal_edges,
        "vendor_edges": vendor_edges,
        "has_test": has_test,
        "has_benchmark": has_bench,
    }


def scan_target_files(
    target_dir: pathlib.Path, is_system_codegen: bool
) -> dict[str, Any]:
    name = target_dir.name
    pub_header = target_dir / name / f"{name}.hpp"
    proto_file = target_dir / name / f"{name}.proto"

    if pub_header.is_file():
        public_tokens = estimate_tokens(pub_header)
        pub_text = pub_header.read_text(encoding="utf-8")
    elif is_system_codegen and proto_file.is_file():
        public_tokens = estimate_tokens(proto_file)
        pub_text = ""
    else:
        public_tokens = 0
        pub_text = ""

    private_tokens = 0
    helper_units: list[str] = []
    quoted_includes: list[str] = []

    for path in sorted(target_dir.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(target_dir).parts
        if any(
            part.endswith("TEST") or part.endswith("BENCH") for part in rel_parts
        ):
            if path.suffix in (".cpp", ".hpp", ".h"):
                text = path.read_text(encoding="utf-8", errors="ignore")
                for line_no, line in enumerate(text.splitlines(), start=1):
                    if re.match(r'^\s*#\s*include\s+"', line):
                        quoted_includes.append(
                            f"{path.relative_to(target_dir)}:{line_no}"
                        )
            continue

        if path.suffix in (".cpp", ".hpp", ".h"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(text.splitlines(), start=1):
                if re.match(r'^\s*#\s*include\s+"', line):
                    quoted_includes.append(f"{path.relative_to(target_dir)}:{line_no}")

            if path == pub_header:
                continue
            private_tokens += estimate_tokens(path)
            if path.name != f"{name}.cpp" and path.suffix == ".cpp":
                helper_units.append(path.stem)

    heavy_pub_includes: list[str] = []
    third_party_pub_includes: list[str] = []
    for match in re.finditer(r"^\s*#\s*include\s*<([^>]+)>", pub_text, re.MULTILINE):
        inc = match.group(1).strip()
        if inc in HEAVY_STD_HEADERS:
            heavy_pub_includes.append(inc)
        if "/" in inc:
            prefix = inc.split("/", 1)[0]
            if prefix in (
                "systemd",
                "google",
                "tbb",
                "oneapi",
                "openssl",
                "curl",
                "Eigen",
                "zstd",
                "sqlite3",
            ):
                third_party_pub_includes.append(inc)

    return {
        "has_public_header": pub_header.is_file() or (is_system_codegen and proto_file.is_file()),
        "public_tokens": public_tokens,
        "private_tokens": private_tokens,
        "helper_units": sorted(helper_units),
        "quoted_includes": quoted_includes,
        "heavy_public_includes": sorted(set(heavy_pub_includes)),
        "third_party_public_includes": sorted(set(third_party_pub_includes)),
    }


def compute_empirical_churn(
    repo_root: pathlib.Path, target_names: list[str]
) -> dict[str, float]:
    default_churn = {name: 0.10 for name in target_names}
    rc, out = run_git(
        repo_root, ["log", "-n", "50", "--pretty=format:COMMIT:%H", "--name-only"]
    )
    if rc != 0 or not out:
        return default_churn

    commits: list[set[str]] = []
    current_targets: set[str] = set()
    in_commit = False

    for line in out.splitlines():
        line = line.strip()
        if line.startswith("COMMIT:"):
            if in_commit:
                commits.append(current_targets)
            current_targets = set()
            in_commit = True
            continue
        if not line:
            continue
        parts = pathlib.Path(line).parts
        if len(parts) >= 2 and parts[0] == "targets" and parts[1] in target_names:
            current_targets.add(parts[1])

    if in_commit:
        commits.append(current_targets)

    # Filter out bulk scaffolding or initial import commits touching > 4 targets
    focused_commits = [c for c in commits if 0 < len(c) <= 4]
    if len(focused_commits) < 3:
        return default_churn

    total = float(len(focused_commits))
    result: dict[str, float] = {}
    for name in target_names:
        touches = sum(1 for c in focused_commits if name in c)
        if touches == 0:
            result[name] = 0.05
        else:
            result[name] = round(min(1.0, max(0.05, touches / total)), 3)
    return result


def classify_execution_nature(
    name: str,
    cmake_info: dict[str, Any],
    file_info: dict[str, Any],
) -> str:
    if cmake_info["target_type"] == "executable":
        return "entrypoint"
    if cmake_info["is_system_codegen"]:
        return "schema_codegen"
    if name in ANCHOR_TARGETS and not cmake_info["has_benchmark"]:
        return "boundary_io"

    # Inspect private sources for OS/IO/syscall/filesystem boundaries vs pure in-memory compute
    target_dir = file_info["target_dir"]
    combined_src = ""
    for cpp in target_dir.glob("*.cpp"):
        combined_src += cpp.read_text(encoding="utf-8", errors="ignore")

    has_io_calls = bool(
        re.search(
            r"\b(syscall|ioctl|sigwait|pthread_sigmask|sd_journal|std::filesystem|std::ifstream|std::ofstream|socket|connect|epoll)\b",
            combined_src,
        )
    )
    if cmake_info["has_benchmark"] and not has_io_calls:
        return "pure_compute"
    if has_io_calls:
        return "boundary_io"
    return "pure_compute" if cmake_info["has_benchmark"] else "boundary_io"


def load_pmu_report(
    repo_root: pathlib.Path, name: str, has_benchmark: bool
) -> tuple[dict[str, Any] | None, bool]:
    if not has_benchmark:
        return None, False

    report_path = (
        repo_root / "production_artifacts" / "profiling" / f"{name}_score_report.json"
    )
    target_dir = repo_root / "targets" / name

    if not report_path.is_file():
        return None, True

    try:
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, True

    report_mtime = report_path.stat().st_mtime
    is_dirty = False
    for src in target_dir.rglob("*"):
        if not src.is_file():
            continue
        if src.suffix in (".cpp", ".hpp", ".proto") or src.name == "CMakeLists.txt":
            if src.stat().st_mtime > report_mtime + 1.0:
                is_dirty = True
                break

    return report_data, is_dirty


def check_acyclicity(
    target_names: list[str], edges: list[dict[str, str]]
) -> tuple[bool, list[str]]:
    adj: dict[str, list[str]] = {n: [] for n in target_names}
    in_degree: dict[str, int] = {n: 0 for n in target_names}
    for edge in edges:
        if edge["target_kind"] != "component":
            continue
        u = edge["source"]
        v = edge["target"]
        if u in adj and v in in_degree:
            adj[u].append(v)
            in_degree[v] += 1

    queue = sorted([n for n, deg in in_degree.items() if deg == 0])
    visited: list[str] = []
    while queue:
        curr = queue.pop(0)
        visited.append(curr)
        for nxt in sorted(adj[curr]):
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    is_dag = len(visited) == len(target_names)
    cycle_nodes = sorted(set(target_names) - set(visited))
    return is_dag, cycle_nodes


def parse_clang_tidy_logged_targets(repo_root: pathlib.Path) -> dict[str, int]:
    state_file = repo_root / "production_artifacts" / "clang_tidy_state.md"
    counts: dict[str, int] = {}
    if not state_file.is_file():
        return counts
    text = state_file.read_text(encoding="utf-8", errors="ignore")
    for match in re.finditer(r"`targets/([A-Za-z0-9_]+)/", text):
        tname = match.group(1)
        counts[tname] = counts.get(tname, 0) + 1
    return counts


def load_cppcheck_report(repo_root: pathlib.Path) -> dict[str, list[dict[str, Any]]]:
    report_file = repo_root / "production_artifacts" / "cppcheck_report.json"
    if not report_file.is_file():
        return {}
    try:
        data = json.loads(report_file.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def load_iwyu_report(repo_root: pathlib.Path) -> dict[str, list[dict[str, Any]]]:
    report_file = repo_root / "production_artifacts" / "iwyu_report.json"
    if not report_file.is_file():
        return {}
    try:
        data = json.loads(report_file.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def build_manifest(repo_root: pathlib.Path) -> dict[str, Any]:
    manifest_path = repo_root / "production_artifacts" / "manifest.json"
    existing_candidates: dict[str, dict[str, Any]] = {}
    if manifest_path.is_file():
        try:
            prev = json.loads(manifest_path.read_text(encoding="utf-8"))
            if isinstance(prev, dict) and prev.get("schema_version") == SCHEMA_VERSION:
                for cand in prev.get("refactor_candidates", []):
                    cid = cand.get("id")
                    if isinstance(cid, str):
                        existing_candidates[cid] = cand
        except (OSError, json.JSONDecodeError):
            pass

    _, head_commit = run_git(repo_root, ["rev-parse", "--short=12", "HEAD"])
    if not head_commit:
        head_commit = "uncommitted"

    _, status_out = run_git(
        repo_root, ["status", "--porcelain", "--untracked-files=normal"]
    )
    # Ignore manifest.json itself when evaluating working_tree_clean during sync
    dirty_lines = [
        line
        for line in status_out.splitlines()
        if line.strip() and not line.strip().endswith("production_artifacts/manifest.json")
    ]
    working_tree_clean = len(dirty_lines) == 0

    palette = parse_dependencies_cmake(repo_root / "cmake" / "dependencies.cmake")
    targets_root = repo_root / "targets"
    target_dirs = sorted(
        [
            d
            for d in targets_root.iterdir()
            if d.is_dir() and (d / "CMakeLists.txt").is_file()
        ],
        key=lambda p: p.name,
    )
    target_names = [d.name for d in target_dirs]
    churn_map = compute_empirical_churn(repo_root, target_names)
    clang_tidy_counts = parse_clang_tidy_logged_targets(repo_root)
    cppcheck_data = load_cppcheck_report(repo_root)
    iwyu_data = load_iwyu_report(repo_root)

    raw_targets: dict[str, dict[str, Any]] = {}
    all_edges: list[dict[str, str]] = []

    for tdir in target_dirs:
        name = tdir.name
        cmake_info = parse_target_cmake(tdir)
        file_info = scan_target_files(tdir, cmake_info["is_system_codegen"])
        file_info["target_dir"] = tdir

        exec_nature = classify_execution_nature(name, cmake_info, file_info)
        for edge in cmake_info["internal_edges"]:
            all_edges.append(
                {
                    "source": name,
                    "target": edge["target"],
                    "linkage": edge["linkage"],
                    "target_kind": "component",
                }
            )
        for edge in cmake_info["vendor_edges"]:
            all_edges.append(
                {
                    "source": name,
                    "target": edge["target"],
                    "linkage": edge["linkage"],
                    "target_kind": "vendor",
                }
            )

        raw_targets[name] = {
            "cmake": cmake_info,
            "files": file_info,
            "execution_nature": exec_nature,
        }

    # Compute consumer fan-out (in-degree in dependency graph)
    consumers_of: dict[str, list[str]] = {n: [] for n in target_names}
    for edge in all_edges:
        if edge["target_kind"] == "component" and edge["target"] in consumers_of:
            consumers_of[edge["target"]].append(edge["source"])

    targets_out: dict[str, dict[str, Any]] = {}
    dirty_benchmarks: list[str] = []

    for name in target_names:
        info = raw_targets[name]
        cmake_info = info["cmake"]
        file_info = info["files"]

        direct_deps = [
            e["target"]
            for e in cmake_info["internal_edges"]
            if e["target"] in raw_targets
        ]
        upstream_pub_tokens = sum(
            raw_targets[dep]["files"]["public_tokens"] for dep in direct_deps
        )
        w_tokens = (
            file_info["private_tokens"]
            + file_info["public_tokens"]
            + upstream_pub_tokens
        )
        context_sat = round(w_tokens / float(B_MAX_TOKENS), 4)

        vendor_libs = [e["target"] for e in cmake_info["vendor_edges"]]
        theta_load = round(
            sum(
                palette.get(lib, {}).get("toxicity", DEFAULT_TOXICITY.get(lib, 0.35))
                for lib in vendor_libs
            ),
            3,
        )

        k_churn = churn_map.get(name, 0.10)
        nu_bench = 1 if cmake_info["has_benchmark"] else 0
        chi_indicator = 1 if len(cmake_info["compiler_regime"]) > 0 else 0

        psi_score = round(
            0.30 * min(1.0, context_sat)
            + 0.30 * k_churn
            + 0.20 * min(1.0, theta_load)
            + 0.10 * nu_bench
            + 0.10 * chi_indicator,
            4,
        )

        if psi_score < 0.70:
            subagent_model = "flash"
        else:
            subagent_model = "pro"

        pmu_report, bench_dirty = load_pmu_report(
            repo_root, name, cmake_info["has_benchmark"]
        )
        if bench_dirty:
            dirty_benchmarks.append(name)

        pmu_summary: dict[str, Any] | None = None
        if pmu_report is not None:
            curr = pmu_report.get("current_metrics", {})
            pmu_summary = {
                "speedup_ratio": pmu_report.get("speedup_ratio", 1.0),
                "bottleneck": pmu_report.get("bottleneck", "unknown"),
                "directive": pmu_report.get("directive", "continue_optimizing"),
                "worth_optimizing": pmu_report.get("worth_optimizing", True),
                "wall_ns_per_op": curr.get("wall_ns_per_op", 0.0),
                "cycles_per_op": curr.get("cycles_per_op", 0.0),
                "instructions_per_op": curr.get("instructions_per_op", 0.0),
                "ipc": curr.get("ipc", 0.0),
                "branch_misses_per_op": curr.get("branch_misses_per_op", 0.0),
                "cache_misses_per_op": curr.get("cache_misses_per_op", 0.0),
                "dirty": bench_dirty,
            }

        targets_out[name] = {
            "target_type": cmake_info["target_type"],
            "is_anchor": name in ANCHOR_TARGETS,
            "execution_nature": info["execution_nature"],
            "has_test": cmake_info["has_test"],
            "has_benchmark": cmake_info["has_benchmark"],
            "compiler_regime": cmake_info["compiler_regime"],
            "direct_dependencies": sorted(direct_deps),
            "consumer_targets": sorted(consumers_of[name]),
            "consumer_fan_out": len(consumers_of[name]),
            "vendor_dependencies": sorted(vendor_libs),
            "helper_units": file_info["helper_units"],
            "public_tokens": file_info["public_tokens"],
            "private_tokens": file_info["private_tokens"],
            "upstream_public_tokens": upstream_pub_tokens,
            "context_window_tokens": w_tokens,
            "context_saturation": context_sat,
            "churn_volatility": k_churn,
            "vendor_toxicity": theta_load,
            "psi_sizing_score": psi_score,
            "subagent_model": subagent_model,
            "rework_cost": 0.0,
            "pmu_metrics": pmu_summary,
        }

    # Compute deterministic tactical rework cost C_rework per target
    for name, tdata in targets_out.items():
        self_rework = (tdata["private_tokens"] * tdata["psi_sizing_score"]) / 1000.0
        downstream_rework = sum(
            (
                targets_out[cons]["private_tokens"]
                * targets_out[cons]["psi_sizing_score"]
                * 0.5
            )
            / 1000.0
            for cons in tdata["consumer_targets"]
            if cons in targets_out
        )
        bench_penalty = (
            1.5
            if tdata["has_benchmark"]
            and tdata["private_tokens"] > 0
            and tdata["pmu_metrics"] is not None
            else 0.0
        )
        tdata["rework_cost"] = round(self_rework + downstream_rework + bench_penalty, 2)

    # Evaluate Hard Invariant Gates H1 - H5
    is_dag, cycle_nodes = check_acyclicity(target_names, all_edges)
    missing_anchors = sorted(ANCHOR_TARGETS - set(target_names))

    h3_violations: list[str] = []
    h4_violations: list[str] = []
    h5_violations: list[str] = []

    for name, tdata in targets_out.items():
        cmake_info = raw_targets[name]["cmake"]
        file_info = raw_targets[name]["files"]

        if tdata["target_type"] == "static_library" and not tdata["has_test"]:
            h3_violations.append(f"{name}: missing {name}TEST unit test suite")
        if tdata["execution_nature"] == "pure_compute" and not tdata["has_benchmark"]:
            h3_violations.append(
                f"{name}: pure_compute target missing {name}BENCH suite"
            )

        if not cmake_info["has_target_properties_include"]:
            h4_violations.append(f"{name}: missing target_properties.cmake include")
        if not cmake_info["has_compile_options_include"]:
            h4_violations.append(f"{name}: missing target_compile_options.cmake include")
        if cmake_info["has_forbidden_pkg_calls"]:
            h4_violations.append(
                f"{name}: forbidden find_package or pkg_check_modules in component CMakeLists.txt"
            )
        if file_info["quoted_includes"]:
            h4_violations.append(
                f"{name}: quoted #include directives found ({', '.join(file_info['quoted_includes'])})"
            )
        if file_info["third_party_public_includes"]:
            h4_violations.append(
                f"{name}: third party headers leaked in public header ({', '.join(file_info['third_party_public_includes'])})"
            )
        for v_edge in cmake_info["vendor_edges"]:
            if v_edge["linkage"] != "PRIVATE" and not cmake_info["is_system_codegen"]:
                h4_violations.append(
                    f"{name}: vendor library {v_edge['target']} linked {v_edge['linkage']} instead of PRIVATE"
                )

        if tdata["context_window_tokens"] > B_MAX_TOKENS:
            h5_violations.append(
                f"{name}: W(C_i)={tdata['context_window_tokens']} exceeds B_max={B_MAX_TOKENS}"
            )

    gates = {
        "H1_acyclicity": {
            "passed": is_dag,
            "cycle_targets": cycle_nodes,
        },
        "H2_anchor_preservation": {
            "passed": len(missing_anchors) == 0,
            "missing_anchors": missing_anchors,
        },
        "H3_execution_verification_parity": {
            "passed": len(h3_violations) == 0,
            "violations": h3_violations,
        },
        "H4_compiler_regime_and_insulation": {
            "passed": len(h4_violations) == 0,
            "violations": h4_violations,
        },
        "H5_context_locality": {
            "passed": len(h5_violations) == 0,
            "violations": h5_violations,
        },
    }
    all_gates_passed = all(g["passed"] for g in gates.values())

    # Compute Partition Objective Score Phi(P)
    c_scaffold = round(len(target_names) * 10.0, 2)
    c_waste = round(
        sum(
            targets_out[n]["public_tokens"] * max(0, targets_out[n]["consumer_fan_out"] - 1) * 0.01
            for n in target_names
        ),
        2,
    )
    c_blast = round(
        sum(
            targets_out[n]["churn_volatility"]
            * targets_out[n]["consumer_fan_out"]
            * 15.0
            for n in target_names
        ),
        2,
    )
    c_insulate = round(
        sum(
            targets_out[n]["vendor_toxicity"]
            * (targets_out[n]["public_tokens"] / 100.0)
            for n in target_names
        ),
        2,
    )
    phi_total = round(c_scaffold + c_waste + c_blast + c_insulate, 2)

    # Detect advisory refactor telemetry notes under the 4 generic enum types
    candidates: list[dict[str, Any]] = []

    def make_candidate(
        cid: str,
        kind: str,
        skill: str,
        cand_targets: list[str],
        impact_score: float,
        benefit_score: float,
        standalone_rework_cost: float,
        summary: str,
        metrics: dict[str, Any],
    ) -> dict[str, Any]:
        assert kind in VALID_CANDIDATE_KINDS
        prev_cand = existing_candidates.get(cid, {})
        discovered = prev_cand.get("discovered_at_commit", head_commit)
        b_score = round(benefit_score, 2)
        r_cost = round(standalone_rework_cost, 2)
        net_gain = round(b_score - r_cost, 2)
        return {
            "id": cid,
            "kind": kind,
            "recommended_skill": skill,
            "targets": cand_targets,
            "impact_score": round(impact_score, 3),
            "benefit_score": b_score,
            "standalone_rework_cost": r_cost,
            "net_gain": net_gain,
            "summary": summary,
            "metrics": metrics,
            "discovered_at_commit": discovered,
        }

    # 1. topology_repartition (2->1 contractions and 1->2 splits)
    for name, tdata in targets_out.items():
        if tdata["is_anchor"] or tdata["target_type"] != "static_library":
            continue
        if tdata["consumer_fan_out"] == 1:
            consumer = tdata["consumer_targets"][0]
            cons_data = targets_out[consumer]
            if cons_data["is_anchor"] and consumer != "app":
                continue
            merged_w = (
                cons_data["context_window_tokens"]
                + tdata["private_tokens"]
            )
            if merged_w <= B_MAX_TOKENS:
                delta_phi = round(10.0 - (tdata["vendor_toxicity"] * 0.5), 2)
                if delta_phi > 0:
                    cid = f"REF-TOPO-{name}-{consumer}"
                    rework = round(tdata["rework_cost"] + cons_data["rework_cost"], 2)
                    candidates.append(
                        make_candidate(
                            cid=cid,
                            kind="topology_repartition",
                            skill="architect",
                            cand_targets=[name, consumer],
                            impact_score=min(1.0, delta_phi / 12.0),
                            benefit_score=delta_phi,
                            standalone_rework_cost=rework,
                            summary=(
                                f"2-to-1 contraction candidate: {name} has consumer_fan_out=1 into {consumer}. "
                                f"Consolidating {name} into {consumer} eliminates scaffolding drag with delta_phi={delta_phi}."
                            ),
                            metrics={
                                "from_count": 2,
                                "to_count": 1,
                                "delta_phi": delta_phi,
                                "merged_context_tokens": merged_w,
                            },
                        )
                    )

        if (
            tdata["context_saturation"] > 0.65
            or (len(tdata["helper_units"]) >= 2 and tdata["consumer_fan_out"] >= 2)
        ) and not tdata["is_anchor"]:
            cid = f"REF-TOPO-SPLIT-{name}"
            split_benefit = round(tdata["context_saturation"] * 12.0, 2)
            candidates.append(
                make_candidate(
                    cid=cid,
                    kind="topology_repartition",
                    skill="architect",
                    cand_targets=[name],
                    impact_score=tdata["context_saturation"],
                    benefit_score=split_benefit,
                    standalone_rework_cost=tdata["rework_cost"],
                    summary=(
                        f"1-to-2 split candidate: {name} has context_saturation={tdata['context_saturation']} "
                        f"across {tdata['consumer_fan_out']} consumers."
                    ),
                    metrics={
                        "from_count": 1,
                        "to_count": 2,
                        "context_saturation": tdata["context_saturation"],
                        "helper_unit_count": len(tdata["helper_units"]),
                    },
                )
            )

    # 2. kernel_acceleration (PMU continue_optimizing or unlinked palette libraries)
    for name, tdata in targets_out.items():
        pmu = tdata["pmu_metrics"]
        if pmu is not None and pmu.get("directive") == "continue_optimizing":
            cid = f"REF-ACCEL-PMU-{name}"
            imp = round(min(1.0, 0.50 + 0.10 * (1.0 / max(0.5, pmu["speedup_ratio"]))), 3)
            local_rework = round((tdata["private_tokens"] * tdata["psi_sizing_score"]) / 1000.0, 2)
            candidates.append(
                make_candidate(
                    cid=cid,
                    kind="kernel_acceleration",
                    skill="performance",
                    cand_targets=[name],
                    impact_score=imp,
                    benefit_score=round(imp * 6.0, 2),
                    standalone_rework_cost=local_rework,
                    summary=(
                        f"Hardware PMU report for {name} indicates directive=continue_optimizing "
                        f"with bottleneck={pmu['bottleneck']} and speedup={pmu['speedup_ratio']}x."
                    ),
                    metrics={
                        "bottleneck": pmu["bottleneck"],
                        "speedup_ratio": pmu["speedup_ratio"],
                        "wall_ns_per_op": pmu["wall_ns_per_op"],
                        "ipc": pmu["ipc"],
                        "cache_misses_per_op": pmu["cache_misses_per_op"],
                    },
                )
            )

    # 3. contract_insulation (heavy public headers or high public-to-private token ratio)
    for name, tdata in targets_out.items():
        file_info = raw_targets[name]["files"]
        if file_info["heavy_public_includes"] and tdata["consumer_fan_out"] > 0:
            cid = f"REF-INSULATE-HDR-{name}"
            candidates.append(
                make_candidate(
                    cid=cid,
                    kind="contract_insulation",
                    skill="feature",
                    cand_targets=[name],
                    impact_score=0.45,
                    benefit_score=round(0.45 * 10.0, 2),
                    standalone_rework_cost=tdata["rework_cost"],
                    summary=(
                        f"Public header {name}.hpp includes heavy standard headers "
                        f"({', '.join(file_info['heavy_public_includes'])}) across {tdata['consumer_fan_out']} downstream callers."
                    ),
                    metrics={
                        "heavy_headers": file_info["heavy_public_includes"],
                        "public_tokens": tdata["public_tokens"],
                        "consumer_fan_out": tdata["consumer_fan_out"],
                    },
                )
            )

    # 4. verification_sync (dirty benchmarks or logged clang-tidy exceptions)
    for name in dirty_benchmarks:
        cid = f"REF-SYNC-BENCH-{name}"
        candidates.append(
            make_candidate(
                cid=cid,
                kind="verification_sync",
                skill="resync",
                cand_targets=[name],
                impact_score=0.75,
                benefit_score=3.75,
                standalone_rework_cost=0.0,
                summary=(
                    f"Benchmark report production_artifacts/profiling/{name}_score_report.json "
                    f"is missing or older than modified source files in targets/{name}/."
                ),
                metrics={"dirty_benchmark": True},
            )
        )

    for name, warn_count in sorted(clang_tidy_counts.items()):
        if name in targets_out:
            tdata = targets_out[name]
            cid = f"REF-SYNC-TIDY-{name}"
            imp = round(min(1.0, 0.25 * warn_count), 3)
            local_rework = round((tdata["private_tokens"] * tdata["psi_sizing_score"]) / 1000.0, 2)
            candidates.append(
                make_candidate(
                    cid=cid,
                    kind="verification_sync",
                    skill="audit-static",
                    cand_targets=[name],
                    impact_score=imp,
                    benefit_score=round(imp * 5.0, 2),
                    standalone_rework_cost=local_rework,
                    summary=(
                        f"Component {name} has {warn_count} situational static analysis warning(s) "
                        f"logged in production_artifacts/clang_tidy_state.md."
                    ),
                    metrics={"logged_warning_count": warn_count},
                )
            )

    for name, findings in sorted(cppcheck_data.items()):
        if name in targets_out and findings:
            tdata = targets_out[name]
            cid = f"REF-CPPCHECK-{name}"
            imp = round(min(1.0, 0.20 * len(findings)), 3)
            local_rework = round((tdata["private_tokens"] * tdata["psi_sizing_score"]) / 1000.0, 2)
            candidates.append(
                make_candidate(
                    cid=cid,
                    kind="verification_sync",
                    skill="audit-static",
                    cand_targets=[name],
                    impact_score=imp,
                    benefit_score=round(imp * 5.0, 2),
                    standalone_rework_cost=local_rework,
                    summary=(
                        f"Cppcheck advisory scan identified {len(findings)} design suggestion(s) "
                        f"in targets/{name}/."
                    ),
                    metrics={"cppcheck_findings": len(findings)},
                )
            )

    for name, suggestions in sorted(iwyu_data.items()):
        if name in targets_out and suggestions:
            tdata = targets_out[name]
            cid = f"REF-IWYU-{name}"
            imp = round(min(1.0, 0.15 * len(suggestions)), 3)
            local_rework = round((tdata["private_tokens"] * tdata["psi_sizing_score"]) / 1000.0, 2)
            candidates.append(
                make_candidate(
                    cid=cid,
                    kind="contract_insulation",
                    skill="audit-static",
                    cand_targets=[name],
                    impact_score=imp,
                    benefit_score=round(imp * 5.0, 2),
                    standalone_rework_cost=local_rework,
                    summary=(
                        f"Include-What-You-Use identified {len(suggestions)} header recommendation(s) "
                        f"in targets/{name}/."
                    ),
                    metrics={"iwyu_suggestions": len(suggestions)},
                )
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "dirty_benchmarks": sorted(dirty_benchmarks),
        "all_gates_passed": all_gates_passed,
        "invariant_gates": gates,
        "partition_friction": {
            "phi_total": phi_total,
            "c_scaffold": c_scaffold,
            "c_waste": c_waste,
            "c_blast": c_blast,
            "c_insulate": c_insulate,
        },
        "approved_palette": palette,
        "targets": targets_out,
        "edges": all_edges,
        "refactor_candidates": candidates,
    }


def install_git_hook(repo_root: pathlib.Path) -> int:
    hooks_dir = repo_root / ".git" / "hooks"
    if not hooks_dir.is_dir():
        print("Error: .git/hooks directory not found.", file=sys.stderr)
        return 1
    hook_path = hooks_dir / "pre-commit"
    hook_content = """#!/usr/bin/env bash
set -e
python3 .agents/skills/architect/scripts/sync_manifest.py --check
git add production_artifacts/manifest.json
"""
    hook_path.write_text(hook_content, encoding="utf-8")
    hook_path.chmod(0o755)
    print(f"Installed Git pre-commit hook at {hook_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize production_artifacts/manifest.json and verify Anvil ACCC invariants."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if any hard invariant gate H1 through H5 fails.",
    )
    parser.add_argument(
        "--require-clean-git",
        action="store_true",
        help="Refuse to proceed and exit non-zero if git status has uncommitted changes.",
    )
    parser.add_argument(
        "--install-git-hook",
        action="store_true",
        help="Install the Git pre-commit hook that runs sync_manifest.py --check.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress standard status output.",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(__file__).resolve().parents[4]
    manifest_path = repo_root / "production_artifacts" / "manifest.json"

    if args.install_git_hook:
        return install_git_hook(repo_root)

    manifest = build_manifest(repo_root)

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    _, status_out = run_git(
        repo_root, ["status", "--porcelain", "--untracked-files=normal"]
    )
    dirty_lines = [line for line in status_out.splitlines() if line.strip()]
    working_tree_clean = len(dirty_lines) == 0

    if not args.quiet:
        print(
            f"[Anvil sync_manifest] schema_version={manifest['schema_version']} "
            f"targets={len(manifest['targets'])} "
            f"phi={manifest['partition_friction']['phi_total']} "
            f"gates_passed={manifest['all_gates_passed']} "
            f"dirty_benchmarks={len(manifest['dirty_benchmarks'])} "
            f"refactor_candidates={len(manifest['refactor_candidates'])} "
            f"git_clean={working_tree_clean}"
        )

    if args.require_clean_git and not working_tree_clean:
        print(
            "Error: Git working tree is not clean. Commit or stash changes before starting orchestration:",
            file=sys.stderr,
        )
        for line in dirty_lines:
            print(f"  {line}", file=sys.stderr)
        return 2

    if args.check and not manifest["all_gates_passed"]:
        print("Error: Hard invariant gate verification failed:", file=sys.stderr)
        for gate_name, gate_res in manifest["invariant_gates"].items():
            if not gate_res["passed"]:
                print(f"  {gate_name}: {gate_res}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
