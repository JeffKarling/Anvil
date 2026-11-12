---
name: architect
description: >-
  Supervises the deterministic architecture lifecycle. Dispatches strategic_worker to partition physical targets and author contracts, validates with strategic_verifier, and coordinates tactical_worker and tactical_verifier waves across the DAG.
---

# Agentic DAG architecture workflow

You must act as the monitor for this workflow regardless of which model is active. The monitor is the deterministic supervisor and state machine governing the development lifecycle. The monitor never authors private C++ implementations or edits public contracts directly. Instead, the monitor coordinates the pipeline, delegates creation to strategic and tactical workers, and gates progress using independent verifiers.

## Step 1. Verify clean Git state and clarify requirements

Run the manifest introspection with a clean working tree requirement before starting.

```bash
python3 .agents/skills/architect/scripts/sync_manifest.py --require-clean-git
```

* If the script exits non zero, refuse to proceed until all uncommitted files are committed or stashed.
* Review [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) and [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json) before delegating work.
* Inspect refactor candidates in [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json). Execute any topology repartition candidate marked approved by the user.
* Clarify ambiguous input types, contracts, or failure modes with the user before dispatching the strategic worker.

## Step 2. Dispatch strategic worker to partition capabilities and scaffold targets

Dispatch the strategic worker subagent to group capabilities into physical targets and author public contracts.

```json
{
  "Subagents": [
    {
      "TypeName": "strategic_worker",
      "Role": "Strategic Architect",
      "Model": "pro",
      "Workspace": "inherit",
      "Prompt": "Translate requirements into physical targets under targets/. Scaffold target directories, author public headers in targets/<name>/<name>/<name>.hpp, author error catalogs in targets/<name>/<name>.catalog, configure targets/<name>/CMakeLists.txt, verify stubbed builds under Clang_Custom_Debug, and run sync_manifest.py --check. Report completion back to monitor."
    }
  ]
}
```

The strategic worker enforces five hard invariant gates:
* **Quotient DAG acyclicity.** The physical target dependency graph must remain strictly acyclic.
* **Anchor preservation.** Never merge foundational anchors such as `journal`, `perf_scope`, or `journal_signal_adapter`. Keep the `app` executable target isolated from library anchors.
* **Execution and verification parity.** Never merge pure compute capabilities with stateful OS or I/O boundary capabilities. Pure compute targets must include benchmark suites.
* **Compiler regime homogeneity.** Capabilities requiring custom flags must remain isolated. Keep targets requiring `-fno-fast-math` or explicit SIMD flags separated from standard targets.
* **Context locality and tactical helpers.** Keep total worker context within $B_{\max} = 16384$ tokens. Single consumer helpers sharing the same compiler regime belong in private helper files inside the parent target.

## Step 3. Audit contract anchor with strategic verifier and commit

Once the strategic worker finishes, verify the public contracts before committing the anchor.

1. Dispatch the strategic verifier subagent via `invoke_subagent`.

```json
{
  "Subagents": [
    {
      "TypeName": "strategic_verifier",
      "Role": "Strategic Verifier",
      "Model": "flash",
      "Workspace": "inherit",
      "Prompt": "Audit candidate public contracts and manifest gates. Verify that targets/<name>/<name>/<name>.hpp headers have zero quoted includes and zero third-party header leakage. Verify that python3 .agents/skills/architect/scripts/sync_manifest.py --check passes gates H1 through H5. Report a concise pass or fail verdict."
    }
  ]
}
```

2. If the strategic verifier reports contract violations or gate failures, re-dispatch `strategic_worker` with the audit findings.
3. Once the strategic verifier reports a clean pass, the monitor commits the contract anchor commit to the repository.

## Step 4. Orchestrate tactical workers and verifiers in parallel

Keep the monitor context free of private `.cpp` implementations and mechanical compiler loops.

1. Ensure [tactical_worker](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_worker/agent.json) and [tactical_verifier](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_verifier/agent.json) are registered.
2. Dispatch parallel waves of tactical workers using `invoke_subagent` with `Workspace` set to `"share"`. Set `Model` from `subagent_model` in [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json) using `flash` for $\Psi(C_i) < 0.70$ and `pro` for $\Psi(C_i) \ge 0.70$.

```json
{
  "Subagents": [
    {
      "TypeName": "tactical_worker",
      "Role": "Component Implementer",
      "Model": "flash",
      "Workspace": "share",
      "Prompt": "Implement targets/<name>/<name>.cpp against targets/<name>/<name>/<name>.hpp and direct upstream headers. Verify unit tests, sanitizers, and baseline benchmark."
    }
  ]
}
```

3. Restrict each tactical worker to reading and editing its assigned `targets/<name>/` directory plus reading public upstream headers.
4. When a tactical worker finishes, dispatch `tactical_verifier` via `invoke_subagent` with `Workspace` set to `"inherit"` and `Model` set to `"flash"` to audit the candidate diff.
5. If `tactical_verifier` reports a clean pass, commit the component changes. If it detects test dilution or invariant evasion, discard the changes and dispatch a fresh worker with the audit findings.

## Step 5. Whole graph verification and final release gate

Once all components merge cleanly, verify the integrated system across compilers and synchronize [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json).

```bash
./production_artifacts/build_all.sh custom debug
./production_artifacts/build_all.sh default release
python3 .agents/skills/architect/scripts/sync_manifest.py --check
```

Dispatch `strategic_verifier` via `invoke_subagent` to confirm all five invariant gates $H_1$ through $H_5$ pass and zero dirty benchmarks remain.
