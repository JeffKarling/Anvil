# Verification philosophy in agentic physical design

Autonomous software engineering fails when an agent grades its own work. When a language model authors implementation code and test suites in the same loop, it inevitably faces subtle reward hacking incentives. A worker stuck on an edge case can satisfy test gates by deleting assertions or loosening tolerances. It can also mock away difficult dependencies.

Anvil solves this verification dilemma through physical division of labor. Building on John Lakos physical component design, Anvil pairs implementation workers with read only verifiers operating at tactical and strategic scopes.

## The tactical duo of worker and verifier

At the component level, Anvil divides labor into a sequential duo consisting of a [tactical_worker](../../.agents/agents/tactical_worker/agent.json) and a [tactical_verifier](../../.agents/agents/tactical_verifier/agent.json).

The tactical worker owns private implementation inside an isolated Git worktree. Operating under a strict $B_{\max} = 16384$ token ceiling, the worker reads only its assigned component directory and the public headers of direct upstream dependencies. It loops until its unit tests pass and all scoped builds exit cleanly.

Once the worker completes its task, the monitor invokes the tactical verifier. The tactical verifier holds strictly read only tools and audits the candidate diff before any merge occurs.

* **Contract preservation.** The verifier confirms public contracts and error catalogs remain identical to the anchor commit. It verifies that no files outside the component directory were modified.
* **Test integrity.** The verifier inspects unit tests to ensure assertions were not deleted or weakened. It confirms that error paths and boundary limits are tested without dummy mocks.
* **Benchmark validity.** In components with hardware PMU benchmarks, the verifier confirms workloads are non trivial and execution inputs cannot be constant folded away.
* **Tool compliance.** The verifier scans the diff for unjustified suppression comments or leaked vendor headers.

If the verifier detects test dilution or contract tampering, the candidate diff is discarded. The monitor dispatches a fresh worker armed with the audit findings.

## The strategic duo across the dependency graph

A component can pass all unit tests while the overall system fails. The tactical verifier is scoped to one directory, so it cannot detect dropped system requirements or architectural coupling.

Anvil pairs the [strategic_worker](../../.agents/agents/strategic_worker/agent.json) with an independent [strategic_verifier](../../.agents/agents/strategic_verifier/agent.json) to audit the global dependency graph across two checkpoints.

* **Checkpoint 1 at the contract anchor.** The strategic worker partitions capabilities and scaffolds component contracts. Before the monitor commits this anchor, the strategic verifier validates invariant gates $H_1$ through $H_5$. It confirms acyclicity and anchor preservation. It also checks execution parity and compiler homogeneity. It verifies context token ceilings and confirms zero vendor leakage in public headers.
* **Checkpoint 2 at final delivery.** After parallel tactical waves land, the strategic verifier audits whole system deliverables. It verifies that multi compiler release builds succeed. It confirms integration executables run properly and zero unverified benchmarks remain.

## The verifier decision rubric

Anvil separates hard defects from soft refactoring telemetry.

* **Hard fails.** Public header tampering and test dilution cause an immediate hard fail. Sanitizer errors and Clang-Tidy Category A findings also reject the diff immediately. The monitor respawns the worker.
* **Advisory telemetry.** Clang-Tidy Category B patterns and heavy standard library includes are logged into [manifest.json](../../production_artifacts/manifest.json) under `refactor_candidates`. These notes record net gain metrics for future waves without blocking current delivery.

By decoupling tactical cheat detection from strategic graph verification, Anvil achieves reliable quality control without human micromanagement.
