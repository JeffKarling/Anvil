#!/usr/bin/env python3
"""Antigravity PostToolUse lifecycle hook handler for Anvil manifest resyncing."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys


def main() -> int:
    try:
        _ = sys.stdin.read()
    except OSError:
        pass

    repo_root = pathlib.Path(__file__).resolve().parents[2]
    sync_script = (
        repo_root / ".agents" / "skills" / "architect" / "scripts" / "sync_manifest.py"
    )
    if sync_script.is_file():
        subprocess.run(
            [sys.executable, str(sync_script), "--quiet"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )

    sys.stdout.write("{}\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
