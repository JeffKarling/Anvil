# Human prompt cookbook and lifecycle workflows

This guide provides tested prompts and interaction protocols for human engineers directing Google Antigravity. It organizes interactions around four distinct operational phases across the Anvil lifecycle.

## Greenfield project bootstrap workflow

When starting a project from scratch, human engineers focus on boundaries and approved building blocks rather than internal C++ mechanics.

### Curing approved dependencies

Populate [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) with candidate libraries for your domain. Use `QUIET` so uninstalled packages do not block builds. Use `REQUIRED` only when a package must be present.

### Writing high level requirements

Create a specification file such as `requirements.md` in the project root. Describe external system boundaries, streaming data flows, and domain numerical precision. Do not prescribe class names, private headers, or low level C++ signatures.

### Host and git hygiene

Verify that git is clean before initiating orchestration. Uncommitted files cannot be seen by worker subagents running in isolated worktrees.

```bash
python3 .agents/skills/architect/scripts/sync_manifest.py --require-clean-git
```

### Initial architecture prompt

Use this prompt to instruct [`monitor`](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/monitor/agent.json) to partition the DAG, scaffold components, and launch implementation waves.

> "Act as the monitor supervisor. Review requirements in requirements.md and approved dependencies in cmake/dependencies.cmake. Dispatch strategic_worker to partition capabilities into physical targets, author public headers and error catalogs, and configure CMakeLists.txt. Verify the contract anchor with strategic_verifier, commit once invariant gates H1 through H5 pass, and proceed with tactical worker waves."

## Senior developer refactor review workflow

Anvil shifts code review away from line by line diff inspection toward reviewing structured telemetry in [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json). The manifest records `refactor_candidates` under four distinct kinds.

**Topology candidates.** Records marked `topology_repartition` indicate single consumer fan out contractions or high context saturation splits. These tasks require [`strategic_worker`](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/strategic_worker/agent.json).

**Kernel acceleration candidates.** Records marked `kernel_acceleration` highlight PMU bottlenecks where hardware counters indicate further optimization is viable. These tasks require [`tactical_worker`](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_worker/agent.json).

**Contract insulation candidates.** Records marked `contract_insulation` identify public headers pulling in heavy standard headers or uninsulated third party includes. These tasks require [`tactical_worker`](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_worker/agent.json).

**Verification sync candidates.** Records marked `verification_sync` log situational Clang-Tidy or Cppcheck findings. These tasks require [`tactical_worker`](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_worker/agent.json).

### Autonomous triage mode

Use this prompt when delegating senior engineering judgment directly to the monitor. The monitor ranks candidates by `impact_score` and routes work to the right agent.

> "Act as the monitor supervisor. Review production_artifacts/manifest.json and triage refactor candidates using your senior judgment. Prioritize high impact items. Dispatch strategic_worker for topology or contract reorganizations, and dispatch tactical_worker for internal diagnostics, benchmarks, and header cleanups. Ensure each task passes verification before committing."

### Sovereign approval mode

Use this prompt when you have reviewed [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json) manually and changed `user_directive` from `ignored` to `approved` on selected tickets.

> "Act as the monitor supervisor. Review production_artifacts/manifest.json and execute all refactor candidates marked with user_directive approved. Dispatch the designated worker for each approved item, verify through the appropriate verifier, and commit upon pass."

### Single ticket precision mode

Use this prompt to resolve a specific candidate directly.

> "Act as the monitor supervisor. Resolve refactor candidate REF-TOPO-item_proto-item_store from production_artifacts/manifest.json. Dispatch strategic_worker to consolidate the targets, verify with strategic_verifier, and commit once all invariant gates pass."

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
