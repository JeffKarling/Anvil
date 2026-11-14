# Human prompt cookbook and workflows

This guide provides tested prompts and interaction protocols for human engineers directing Google Antigravity.

Daily interaction with Anvil centers on standard software engineering directives such as implementing new capabilities, modifying existing behavior, or fixing defects. Beyond standard feature development, Anvil introduces two specialized workflows. The first optimizes physical architecture using advisory telemetry from [manifest.json](../../production_artifacts/manifest.json). The second resynchronizes project telemetry and validation gates after manual code edits.

## Project boundaries and requirements

Human engineers define requirements and external building blocks rather than micromanaging low level C++ mechanics.

### Approved dependencies

Populate [cmake/dependencies.cmake](../../cmake/dependencies.cmake) with candidate libraries for your domain. Use `QUIET` so uninstalled packages do not block builds. Use `REQUIRED` when the package must be present in the host environment. If an approved third party library is missing from the host system, the agent can assist in installing it automatically.

### Writing high level requirements

Create a specification file such as `requirements.md` in the project root. Requirements should stay at a higher level of abstraction than traditional C++ specifications. Frontier models excel at reading domain goals and filling in between the lines. Prescribing class names, private methods, or specific syntax in requirements restricts model reasoning. Focus instead on system capabilities, external boundaries, expected data flows, and precision constraints. The strategic architect will synthesize the physical component decomposition and clean interfaces automatically.

### Clean working tree requirement

The orchestrator requires a clean git status before starting any task. Worker subagents operate in isolated git worktrees and cannot see uncommitted changes. The supervisor inspects git status at startup and will refuse to start if uncommitted files exist. Commit or stash any local modifications before issuing prompts.

## Feature development and defect remediation

Directing the orchestrator to build new capabilities or modify existing components uses the same declarative prompt regardless of project age. Initial bootstrapping and ongoing evolution follow the same lifecycle.

### Implementing requirements

Use this prompt to instruct [`monitor`](../../.agents/agents/monitor/agent.json) to implement domain specifications across the repository.

> "Act as the monitor supervisor. Implement the requirements in requirements.md."

### Remediating defects

Use this prompt when reporting bug or defect feedback so the supervisor conducts root cause analysis and establishes testability boundaries.

> "Act as the monitor supervisor. Remediate this defect: <DEFECT_DESCRIPTION>."

Engineers can also point the supervisor directly to an issue ticket URL in an external tracking system.

> "Act as the monitor supervisor. Remediate the defect described at https://github.com/organization/repository/issues/142."

When provided with update instructions or access tools, the supervisor can post remediation summaries and benchmark diffs back to the tracker upon completion.

> "Act as the monitor supervisor. Remediate the issue at https://github.com/organization/repository/issues/142 and update the ticket with root cause findings and benchmark diffs."

## Autonomous refactor telemetry workflow

When workers implement features, they enforce hard invariant gates H1 through H5 immediately. Secondary opportunities such as situational linter warnings, topology contractions, and hardware PMU headroom are recorded as advisory notes in [manifest.json](../../production_artifacts/manifest.json) rather than executed right away. Deferring secondary optimizations prevents scope creep and keeps feature commit diffs small.

When new requirements touch those components later, the strategic worker folds the refactors in automatically at near zero marginal rework cost. If components remain untouched in quiet subgraphs, human engineers can trigger a dedicated technical debt cleanup pass using the prompts below. A detailed explanation of metrics, gates, and candidate scoring is available in [manifest.md](manifest.md).

### Executing positive net gain refactors

Use this prompt to run a standalone maintenance pass across untouched components without adding new feature requirements.

> "Act as the monitor supervisor. Execute all advisory refactor candidates with positive net gain."

### Incremental requirements with telemetry hints

Use this prompt when adding requirements to an existing codebase so the supervisor folds advisory telemetry into active modification subgraphs under the free rider discount.

> "Act as the monitor supervisor. Implement the updated requirements in requirements.md and fold in relevant refactor telemetry."

### Resolving specific candidates

Use this prompt to force resolution of a single telemetry note directly.

> "Act as the monitor supervisor. Resolve advisory refactor candidate REF-TOPO-item_proto-item_store."

## Performance benchmarking workflow

Algorithmic components generate structured hardware counter reports in `production_artifacts/profiling/`.

### Host environment preparation

Unlock Linux kernel hardware performance counters and lock CPU frequencies to ensure repeatable cycles.

```bash
sudo sysctl kernel.perf_event_paranoid=1
powerprofilesctl set performance
```

### Optimizing performance bottlenecks

Use this prompt to execute benchmark suites and optimize detected bottlenecks.

> "Act as the monitor supervisor. Benchmark algorithmic components and optimize detected bottlenecks."

### Exploring external libraries

Use this prompt to ask the orchestrator if external libraries could replace bespoke computation.

> "Analyze component performance telemetry across the project. Which external libraries could accelerate current memory or compute bottlenecks?"

## Manual edits and resync workflow

When code is edited manually in an IDE, local telemetry and benchmark reports become dirty.

### Resynchronization prompt

Use this prompt to reconcile project state after manual edits before continuing orchestration.

> "I made manual edits in components. Resynchronize the project."
