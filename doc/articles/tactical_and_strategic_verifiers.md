# Verification philosophy in agentic physical design

Autonomous software engineering fails when an agent grades its own work. When a language model authors implementation code, colocated unit tests, and performance benchmarks in the same loop, it inevitably faces subtle reward hacking pressures. A worker stuck on an edge case can satisfy test gates by deleting assertions, loosening numeric tolerances, or mocking away difficult external dependencies. During optimization, it can allow the compiler to constant fold loops away while reporting dramatic benchmark speedups.

Anvil solves this verification dilemma through a layered division of labor. Building on John Lakos physical component design, Anvil pairs implementation workers with read only verifiers operating at two distinct physical scopes.

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

## The tactical duo of worker and verifier

At the component level, Anvil divides labor into a sequential duo consisting of a `tactical_worker` and a `tactical_verifier`.

### The tactical worker

The `tactical_worker` owns private implementation and mechanical build loops inside an isolated Git worktree.

Operating under a strict $B_{\max} = 16384$ token ceiling, the worker reads only its assigned directory under `targets/<name>/` and the public headers of direct upstream dependencies. It writes `targets/<name>/<name>.cpp`, `targets/<name>/<name>TEST/`, and optional benchmark targets under `targets/<name>/<name>BENCH/`.

The worker is responsible for all mechanical compilation loops. It builds scoped targets with Clang and GCC, resolves compiler warnings, and executes scoped runtime sanitizers including AddressSanitizer and UndefinedBehaviorSanitizer. The worker loops until its unit tests pass and all scoped builds exit cleanly.

### The tactical verifier

Once the worker completes its task, the orchestrator invokes `tactical_verifier`.

The tactical verifier is strictly read only and holds no file editing tools. Running in the primary workspace against the candidate diff, it audits the worker output before any change is committed to the main branch.

The tactical verifier enforces four specific audit gates.
* **Contract preservation.** The verifier confirms the public contract in `targets/<name>/<name>/<name>.hpp` and the catalog contract in `targets/<name>/<name>.catalog` remain identical to the anchor commit. It also confirms no files outside `targets/<name>/` were modified.
* **Test integrity and anti reward hacking.** The verifier inspects `targets/<name>/<name>TEST/` to ensure assertions were not deleted or weakened. It verifies that error paths, boundary limits, and catalog failure entries are genuinely exercised without mock abstractions.
* **Benchmark validity.** In components with hardware PMU benchmarks, the verifier inspects `targets/<name>/<name>BENCH/` to confirm workloads are non trivial and execution inputs cannot be constant folded away by the compiler.
* **Invariant and tool compliance.** The verifier scans the diff for unjustified suppression comments, altered CMake warning flags, quoted include directives, or leaked vendor headers.

If the tactical verifier discovers test dilution or contract violations, the candidate diff is discarded. The orchestrator dispatches a fresh worker armed with the exact audit findings. If the verifier issues a clean pass, the orchestrator commits the atomic change to the repository ledger.

## The strategic verifier across the dependency graph

A component can pass all unit tests while the overall system fails. Because the tactical verifier is scoped to one directory, it cannot detect dropped system requirements, broken cross target integration, or architectural coupling.

The strategic orchestrator acts as a strategic worker during graph design and public contract scaffolding. To avoid strategic self grading, Anvil introduces the `strategic_verifier`.

The `strategic_verifier` is a read only agent that audits the global dependency graph and public contracts across two specific checkpoints.

### Checkpoint 1 at the contract anchor

Step 3 of the architecture workflow scaffolds all physical targets, authors public headers, and computes component sizing scores. Before the orchestrator commits this anchor and spawns worker waves, the `strategic_verifier` executes Checkpoint 1.

The verifier conducts three global checks.
* **Hard mathematical gates.** The verifier runs manifest introspection to confirm invariant gates $H_1$ through $H_5$ pass. It verifies quotient graph acyclicity, anchor preservation, execution parity, compiler regime homogeneity, and context locality.
* **Public interface hygiene.** The verifier audits every public header under `targets/<name>/<name>/<name>.hpp`. It ensures all includes use angle brackets, zero third party vendor headers leak into public contracts, and types rely on strong domain structs and non owning `std::span` concepts.
* **Catalog consistency.** The verifier confirms that operational targets define error catalogs and declare boundary exception firewalls returning `std::optional` or `bool`.

Catching interface mismatches at Checkpoint 1 prevents dozens of downstream workers from implementing code against a flawed contract.

### Checkpoint 2 at final delivery

After parallel worker waves land and the whole DAG compiles cleanly, the `strategic_verifier` executes Checkpoint 2.

At this gate, the verifier audits whole system deliverables. It verifies that multi compiler release builds succeed, integration executables under `targets/app` run properly, and zero dirty benchmarks remain in the profiling ledger.

## Physical boundaries as an audit firewall

The layered verifier architecture in Anvil succeeds because it mirrors physical component boundaries.

In monolithic codebases, auditing changes requires holding massive context in memory. Reviewing an architectural change forces an agent to reason about hundreds of source files at once. That cognitive load degrades LLM attention and causes models to miss subtle bugs.

Under Lakosian physical design, context is bounded mathematically. A tactical verifier needs only the component directory and its direct upstream headers, easily fitting within the token budget. A strategic verifier needs only public interface contracts and graph topology, completely ignoring private implementation details.

By decoupling tactical cheat detection from strategic graph verification, Anvil achieves reliable quality control without human micromanagement. Workers remain fast and focused on private code, while independent verifiers guarantee architectural integrity at every commit.
