# Human prompt cookbook and lifecycle workflows

This guide provides tested prompts and interaction protocols for human engineers directing Google Antigravity. It organizes interactions around four distinct operational phases across the Anvil lifecycle.

## Greenfield project bootstrap workflow

When starting a project from scratch, human engineers focus on boundaries and approved building blocks rather than internal C++ mechanics.

### Curing approved dependencies

Populate [cmake/dependencies.cmake](../../cmake/dependencies.cmake) with candidate libraries for your domain. Use `QUIET` so uninstalled candidate packages do not block builds. Use `REQUIRED` when the package must be present in the host environment.

### Writing high level requirements

Create a specification file such as `requirements.md` in the project root. Describe external system boundaries, streaming data flows, and domain numerical precision. Do not prescribe class names, private headers, or low level C++ signatures.

### Host and git hygiene

Verify that git is clean before initiating orchestration. Uncommitted files cannot be seen by worker subagents running in isolated worktrees.

```bash
python3 .agents/skills/architect/scripts/sync_manifest.py --require-clean-git
```

### Initial architecture prompt

Use this prompt to instruct [`monitor`](../../.agents/agents/monitor/agent.json) to partition the DAG, scaffold components, and launch implementation waves.

> "Act as the monitor supervisor. Review requirements in requirements.md and approved dependencies in cmake/dependencies.cmake. Dispatch strategic_worker to partition capabilities into physical targets, author public headers and error catalogs, and configure CMakeLists.txt. Verify the contract anchor with strategic_verifier, commit once invariant gates H1 through H5 pass, and proceed with tactical worker waves."

## Autonomous refactor telemetry workflow

Anvil shifts architectural maintenance away from line by line diff inspection and manual ticket approval toward continuous telemetry in [manifest.json](../../production_artifacts/manifest.json). The manifest records advisory `refactor_candidates` notes under four distinct kinds alongside their deterministic `benefit_score`, `standalone_rework_cost`, and `net_gain`.

**Topology notes.** Records marked `topology_repartition` indicate single consumer fan out contractions or high context saturation splits. These tasks are evaluated by [`strategic_worker`](../../.agents/agents/strategic_worker/agent.json) against incoming requirements and net gain thresholds.

**Kernel acceleration notes.** Records marked `kernel_acceleration` highlight PMU bottlenecks where hardware counters indicate further optimization is viable. These tasks are handled by [`tactical_worker`](../../.agents/agents/tactical_worker/agent.json).

**Contract insulation notes.** Records marked `contract_insulation` identify public headers pulling in heavy standard headers or uninsulated includes. These tasks are handled by [`strategic_worker`](../../.agents/agents/strategic_worker/agent.json) or [`tactical_worker`](../../.agents/agents/tactical_worker/agent.json).

**Verification sync notes.** Records marked `verification_sync` log situational Clang-Tidy, Cppcheck, or dirty benchmark findings. These tasks are handled by [`tactical_worker`](../../.agents/agents/tactical_worker/agent.json).

### Autonomous net gain triage mode

Use this prompt when asking the monitor to execute positive net gain optimizations across the repository without new feature requirements.

> "Act as the monitor supervisor. Review advisory refactor_candidates telemetry in production_artifacts/manifest.json. Execute candidates with positive net_gain by dispatching strategic_worker for topology or public contract reorganizations and tactical_worker for internal diagnostics, benchmarks, and header cleanups. Verify every change through the appropriate verifier before committing."

### Incremental requirement evolution with telemetry hints

Use this prompt when adding new requirements after Version 1 so the strategic worker folds advisory telemetry notes into the active modification subgraph under the free rider rework discount.

> "Act as the monitor supervisor. Review the updated requirements in requirements.md alongside the advisory refactor_candidates notes in production_artifacts/manifest.json. Dispatch strategic_worker to integrate the new requirements while folding in neighborhood telemetry hints and positive net_gain refactors. Verify with strategic_verifier and proceed with tactical worker waves."

### Single candidate precision mode

Use this prompt when you want to force resolution of a specific telemetry note directly.

> "Act as the monitor supervisor. Resolve advisory candidate REF-TOPO-item_proto-item_store from production_artifacts/manifest.json. Dispatch strategic_worker to consolidate the targets, verify with strategic_verifier, and commit once all invariant gates pass."

### Defect triage and remediation mode

Use this prompt when reporting bug or defect feedback so the strategic worker conducts root cause analysis and establishes testability boundaries before tactical waves begin.

> "Act as the monitor supervisor. I found a defect: <DEFECT_DESCRIPTION>. Dispatch strategic_worker to investigate the root cause, determine required DAG or public contract modifications, and produce a tactical remediation plan with testability boundaries. Verify any contract anchor with strategic_verifier before proceeding with tactical worker waves."

## Performance tuning and hardware PMU workflow

Algorithmic components with `<name>BENCH` suites generate structured hardware counter reports in `production_artifacts/profiling/`.

### Host environment preparation

Unlock Linux kernel hardware performance counters and lock CPU frequencies to ensure repeatable cycles.

```bash
sudo sysctl kernel.perf_event_paranoid=1
powerprofilesctl set performance
```

### Benchmark optimization prompt

Use this prompt to execute benchmark suites and optimize detected bottlenecks.

> "Act as the monitor supervisor. Profile algorithmic targets using their performance benchmarks. Run benchmark presets, inspect production_artifacts/profiling reports, and dispatch tactical_worker to optimize kernels marked with continue_optimizing. Verify with tactical_verifier and confirm speedup ratios."

### Dependency exploration prompt

Use this prompt to ask the orchestrator if external libraries could replace bespoke computation.

> "Analyze component performance telemetry across the project. Are there any additional third party libraries that can accelerate memory bound or compute bound bottlenecks, and which packages should I add to cmake/dependencies.cmake?"

## Ad hoc manual edits and resync workflow

When you edit code manually in an IDE, local telemetry and benchmark reports become dirty.

### Resynchronization prompt

Use this prompt to reconcile project state before handing control back to the monitor.

> "I made manual edits in targets. Act as the monitor supervisor and run the resync skill. Rebuild the components, refresh production_artifacts/manifest.json, run fast invariant gates H1 through H5, and ensure dirty benchmark reports are updated before committing."
