---
name: resync
description: >-
  Synchronizes repository state, ACCC metrics, invariant gates, and hardware PMU benchmark JSON reports after manual or ad hoc code edits.
  Use this skill when resyncing the project after manual edits or before starting an orchestrator workflow.
---

# Deterministic repository resync workflow

Use this workflow after manual IDE edits or ad hoc fixes outside the strategic `architect` loop to bring all JSON telemetry, hardware PMU reports, static analysis logs, and dual compiler builds back into parity.

## Step 1. Recompute bottom up ACCC state and check hard invariant gates

Run the deterministic introspection script to measure exact token footprints, extract `CMakeLists.txt` dependency edges, calculate subagent sizing scores $\Psi(C_i)$, and evaluate hard gates $H_1$ through $H_5$.

```bash
python3 .agents/skills/architect/scripts/sync_manifest.py --check
```

Fix any reported violation in `H1_acyclicity`, `H2_anchor_preservation`, `H3_execution_verification_parity`, `H4_compiler_regime_and_insulation`, or `H5_context_locality` before proceeding.

## Step 2. Re-run dirty hardware PMU benchmarks

Inspect `dirty_benchmarks` in `production_artifacts/manifest.json`. For each listed component, execute its `<name>BENCH_run` target under `Clang_Custom_Release` to regenerate `production_artifacts/profiling/<name>_score_report.json`.

```bash
cmake --build --preset Clang_Custom_Release --target <name>BENCH_run
```

## Step 3. Reconcile static analysis and dual compiler verification

If C++ translation units or headers under `targets/` were modified, verify static analysis and dual compiler debug and release builds.

```bash
cmake --preset Clang_Tidy && cmake --build --preset Clang_Tidy
./production_artifacts/build_all.sh custom debug
./production_artifacts/build_all.sh default release
```

Resolve any safety critical findings in code and update `production_artifacts/clang_tidy_state.md` if situational exceptions changed.

## Step 4. Finalize manifest and commit clean state

Run `sync_manifest.py --check` once more so `dirty_benchmarks` clears and `production_artifacts/manifest.json` reflects the freshly generated `<name>_score_report.json` files. Commit all updated files so `git status --porcelain` is clean for subsequent `architect` or `performance` runs.
