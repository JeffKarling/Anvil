---
name: audit-static
description: >-
  Runs compile-time static analysis, Clang-Tidy checks, Cppcheck scans, and Include-What-You-Use header hygiene.
  Use this skill when running static analysis, checking code quality, or auditing header includes.
---

# Static analysis and header hygiene workflow

## Step 1. Clang-Tidy analysis

Execute Clang-Tidy under the dedicated analysis preset.

```bash
cmake --preset Clang_Tidy
cmake --build --preset Clang_Tidy
```

Category A defects halt the build automatically. Log intentional Category B situational exceptions in `production_artifacts/clang_tidy_state.md`.

## Step 2. Advisory Cppcheck scan

Run Cppcheck in advisory mode against `compile_commands.json` without modifying CMake cache flags.

```bash
python3 .agents/skills/audit-static/scripts/scan_advisory.py --cppcheck
```

Findings are parsed into structured records in `production_artifacts/cppcheck_report.json` and converted into manifest refactor tickets.

## Step 3. Advisory Include-What-You-Use scan

Run Include-What-You-Use to audit public contract hygiene and forward declaration opportunities.

```bash
python3 .agents/skills/audit-static/scripts/scan_advisory.py --iwyu
grep -rn '#include "' targets/
```

Suggestions are saved to `production_artifacts/iwyu_report.json` and converted into `contract_insulation` refactor candidates. Ensure all target headers use angle brackets.

## Step 4. Manifest synchronization and multi compiler verification

Synchronize [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json) with newly generated scanner candidates and verify dual compiler builds.

```bash
python3 .agents/skills/architect/scripts/sync_manifest.py --check
cmake --build --preset GNU_Custom_Debug
cmake --build --preset Clang_Custom_Debug
```
