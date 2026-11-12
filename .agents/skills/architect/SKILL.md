---
name: architect
description: >-
  Decomposes multi-component features or system designs into an acyclic physical component graph optimized for context window locality and parallel subagent execution.
  Use this skill when designing a new system capability, planning multiple components, or orchestrating subagents across the DAG.
---

# Agentic DAG architecture workflow

You must act as the strategic orchestrator for this workflow regardless of which model is active. Gemini 4 Argon is recommended for this role because it assumes orchestration proactively, though the workflow is model agnostic. Translate requirements into a logical capability graph, contract it into physical targets, and orchestrate tactical workers across isolated Antigravity shared Git worktrees to implement the contracted graph.

## Step 1. Verify clean Git state, resync manifest, and translate requirements

Run the bottom up manifest introspection with a strict clean working tree check before reading repository files.

```bash
python3 .agents/skills/architect/scripts/sync_manifest.py --require-clean-git
```

* If `sync_manifest.py --require-clean-git` exits non zero, refuse to start the architecture workflow until all uncommitted files are committed or stashed and the working tree is clean.
* Read `cmake/dependencies.cmake` and `production_artifacts/manifest.json` before proposing any component.
* Inspect `refactor_candidates` in `production_artifacts/manifest.json`. Execute any `topology_repartition` candidate whose `user_directive` is set to `"approved"`, and leave all candidates marked `"ignored"` untouched unless they are directly superseded by the new requirement subgraph.
* Resolve ambiguous input types, output contracts, or failure modes with the user before partitioning the graph.
* Map each atomic operation to six physical coordinates covering execution nature, verification profile, private library bindings from `cmake/dependencies.cmake`, local compiler regime flags, token footprint, and churn volatility.
* Bind approved third party libraries from `cmake/dependencies.cmake` wherever possible so components remain thin private adapters rather than bespoke reimplementations. Treat `QUIET` entries as pre approved candidates that can be installed on demand when selected, and treat `REQUIRED` entries as mandatory libraries explicitly requested by the user.
* Split any mixed operation that combines blocking OS or I/O calls with deterministic in memory compute into separate capability vertices before optimization.

## Step 2. Contract capabilities under hard physical gates

Group capabilities into physical targets under `targets/<name>/` to minimize context waste and blast radius. Balance scaffolding drag against vendor header exposure while enforcing five hard invariant gates.

* **Quotient DAG acyclicity.** The physical target dependency graph must remain strictly acyclic.
* **Anchor preservation.** Never merge distinct foundational anchors such as `journal`, `perf_scope`, or `journal_signal_adapter`. Keep the `app` executable target isolated from library anchors.
* **Execution and verification parity.** Never merge pure deterministic compute capabilities with stateful OS, I/O, or IPC boundary capabilities. Pure compute targets include `<name>BENCH/` while stateful boundary targets pass `--no-bench` when no hot compute path exists.
* **Compiler regime homogeneity.** Capabilities requiring local flag overrides must not be merged with capabilities under standard flags. Isolate targets requiring `-fno-fast-math`, explicit SIMD flags, or private C++23 features as well as Protobuf `SYSTEM ON` targets.
* **Context locality and tactical helpers.** Keep total worker context $W(C_i)$ for a target and its direct public headers within $B_{\max} = 16384$ tokens. Merge single consumer helpers that share the same execution nature, compiler regime, and header footprint into private `<helper>.hpp` and `<helper>.cpp` files inside the parent target. Extract a sibling target `targets/<new_name>/` whenever a capability serves multiple callers, links a distinct high toxicity library, or forces upstream callers to pay a token tax for unused headers.

## Step 3. Execute contract first scaffolding and compute subagent sizing on the anchor commit

Complete all public contracts and persist the updated manifest before delegating private implementations.

1. Run `.agents/skills/feature/scripts/scaffold.py` for each planned component in the DAG.
2. Author the final public interface in `targets/<name>/<name>/<name>.hpp`, the catalog contract in `targets/<name>/<name>.catalog`, and the dependency edges in `targets/<name>/CMakeLists.txt` for every new component.
3. Verify that the stubbed component graph configures and compiles cleanly.
4. Run `python3 .agents/skills/architect/scripts/sync_manifest.py --check` to compute $\Psi(C_i)$ and record each target's `subagent_model` tier (`flash_lite`, `flash`, or `pro`) inside `production_artifacts/manifest.json`.
5. Commit the clean contract anchor so every subagent worktree branched from `HEAD` sees the new public contracts and `production_artifacts/manifest.json`.

## Step 4. Orchestrate tactical workers via Antigravity `invoke_subagent`

Keep the strategic manager context free of private `.cpp` implementations and inner compiler loops.

1. Ensure the `tactical_worker` subagent from `.agents/agents/tactical_worker/agent.json` is registered in the session, calling `define_subagent` with `name: "tactical_worker"` and `enable_write_tools: true` if not yet registered.
2. Dispatch parallel waves of tactical workers using `invoke_subagent` with `TypeName: "tactical_worker"`, `Workspace: "share"`, and `Model` set from `subagent_model` in `production_artifacts/manifest.json` (`flash_lite` for $\Psi(C_i) < 0.30$, `flash` for $0.30 \le \Psi(C_i) < 0.70$, and `pro` for $\Psi(C_i) \ge 0.70$).

```json
{
  "Subagents": [
    {
      "TypeName": "tactical_worker",
      "Role": "Component Implementer",
      "Model": "flash",
      "Workspace": "share",
      "Prompt": "Implement targets/<name>/<name>.cpp against targets/<name>/<name>/<name>.hpp and direct upstream headers. Verify unit tests, sanitizers, and PMU baselines."
    }
  ]
}
```

3. Restrict each tactical worker to reading and editing only its assigned `targets/<name>/` directory plus reading the public `<dep>/<dep>.hpp` headers of its direct dependencies.
4. Verify that each returned worker modifies only permitted files within `targets/<name>/` and passes unit tests and dual compiler debug builds before integrating and committing its changes on the main branch.
5. If a downstream sanitizer or static analysis checkpoint fails on an integrated branch, bisect the commit ledger to identify the first offending commit. Quarantine its descendant subtree, hard reset to the last clean ancestor commit, and seed `<name>TEST` with a regression test reproducing the fault.

## Step 5. Whole graph verification and manifest resync

Once all component implementations merge cleanly, verify the integrated DAG across both compilers and synchronize `production_artifacts/manifest.json`.

```bash
./production_artifacts/build_all.sh custom debug
./production_artifacts/build_all.sh default release
python3 .agents/skills/architect/scripts/sync_manifest.py --check
```

Inspect `production_artifacts/manifest.json` to confirm all five invariant gates $H_1$ through $H_5$ pass and no dirty benchmarks remain.
