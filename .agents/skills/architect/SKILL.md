---
name: architect
description: >-
  Decomposes multi-component features or system designs into an acyclic physical component graph optimized for context window locality and parallel subagent execution.
  Use this skill when designing a new system capability, planning multiple components, or orchestrating subagents across the DAG.
---

# Agentic DAG architecture workflow

Use this workflow as the strategic manager to translate requirements into a logical capability graph and contract it into physical targets. Orchestrate tactical workers across isolated Git worktrees to implement the contracted graph.

## Step 1. Translate requirements into capability vectors

Read `cmake/dependencies.cmake` and `targets/` before proposing any component.
* Resolve ambiguous input types, output contracts, or failure modes with the user before partitioning the graph.
* Map each atomic operation to six physical coordinates. These coordinates cover execution nature, verification profile, and private library bindings from `cmake/dependencies.cmake`. They also record local compiler regime flags, token footprint, and churn volatility.
* Bind approved third party libraries from `cmake/dependencies.cmake` wherever possible so components remain thin private adapters rather than bespoke reimplementations. Treat `QUIET` entries as pre approved candidates that can be installed on demand when selected, and treat `REQUIRED` entries as mandatory libraries explicitly requested by the user.
* Split any mixed operation that combines blocking OS or I/O calls with deterministic in memory compute into separate capability vertices before optimization.

## Step 2. Contract capabilities under hard physical gates

Group capabilities into physical targets under `targets/<name>/` to minimize context waste and blast radius. Balance scaffolding drag against vendor header exposure while enforcing five hard invariant gates.

* **Quotient DAG acyclicity.** The physical target dependency graph must remain strictly acyclic.
* **Anchor preservation.** Never merge distinct foundational anchors such as `journal`, `perf_scope`, or `journal_signal_adapter`. Keep the `app` executable target isolated from library anchors.
* **Execution and verification parity.** Never merge pure deterministic compute capabilities with stateful OS, I/O, or IPC boundary capabilities. Pure compute targets include `<name>BENCH/` while stateful boundary targets pass `--no-bench` when no hot compute path exists.
* **Compiler regime homogeneity.** Capabilities requiring local flag overrides must not be merged with capabilities under standard flags. Isolate targets requiring `-fno-fast-math`, explicit SIMD flags, or private C++23 features as well as Protobuf `SYSTEM ON` targets.
* **Context locality and tactical helpers.** Keep total worker context for a target and its direct public headers within budget. Merge single consumer helpers that share the same execution nature, compiler regime, and header footprint into private `<helper>.hpp` and `<helper>.cpp` files inside the parent target. Extract a sibling target `targets/<new_name>/` whenever a capability serves multiple callers, links a distinct high toxicity library, or forces upstream callers to pay a token tax for unused headers.

## Step 3. Execute contract first scaffolding on the anchor commit

Complete all public contracts before delegating private implementations.

1. Run `.agents/skills/feature/scripts/scaffold.py` for each planned component in the DAG.
2. Author the final public interface in `targets/<name>/<name>/<name>.hpp`, the catalog contract in `targets/<name>/<name>.catalog`, and the dependency edges in `targets/<name>/CMakeLists.txt` for every new component.
3. Verify that the stubbed component graph configures and compiles cleanly, then record the clean anchor commit.

## Step 4. Orchestrate tactical workers in isolated Git worktrees

Keep the strategic manager context free of private `.cpp` implementations and inner compiler loops.

1. Spawn short lived tactical worker subagents in isolated workspaces or Git worktrees branched from the anchor commit.
2. Restrict each tactical worker to reading and editing only its assigned `targets/<name>/` directory plus reading the public `<dep>/<dep>.hpp` headers of its direct dependencies.
3. Verify that each returned worker commit modifies only permitted files within `targets/<name>/` and passes unit tests and dual compiler debug builds before merging into the integration branch.
4. If a downstream sanitizer or static analysis checkpoint fails on an integrated branch, bisect the commit ledger to identify the first offending commit. Quarantine its descendant subtree, hard reset to the last clean ancestor commit, and seed `<name>TEST` with a regression test reproducing the fault.

## Step 5. Whole graph verification

Once all component implementations merge cleanly, verify the integrated DAG across both compilers and audit the physical topology.

```bash
./production_artifacts/build_all.sh custom debug
./production_artifacts/build_all.sh default release
cmake --build --preset GNU_Custom_Release --target graphviz
```

Inspect `production_artifacts/graphviz/project.dot` to confirm the dependency graph remains wide, shallow, and strictly acyclic.

