---
name: performance
description: >-
  Profiles, benchmarks, and optimizes hot paths in components against hardware PMU baselines.
  Use this skill when optimizing, benchmarking, or profiling a component.
---

# Performance optimization workflow

## Step 1. Verify host PMU permissions and capture baseline

Ensure `/proc/sys/kernel/perf_event_paranoid` is `<= 1` via `sudo sysctl kernel.perf_event_paranoid=1` and CPU governor is set to performance via `powerprofilesctl set performance`.

Measure the starting baseline under an optimized release preset.

```bash
cmake --build --preset Clang_Custom_Release --target <component>BENCH_run
```

## Step 2. Diagnose bottlenecks from hardware counters

Inspect `production_artifacts/profiling/<component>_score_report.md` or run whole application profiling via `cmake --build --preset Clang_Custom_Release --target Perf_stat`, `Perf_record`, and `Perf_report`.
* **High instructions.** Eliminate virtual dispatch, redundant copies, or per iteration bounds checks inside loops by slicing spans before iteration via `span.first(count)`.
* **Low IPC or cache misses.** Pack data into contiguous buffers and access via `std::span`.
* **Branch misses.** Replace inner loop conditionals with branchless arithmetic or lookup tables.

## Step 3. Apply isolated tactical optimizations

Execute optimization trials in isolated Git worktrees while keeping `targets/<component>/<component>.hpp` and existing unit test assertions in `<component>TEST.cpp` unmodified.
* Never delete, weaken, or bypass unit tests or exception firewalls to inflate benchmark scores.
* Prefer linking accelerated routines from `cmake/dependencies.cmake` privately over custom scalar loops.
* When profiling shows a coarse compute bound loop with high IPC over contiguous `std::span` memory, encapsulate the kernel inside an anonymous namespace in `<component>.cpp` and apply multi versioning across the three standard tiers.

```cpp
__attribute__((target_clones("default", "arch=x86-64-v3", "arch=x86-64-v4")))
```

Never apply `target_clones` to tiny inlined helpers or memory bound loops, and never include `arch=x86-64-v2`. Verify IFUNC clone generation under `GNU_Default_Release` using `nm --demangle targets/<component>/CMakeFiles/<component>.dir/<component>.cpp.o`.

## Step 4. Evaluate safety barriers, plateau stalls, and rollback directives

Verify correctness gates first, then evaluate hardware counter progression.

```bash
./production_artifacts/build_all.sh custom debug
cmake --build --preset Clang_Custom_Release --target <component>BENCH_run
```

Apply the strategic acceptance and stopping rules using `production_artifacts/profiling/<component>_score_report.md`.
* Any failure in compilation, unit tests, or static analysis zeroes the candidate score. Runtime sanitizer faults also zero the score and trigger an immediate revert to the clean parent commit.
* `regression_detected` means revert the candidate commit immediately.
* `stop_hardware_saturated` or `stop_diminishing_returns` means commit the winning state and halt optimization on the component.
* If three consecutive tactical trials fail to achieve at least a `1.03x` composite speedup over the parent commit or oscillate between bottlenecks, mark the search branch stalled. Backtrack to the highest scoring clean ancestor and either switch to an orthogonal algorithmic strategy or stop optimizing.
* Run `.agents/skills/audit-sans/SKILL.md` before finalizing any optimization lineage to confirm zero memory, UB, or thread safety poisoning.

