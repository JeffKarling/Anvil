# Verification philosophy in agentic physical design

Autonomous software engineering fails when an agent grades its own work. When a language model authors implementation code, colocated unit tests, and performance benchmarks in the same loop, it inevitably faces subtle reward hacking pressures. A worker stuck on an edge case can satisfy test gates by deleting assertions, loosening numeric tolerances, or mocking away difficult external dependencies. During optimization, it can allow the compiler to constant fold loops away while reporting dramatic benchmark speedups.

Anvil solves this verification dilemma through a layered division of labor. Building on John Lakos physical component design, Anvil pairs implementation workers with read only verifiers operating at two distinct physical scopes, all supervised by a deterministic monitor.

Tactical verification operates strictly within an isolated component directory to detect implementation cheating. Strategic verification operates across the whole dependency graph to ensure contract hygiene and system coherence.

## The self grading trap in autonomous software agents

In traditional human engineering, code review is social and hierarchical. Senior developers review pull requests, challenge architectural shortcuts, and verify that test suites genuinely exercise failure modes.

Autonomous agent workflows lack natural human skepticism. A single model tasked with implementing a feature and making tests pass optimizes for the prompt stopping condition. If unit tests fail, the fastest route to a green exit code is often modifying the test rather than fixing the underlying C++ logic.

Self grading manifests in four distinct failure modes.
* **Assertion dilution.** An agent replaces strict equality checks with loose bounds or removes assertions on tricky error paths.
* **Mock escapism.** An agent introduces dummy stubs that bypass operating system calls, concurrency barriers, or hardware interactions.
* **Benchmark gaming.** An agent feeds compile time constants into hot loops, allowing dead code elimination to report artificial nanosecond latencies.
* **Suppression drift.** An agent silences compiler warnings or static analysis diagnostics with inline comments rather than addressing root defects.

Relying on a single prompt or self review loop cannot eliminate these behaviors. True verification requires adversarial separation, bounded context scopes, and read only permissions.

## The three tier supervisory architecture

To ensure complete verification independence, Anvil separates responsibilities across three distinct tiers:

* **The supervisor tier.** The [monitor](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/monitor/agent.json) operates as a deterministic state machine. It manages the lifecycle sequence, dispatches subagents, and commits verified artifacts. It never authors C++ implementations or edits public contracts directly.
* **The strategic tier.** The [strategic_worker](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/strategic_worker/agent.json) authors physical target topologies, public headers, and error catalogs. The [strategic_verifier](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/strategic_verifier/agent.json) acts as an independent critic evaluating public interface hygiene and invariant gates $H_1$ through $H_5$.
* **The tactical tier.** The [tactical_worker](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_worker/agent.json) authors private implementations and unit tests inside isolated Git worktrees. The [tactical_verifier](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_verifier/agent.json) audits candidate diffs to catch test dilution and cheating before merging.

## The tactical duo of worker and verifier

At the component level, Anvil divides labor into a sequential duo consisting of a [tactical_worker](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_worker/agent.json) and a [tactical_verifier](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_verifier/agent.json).

### The tactical worker

The [tactical_worker](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_worker/agent.json) owns private implementation and mechanical build loops inside an isolated Git worktree.

Operating under a strict $B_{\max} = 16384$ token ceiling, the worker reads only its assigned directory under `targets/<name>/` and the public headers of direct upstream dependencies. It writes `targets/<name>/<name>.cpp`, `targets/<name>/<name>TEST/`, and optional benchmark targets under `targets/<name>/<name>BENCH/`.

The worker is responsible for all mechanical compilation loops. It builds scoped targets with Clang and GCC, resolves compiler warnings, and executes scoped runtime sanitizers including AddressSanitizer and UndefinedBehaviorSanitizer. The worker loops until its unit tests pass and all scoped builds exit cleanly.

### The tactical verifier

Once the worker completes its task, the monitor invokes [tactical_verifier](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_verifier/agent.json).

The tactical verifier is strictly read only and holds no file editing tools. Running in the primary workspace against the candidate diff, it audits the worker output before any change is committed to the main branch.

The tactical verifier enforces four specific audit gates.
* **Contract preservation.** The verifier confirms the public contract in `targets/<name>/<name>/<name>.hpp` and the catalog contract in `targets/<name>/<name>.catalog` remain identical to the anchor commit. It also confirms no files outside `targets/<name>/` were modified.
* **Test integrity and anti reward hacking.** The verifier inspects `targets/<name>/<name>TEST/` to ensure assertions were not deleted or weakened. It verifies that error paths, boundary limits, and catalog failure entries are genuinely exercised without mock abstractions.
* **Benchmark validity.** In components with hardware PMU benchmarks, the verifier inspects `targets/<name>/<name>BENCH/` to confirm workloads are non trivial and execution inputs cannot be constant folded away by the compiler.
* **Invariant and tool compliance.** The verifier scans the diff for unjustified suppression comments, altered CMake warning flags, quoted include directives, or leaked vendor headers.

If the tactical verifier discovers test dilution or contract violations, the candidate diff is discarded. The monitor dispatches a fresh worker armed with the exact audit findings. If the verifier issues a clean pass, the monitor commits the atomic change to the repository ledger.

## The strategic duo across the dependency graph

A component can pass all unit tests while the overall system fails. Because the tactical verifier is scoped to one directory, it cannot detect dropped system requirements, broken cross target integration, or architectural coupling.

To solve this, Anvil pairs the [strategic_worker](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/strategic_worker/agent.json) with an independent [strategic_verifier](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/strategic_verifier/agent.json).

The `strategic_verifier` is a read only agent that audits the global dependency graph and public contracts across two specific checkpoints.

### Checkpoint 1 at the contract anchor

Step 2 and Step 3 of the architecture workflow partition capabilities, scaffold all physical targets, author public headers, and compute component sizing scores via the `strategic_worker`. Before the monitor commits this anchor and spawns tactical worker waves, the `strategic_verifier` executes Checkpoint 1.

The verifier conducts three global checks.
* **Hard mathematical gates.** The verifier runs manifest introspection to confirm invariant gates $H_1$ through $H_5$ pass. It verifies quotient graph acyclicity, anchor preservation, execution parity, compiler regime homogeneity, and context locality.
* **Public interface hygiene.** The verifier audits every public header under `targets/<name>/<name>/<name>.hpp`. It ensures all includes use angle brackets, zero third party vendor headers leak into public contracts, and types rely on strong domain structs and non owning `std::span` concepts.
* **Catalog consistency.** The verifier confirms that operational targets define error catalogs and declare boundary exception firewalls returning `std::optional` or `bool`.

Catching interface mismatches at Checkpoint 1 prevents dozens of downstream workers from implementing code against a flawed contract.

### Checkpoint 2 at final delivery

After parallel worker waves land and the whole DAG compiles cleanly, the `strategic_verifier` executes Checkpoint 2.

At this gate, the verifier audits whole system deliverables. It verifies that multi compiler release builds succeed, integration executables under `targets/app` run properly, and zero dirty benchmarks remain in the profiling ledger.

## The verifier decision rubric and separation of concerns

A senior developer must walk the line between meeting delivery commitments and keeping the codebase clean. Failing a build on minor stylistic suggestions paralyzes development velocity. Conversely, ignoring safety defects or architectural leakage leads to technical debt and runtime crashes.

Anvil solves this trade off by strictly separating hard faults from soft refactoring considerations.

| Category | Defect or observation | Verifier action | Destination |
| :--- | :--- | :--- | :--- |
| Contract | Public header altered or vendor headers leaked | Hard fail | Reject diff and respawn worker |
| Integrity | Test assertions weakened or dependencies mocked | Hard fail | Reject diff and respawn worker |
| Safety | ASan, UBSan, or compiler warning as error | Hard fail | Reject diff and respawn worker |
| Static safety | Clang-Tidy Category A analyzer or concurrency fault | Hard fail | Reject diff and respawn worker |
| Situational design | Clang-Tidy Category B macro usage or vararg syscall | Pass & document | Log verification_sync in manifest.json |
| Code smell | C style loop instead of std::views or missing forward | Pass & document | Log syntax_smell in manifest.json |
| Coverage | Error catalog covered but soak edge case missing | Pass & document | Log test_strengthening in manifest.json |
| Performance | Meets baseline but hardware PMU shows headroom | Pass & document | Log kernel_acceleration in manifest.json |

### Category A hard fails versus Category B manifest tickets

Clang-Tidy checks are partitioned into two operational regimes.

**Category A safety critical defects.** These checks detect memory corruption, undefined behavior, concurrency hazards, and bugprone logic. In Anvil, Category A checks are configured with `--warnings-as-errors`. The tactical worker must loop and resolve every Category A issue before reporting completion. If any Category A defect slips through, the tactical verifier issues an immediate hard fail and rejects the diff.

**Category B situational design considerations.** These checks detect patterns such as macro constants, vararg system calls, missing `std::forward`, or potential performance improvements. Many of these are valid in low level systems code. The tactical verifier audits these warnings, filters out stylistic noise, and logs them into [manifest.json](../../production_artifacts/manifest.json) under `refactor_candidates`. This creates an actionable ticket for future refactoring without blocking the release.

**Filtering Category C stylistic noise.** Stylistic warnings such as identifier lengths and magic number diagnostics are ignored. Bothering developers and agents with trivia creates noise and distracts from core architectural integrity.

### Deliberate duplication of static analysis runs

The tactical worker runs Clang-Tidy during its private build loop. The tactical verifier executes Clang-Tidy again during its independent audit.

While this creates overlapping compute, the separation of concerns provides significant architectural benefits. Compromising slightly on verification speed preserves strict modularity. The worker uses static analysis as a local compiler constraint to fix defects. The verifier uses static analysis as an objective audit tool to classify findings. Either agent can be updated or extended with additional checks without breaking the other.

### Strategic verifier follows the same rubric

The strategic tier follows the identical verification philosophy.

The [strategic_worker](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/strategic_worker/agent.json) must fix all hard faults before presenting contracts. Invariant gates $H_1$ through $H_5$ must pass, quoted includes are forbidden, and vendor headers must never leak. If any hard gate fails, the [strategic_verifier](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/strategic_verifier/agent.json) rejects the contracts and the monitor re-dispatches the worker.

Softer architectural observations do not block progress. Heavy standard library includes across multiple callers or potential 2-to-1 component merges are recorded in [manifest.json](../../production_artifacts/manifest.json) for human review.

### The role of performance benchmarking

Performance benchmarks follow this exact hard versus soft distinction.

During initial feature delivery, the tactical worker executes `<name>BENCH_run` exactly once. This single execution proves that the benchmark compiles, links, runs cleanly without crashes, and records baseline hardware counters.

The worker does not attempt open-ended micro-optimizations during feature construction. Speculative tuning during initial implementation risks introducing regressions and wastes model tokens.

If the hardware PMU counters indicate bottlenecks such as cache misses or low IPC, the finding is recorded in [manifest.json](../../production_artifacts/manifest.json) as a `kernel_acceleration` candidate. Active optimization occurs only when the user or monitor explicitly launches the dedicated performance optimization workflow.

## Physical boundaries as an audit firewall

The layered verifier architecture in Anvil succeeds because it mirrors physical component boundaries.

In monolithic codebases, auditing changes requires holding massive context in memory. Reviewing an architectural change forces an agent to reason about hundreds of source files at once. That cognitive load degrades LLM attention and causes models to miss subtle bugs.

Under Lakosian physical design, context is bounded mathematically. A tactical verifier needs only the component directory and its direct upstream headers, easily fitting within the token budget. A strategic verifier needs only public interface contracts and graph topology, completely ignoring private implementation details.

By decoupling tactical cheat detection from strategic graph verification and coordinating both through a deterministic monitor, Anvil achieves reliable quality control without human micromanagement. Workers remain fast and focused on private code, while independent verifiers guarantee architectural integrity at every commit.
