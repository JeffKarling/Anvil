# Manifest and advisory refactor telemetry

The manifest file in [production_artifacts/manifest.json](../../production_artifacts/manifest.json) serves as the authoritative telemetry record for the repository. It captures dependency graph topology, component token footprints, subagent model sizing, verification gates, and autonomous refactoring candidates.

## Core telemetry fields

The top level fields record global health and graph metrics.

**Schema and graph coordinates.** The manifest records `schema_version` alongside total repository token mass `phi`. Each physical component under `targets/` is indexed with its public includes, private dependencies, unit tests, and benchmarks.

**Subagent sizing.** Each component records an architectural sizing score $\Psi(C_i)$ based on Lakosian fan out and token mass. When $\Psi(C_i) < 0.70$, the orchestrator assigns tactical workers to fast model tiers. When $\Psi(C_i) \ge 0.70$, the orchestrator assigns capable model tiers.

**Invariant gates.** The manifest tracks mathematical verification gates $H_1$ through $H_5$.
* Hard gate 1 verifies acyclicity across the physical target dependency graph.
* Hard gate 2 verifies anchor preservation so foundation components remain isolated.
* Hard gate 3 verifies execution and verification parity between pure compute targets and stateful boundary targets.
* Hard gate 4 verifies compiler regime homogeneity and contract insulation.
* Hard gate 5 verifies context locality under the 16384 token ceiling.

**Dirty benchmarks.** Algorithmic components modified during development are flagged in `dirty_benchmarks`. This indicates their hardware performance counter JSON reports must be regenerated before merging.

## Advisory refactor candidates

Anvil automates repository architectural maintenance through deterministic telemetry rather than speculative architectural debates. Hard invariant gates H1 through H5 must pass before any code merges. In contrast, non-blocking optimizations are recorded into the `refactor_candidates` array during manifest synchronization.

Deferring non-critical optimizations prevents scope creep during active feature delivery. Forcing workers to optimize untouched dependencies while implementing an unrelated feature bloats commit blast radius.

Each candidate record includes a unique identifier, component targets, discovery commit, and economic scoring.

### Mathematical evaluation

Candidates are ranked by net gain.

$$\text{NetGain} = \Delta \Phi_{\text{benefit}} - C_{\text{rework}}$$

The benefit score $\Delta \Phi_{\text{benefit}}$ measures target context reduction and graph simplification. The rework cost $C_{\text{rework}}$ measures blast radius across dependent components. When net gain is positive, the refactor delivers architectural improvement that exceeds the cost of editing downstream code.

During active feature work, candidates located in touched subgraphs receive a free rider discount. The supervisor folds those optimizations directly into the ongoing tactical wave at minimal marginal rework cost. Standalone maintenance runs can also resolve candidates across untouched subgraphs when net gain is positive.

### Categories of refactor notes

Refactor notes fall under four distinct categories.

**Topology repartition.** Notes marked `topology_repartition` identify single consumer schemas that introduce unnecessary scaffolding drag, or saturated components approaching token capacity. These candidates guide target consolidation or target splitting.

**Kernel acceleration.** Notes marked `kernel_acceleration` highlight algorithmic bottlenecks where hardware performance counters show significant potential speedup.

**Contract insulation.** Notes marked `contract_insulation` identify public headers pulling in heavy system headers or leaky transitive dependencies.

**Verification sync.** Notes marked `verification_sync` track outstanding static analysis findings, situational linter exceptions, or dirty benchmark baselines.
