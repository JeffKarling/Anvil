# Anvil human engineering manual

Anvil is an agentic C++ project blueprint built exclusively for Google Antigravity on Linux. In this workflow, an experienced C++ engineer stops writing implementation code by hand and stops relying on manual code inspection or gut feelings. Instead, you author high level system requirements and curate approved third party libraries. You trust the **anchor constrained capability contraction** algorithm and your reviews include the structured JSON telemetry and refactoring records produced by the system.

As a template, Anvil configures a portable C++20 baseline across all components in [target_properties.cmake](../cmake/templates/target_properties.cmake) so public interfaces remain minimal and standard. New components created by the orchestrator default to this clean C++20 baseline. The template also provides exemplar foundation components like [journal](../targets/journal/CMakeLists.txt) to demonstrate private C++23 adoption. For example, `journal` uses `std::views::enumerate` and `std::stacktrace` behind its private translation unit without leaking C++23 requirements to upstream callers.

## Native Antigravity orchestration and division of labor

Anvil exploits the concurrent native multi agent runtime in Google Antigravity as a core built in capability. You never manually spawn, coordinate, or micromanage worker subagents. All interactions are with the top level orchestrator while the framework automation manages intelligently delegated worker subagent work.

* **Human focus and available reports.** Rather than speculating on architecture or optimization from old school gut feelings, trust the algorithm and review the versioned JSON telemetry generated in [manifest.json](../production_artifacts/manifest.json) and `production_artifacts/profiling/<name>_score_report.json`. In this version of Anvil, [manifest.json](../production_artifacts/manifest.json) surfaces structured `refactor_candidates` records calculated directly from graph topology, context saturation, and hardware PMU telemetry. To explore further performance gains, you can prompt the orchestrator with a question such as *"Are there any additional dependencies that can further improve component performance, and if so what third party library can I add to approved project dependencies?"* Explicit latency numbers are only needed in requirements where a hard deadline is known in advance because hardware PMU benchmarks guide routine optimization automatically.
* **Model agnostic orchestrator.** The primary Antigravity session acts as the strategic orchestrator regardless of which frontier model you select. Gemini 4 Argon is recommended because Gemini models adopt the orchestrator role proactively from repository context, whereas other models such as Claude may need explicit prompt instruction to assume the orchestrator role and delegate workers. Acting through [.agents/skills/architect/SKILL.md](../.agents/skills/architect/SKILL.md), the orchestrator reads your requirements and [cmake/dependencies.cmake](../cmake/dependencies.cmake). It partitions the system into a directed acyclic graph of physical components, scaffolds public header contracts via [scaffold.py](../.agents/skills/feature/scripts/scaffold.py), and commits clean public interfaces at the contract anchor so worker subagents see fixed boundaries in parallel worktrees.
* **Tactical worker and verifier duo.** The orchestrator delegates private `.cpp` implementations and local optimization loops to short lived worker subagents defined in [.agents/agents/tactical_worker/agent.json](../.agents/agents/tactical_worker/agent.json) running in `Workspace: "share"`. Once a worker completes its scoped builds and tests, a read only tactical verifier defined in [.agents/agents/tactical_verifier/agent.json](../.agents/agents/tactical_verifier/agent.json) audits the diff for test dilution, contract tampering, and benchmark gaming before the orchestrator commits changes to the main branch.
* **Strategic verifier at key checkpoints.** Before delegating parallel worker waves and after merging all component branches, the orchestrator invokes a read only strategic verifier defined in [.agents/agents/strategic_verifier/agent.json](../.agents/agents/strategic_verifier/agent.json). Running in `Workspace: "inherit"`, the strategic verifier audits public contracts, checks DAG acyclicity and manifest gates $H_1$ through $H_5$, and confirms whole graph builds pass without editing code.

## Provisioning third party libraries as a capability multiplier

The highest leverage action you can take before starting a feature is populating [cmake/dependencies.cmake](../cmake/dependencies.cmake) with a rich selection of vetted third party libraries.

When translating your requirements, the orchestrator explores candidate libraries in [cmake/dependencies.cmake](../cmake/dependencies.cmake). Drawing on deep systems knowledge, it evaluates architectural trade offs, memory layout characteristics, and zero copy efficiency across registered candidates. The orchestrator decides which library best fits the architecture using technical judgment that goes deeper than human heuristics. Once selected, the orchestrator delegates a worker subagent to write a compact private adapter around that library. When no suitable library is registered, the worker subagent is forced to write bespoke C++ algorithms from scratch. Bespoke code consumes far more context tokens, takes more optimization iterations, and carries a larger surface for subtle bugs.

Because Anvil enables link time optimization via `ENABLE_IPO=ON` in release builds and links third party targets strictly `PRIVATE` inside leaf components, registering extra candidate libraries in [cmake/dependencies.cmake](../cmake/dependencies.cmake) adds zero binary bloat to components that do not use them. You do not need to decide in advance which exact library every internal component will use. The more high quality libraries you expose in [cmake/dependencies.cmake](../cmake/dependencies.cmake), the better the orchestrator can assemble a fast, reliable application.

### Example third party library expansion

Declare external packages globally in [cmake/dependencies.cmake](../cmake/dependencies.cmake) using standard CMake `find_package` or `pkg_check_modules`. Below are example libraries across common systems domains that give the orchestrator strong building blocks.

* **Serialization and schema generation.** Provision binary schema tools like `protobuf`, `flatbuffers`, and `capnproto`. Add structured parsers like `simdjson`, `yyjson`, or `sd_json` from `libsystemd` so worker subagents build zero copy parsers without hand written state machines.
* **Concurrency and event loops.** Expose `tbb` and `concurrentqueue` for task arenas and lock free queues. Include `liburing` for asynchronous kernel I/O rings and `sd_event` from `libsystemd` for Linux event loops.
* **Vectorized math and numerical kernels.** Provide `highway` or `xsimd` for portable SIMD dispatch alongside `eigen3`, `openblas`, or Intel MKL for linear algebra.
* **Compression and cryptography.** Register `libzstd` and `liblz4` for high throughput block compression. Add `openssl` and `libsodium` for constant time cryptographic operations.
* **Storage and embedded databases.** `sqlite3`, `lmdb`, and `rocksdb` allow stateful components to persist structured data behind transactional guarantees.
* **Networking and transport.** Provision `libcurl` and `nghttp2` for HTTP traffic. Add `grpc++` and `zeromq` to cover RPC and low latency message bus transports.
* **Command line and configuration.** `CLI11` and `re2` handle entrypoint flag parsing in `targets/app/` and deterministic regular expression matching.

```cmake
# Example palette of approved third party libraries in cmake/dependencies.cmake
pkg_check_modules(libsystemd GLOBAL QUIET IMPORTED_TARGET libsystemd)
pkg_check_modules(protobuf GLOBAL QUIET IMPORTED_TARGET protobuf)
find_program(PROTOC_EXECUTABLE NAMES protoc)
pkg_check_modules(tbb GLOBAL QUIET IMPORTED_TARGET tbb)
pkg_check_modules(zstd GLOBAL QUIET IMPORTED_TARGET libzstd)
pkg_check_modules(sqlite3 GLOBAL QUIET IMPORTED_TARGET sqlite3)
pkg_check_modules(xxhash GLOBAL QUIET IMPORTED_TARGET libxxhash)
find_package(OpenSSL QUIET)
pkg_check_modules(liburing GLOBAL QUIET IMPORTED_TARGET liburing)
pkg_check_modules(curl GLOBAL QUIET IMPORTED_TARGET libcurl)
pkg_check_modules(eigen3 GLOBAL QUIET IMPORTED_TARGET eigen3)
```

All entries in [cmake/dependencies.cmake](../cmake/dependencies.cmake) use `QUIET` discovery by default. This minimizes configuration noise and allows a greenfield project to initialize and run even when nothing exists in the repository apart from a `main` function. Listing a library with `QUIET` signals to the orchestrator that the dependency is pre approved for use. If the orchestrator selects an approved library that is not yet installed on the host, the orchestrator can install it or update the build configuration on demand. Conversely, when you explicitly change a dependency to `REQUIRED`, that serves as a strong directive telling the orchestrator that the library must be enabled and integrated into the design. Inspecting the compiled `targets/app/app` binary with `ldd` confirms that unlinked targets in this palette contribute zero shared library dependencies and zero binary bytes until a worker subagent explicitly links them `PRIVATE`.

Behind the curtains, the orchestrator and worker subagents handle all CMake linkage rules and header insulation automatically. Standard CMake `find_package` imported targets work seamlessly alongside `pkg_check_modules`. Worker subagents link imported library targets strictly `PRIVATE` and keep `targets/<name>/<name>/<name>.hpp` completely free of third party headers so vendor upgrades never trigger downstream rebuilds or bloat caller context. Even specialized build pipelines such as code generated Protobuf schema components or custom test harnesses are configured by the orchestrator in a completely hands off manner.

## Mathematical DAG synthesis via the capability contraction algorithm

A signature core capability of Anvil is how the orchestrator synthesizes the physical component graph into a directed acyclic graph. Under John Lakos physical design, a component is a self contained physical unit. It consists of a single public header, a private implementation file, and a colocated test suite. Algorithmic components also include a hardware benchmark suite. A physical component graph is the acyclic dependency structure connecting these isolated components.

Human engineers naturally organize code into conceptual taxonomies like a monolithic algorithms component or a broad utils library. For autonomous AI systems, human taxonomies fail completely. They pull unneeded headers into LLM context windows, serialize worker subagent tasks, and create merge conflicts.

Anvil solves this problem through the **anchor constrained capability contraction algorithm**. In an agentic workflow, this algorithm creates symmetry between user requirements and physical component architecture. The orchestrator decomposes your requirements into atomic capability operations and decorates each operation with six physical coordinates. These coordinates track execution nature and verification profiles alongside external library bindings. They also record compiler flag regimes, token footprints, and churn volatility so the algorithm can weigh isolation benefits against context and build costs.

The anchor constrained capability contraction algorithm groups capabilities into components by solving an optimization problem governed by five hard invariant gates.

* **Quotient graph acyclicity.** The resulting component dependency graph must remain strictly acyclic so targets link cleanly and worker waves can execute concurrently in a topological order.
* **Anchor preservation.** Foundational repository anchors like `journal`, `perf_scope`, and `app` must never be merged into other components because shared observability and entrypoints must stay globally independent.
* **Execution and verification parity.** Pure in memory compute kernels are never merged with stateful OS or I/O boundaries. This ensures compute components receive deterministic hardware PMU benchmarks while boundary components stay focused on Lippincott exception firewalls.
* **Compiler regime homogeneity.** Capabilities requiring specialized compiler flags like `-fno-fast-math`, SIMD overrides, or private C++23 features are isolated into their own components so non standard flags never leak into unrelated code.
* **Context locality.** The combined public and private token footprint of a component and its direct upstream headers must not exceed the worker subagent context ceiling $B_{\max} = 16384$ so every worker fits its entire task in working memory without truncation.

Within this feasible space, the algorithm minimizes a **friction cost function** balancing four physical forces.

* **Context waste.** Penalizes pulling unused public functions into downstream callers.
* **Blast radius.** Penalizes deep dependency chains and high churn on shared upstream components.
* **Scaffolding drag.** Prevents trivial component explosion when capabilities naturally belong together.
* **Vendor insulation.** Drives components that wrap external libraries to keep public contracts compact.

The result is a wide, shallow component graph. Because the graph is wide and shallow, the orchestrator can dispatch multiple worker subagents in parallel across isolated Git worktrees with zero merge conflicts.

### Mathematical worker subagent sizing from ACCC coordinates

In the Google Gemini AI domain, higher reasoning budgets generate hidden thinking tokens before every tool call. Because thinking tokens multiply across every turn of an edit, compile, and test loop, oversizing a worker subagent on a simple adapter wastes tokens and increases latency.

Anvil combines five component metrics from the **anchor constrained capability contraction algorithm** into a deterministic sizing score $\Psi(C_i) \in [0, 1]$ for every component $C_i$.

$$\Psi(C_i) = 0.30 \left(\frac{W(C_i)}{B_{\max}}\right) + 0.30 K(C_i) + 0.20 \min\!\left(1,\, \Theta(C_i)\right) + 0.10 \nu(C_i) + 0.10 \mathbb{I}\!\left(\|\chi(C_i)\|_1 > 0\right)$$

In this equation, $W(C_i) / B_{\max}$ is the context saturation ratio against the $16384$ token ceiling, $K(C_i)$ is empirical churn volatility, $\Theta(C_i)$ is vendor header toxicity load from [cmake/dependencies.cmake](../cmake/dependencies.cmake), $\nu(C_i)$ indicates whether `<name>BENCH` is present, and $\mathbb{I}(\|\chi(C_i)\|_1 > 0)$ indicates specialized local compiler flags. Rapid churn signals active regression risk, while heavy vendor bindings and custom compiler flags add subtle edge cases that require higher reasoning capacity. The introspection script [.agents/skills/architect/scripts/sync_manifest.py](../.agents/skills/architect/scripts/sync_manifest.py) computes $\Psi(C_i)$ automatically and maps each component to the `Model` parameter of `invoke_subagent`.

| Sizing score range | `invoke_subagent` `Model` value | Target reasoning profile | Component characteristics |
| :--- | :--- | :--- | :--- |
| $\Psi(C_i) < 0.70$ | `flash` | Standard fast reasoning tier | Adapters, stateful OS boundaries, exception firewalls, single vendor library bindings |
| $\Psi(C_i) \ge 0.70$ | `pro` | High reasoning frontier tier | Hot compute kernels with `<name>BENCH` PMU gates, SIMD regimes, multi library insulation, high churn $K(C_i)$ |

Both $\Psi(C_i)$ and the selected `Model` tier are persisted inside `production_artifacts/manifest.json` for every component.

### Example component design versus production component design

The project provides hand crafted example components in `targets/` to demonstrate physical encapsulation in code. Proto requirement is split into two components in [item_proto](../targets/item_proto) and [item_store](../targets/item_store). This hand crafted two component design is objectively wrong as both targets include the same protobuf generated code, keeping it serves an educational purpose demonstrating less optimal component design.

In production, human engineers should never hand craft or prescribe whether a Protobuf schema is split or merged. The core philosophy of Anvil is to trust the **anchor constrained capability contraction algorithm** to make the correct decision. For the worked Protobuf case study, read **[The Protobuf pedagogic example](articles/protobuf_pedagogic_example.md)**, for the broader lifecycle philosophy read **[Trust the algorithm in systems architecture](articles/trust_the_algorithm.md)**, and for adversarial verification read **[Verification philosophy in agentic physical design](articles/tactical_and_strategic_verifiers.md)**.

### How the algorithm calculates component boundaries

The anchor constrained capability contraction algorithm mathematically decides between a single component and two components by balancing scaffolding drag against blast radius and context waste.

When a schema is consumed by only one operational capability, its consumer fan out is one. In this scenario, splitting into two targets introduces scaffolding drag. Because no other component consumes the schema, keeping it in a separate target creates an extra CMake target, an extra directory, and extra build graph edges for zero isolation benefit. Because `item_proto` has a fan out of one in the starter template, `sync_manifest.py` automatically detects `item_proto -> item_store` and records it as a `topology_repartition` candidate inside `production_artifacts/manifest.json` with `user_directive` defaulted to `"ignored"`.

When a schema is consumed by multiple independent capabilities, the fan out is greater than one. Merging the schema into one consumer would force secondary consumers to depend on unrelated logic. That introduces high blast radius and context waste. In this scenario, the cost function heavily penalizes the merged layout. The algorithm automatically extracts a dedicated schema target like `item_proto` and links it privately across all consumers.

## Providing structured requirements

Typing a brief request into a chat box creates the false impression that complex systems architecture can be inferred from a casual sentence. Instead, provide structured requirements that the orchestrator can read. The orchestrator can read a file in your workspace, a ticket in an issue tracker, or a specification page. What matters is that the requirements provide a clear functional foundation.

If you are an experienced C++ engineer, your natural instinct may be to specify low level C++ mechanics such as `std::span` signatures or `noexcept` boundaries. You might also be tempted to prescribe compiler flags or how classes should be split across files. In Anvil, writing low level specifications is counterproductive. The orchestrator and worker subagents already enforce modern C++20 and C++23 idioms, exception firewalls, and hardware optimizations automatically through [.agents/rules/invariants.md](../.agents/rules/invariants.md). When you step up to a higher level of abstraction and describe what the system must accomplish rather than how to write the C++ syntax, the orchestrator makes significantly better architectural and library choices. For an in depth look at why prompt micromanagement fails and how physical boundaries empower evolving models, read **[Compiler boundaries over prompt rule bloat](articles/compiler_boundaries_over_prompt_rules.md)**.

Focus your requirements on four high level areas.

* **External system boundaries and data flow.** Describe where data enters and leaves the application at the OS, storage, or network edge rather than trying to pre-design internal components. Concrete phrases such as *"receive multicast UDP market packets from a socket and decode order book snapshots"*, *"ingest compressed telemetry batches from disk and filter corrupted records"*, or *"publish service health status to systemd"* give the orchestrator exact boundary signals. While these examples illustrate Linux daemon and network services, the same boundary separation applies to GUI event loops or storage backends. From those high level descriptions, the orchestrator automatically separates stateful I/O boundaries from pure in memory compute targets so compute kernels receive deterministic `<name>BENCH` hardware counter harnesses.
* **Domain accuracy and numerical intent.** You cannot call out internal component names or compiler flags in advance because the orchestrator has not designed the component graph yet. Instead, state numerical precision requirements in domain terms when they matter, such as requiring exact decimal rounding or strict IEEE 754 `NaN` and infinity preservation for sensor dropout detection. The orchestrator automatically applies `-fno-fast-math` to whichever internal component implements that math. Likewise, CPU instruction cloning via `target_clones` is strictly an autonomous worker subagent task triggered after hardware benchmarking and never needs to be requested by the user.
* **Candidate third party libraries.** Mention which third party libraries you have added to [cmake/dependencies.cmake](../cmake/dependencies.cmake) for major workloads so primary architectural picks match your intent while the orchestrator remains free to select secondary utilities.
* **Explicit C++ design preferences only when mandatory.** The orchestrator defaults to modern C++ features, strong domain types, and structured flight recorder logging out of the box. State a specific C++ design pattern or error handling convention in your requirements only when you have a strict reason to mandate it because extra rules restrict the orchestrator from choosing simpler designs.

## Human and orchestrator Git collaboration

In Anvil, Git history is an active input to the mathematical model rather than a passive archive. Following three Git habits keeps the orchestrator, worker subagents, and ACCC metrics synchronized.

* **Hard clean working tree gate before orchestration.** The orchestrator always spawns worker subagents with `Workspace` set to `"share"` so Antigravity branches isolated Git worktrees from `HEAD`. Isolating workers into separate worktrees minimizes each worker's context exposure and edit blast radius while preventing parallel file collisions. For an in depth analysis of how this physical isolation compares to conversational multi-agent swarms, read **[How Anvil verifiers compare to Swarm](articles/how_anvils_verifiers_compare_to_swarm.md)**. Because those worktrees branch from `HEAD`, any uncommitted file would be invisible to subagents. To prevent silent drift, both [.agents/skills/architect/SKILL.md](../.agents/skills/architect/SKILL.md) and [.agents/skills/performance/SKILL.md](../.agents/skills/performance/SKILL.md) run `sync_manifest.py --require-clean-git` at Step 1 and refuse to start if any uncommitted or untracked changes exist. Commit or stash all working tree changes before starting an orchestration run, including edits to [cmake/dependencies.cmake](../cmake/dependencies.cmake) and requirement specifications.
* **Natural atomic commits keep empirical churn $K(C_i)$ accurate.** Churn volatility measures how often a component changes over recent history because rapidly changing targets carry higher regression risk and increase blast radius for downstream callers. The introspection script [.agents/skills/architect/scripts/sync_manifest.py](../.agents/skills/architect/scripts/sync_manifest.py) computes $K(C_i)$ solely from modified file paths in `git log --name-only` over the last 50 commits. It ignores commit messages because prose labels are subjective, and it filters out bulk commits touching more than four targets so formatting sweeps or template imports do not skew volatility. Because $K(C_i)$ accounts for 30 percent of the worker sizing score $\Psi(C_i)$, keeping manual commits scoped to one feature or component prevents unrelated targets from looking volatile and being pushed into higher cost `flash` or `pro` subagent tiers.
* **Ad hoc manual edits and the resync workflow.** When you edit C++ files or `CMakeLists.txt` manually in an IDE or ask for a quick ad hoc fix outside the `architect` workflow, the lifecycle hook in [.agents/hooks.json](../.agents/hooks.json) and the Git `pre-commit` hook automatically run `sync_manifest.py` to update `production_artifacts/manifest.json` and check fast mathematical gates $H_1$ through $H_5$. Before handing control back to the orchestrator after manual edits, invoke the resync skill in [.agents/skills/resync/SKILL.md](../.agents/skills/resync/SKILL.md). This brings dirty `<name>BENCH_run` hardware reports and dual compiler builds back into full parity before committing so the orchestrator plans from verified state rather than stale artifacts.

## Available reports and working alongside IDEs and CI/CD

Anvil is built first and foremost for Google Antigravity where you do not need a manual build terminal or manual code review checklists. Trust the anchor constrained capability contraction algorithm to synthesize component boundaries and delegate implementation loops instead of speculating from human gut feelings.

In this version of Anvil, the system exposes structured reports and records that summarize the state of the repository and surface potential refactorings.

* **Versioned repository manifest and refactor candidates.** Inspect [manifest.json](../production_artifacts/manifest.json) to review the authoritative dependency graph `edges`, per component ACCC coordinates, and worker subagent sizing scores $\Psi(C_i)$. The manifest also records invariant gate statuses $H_1$ through $H_5$ and the active `refactor_candidates` array. You should regularly review the JSON records inside `refactor_candidates` for algorithmically discovered refactoring potential rather than relying on manual intuition. Each candidate record is classified under `topology_repartition`, `kernel_acceleration`, `contract_insulation`, or `verification_sync`. Every record is anchored to its discovery Git commit hash via `discovered_at_commit` and controlled by a binary `user_directive` set to `"ignored"` or `"approved"`.
* **Versioned JSON hardware benchmark reports.** Inspect `production_artifacts/profiling/<name>_score_report.json` to review structured nanosecond latencies, CPU cycle counts, and IPC alongside cache miss ratios. Each report also provides hardware bottleneck classifications and a deterministic stopping directive set to `continue_optimizing`, `stop_hardware_saturated`, or `stop_diminishing_returns` so optimization loops stop objectively instead of guessing.
* **Public error catalogs and contract headers.** Each component maintains a structured error catalog in `targets/<name>/<name>.catalog` and a clean public contract in `targets/<name>/<name>/<name>.hpp` that documents boundary behavior without exposing private implementation details.
* **Prompting for third party dependency opportunities.** Instead of guessing which code path to rewrite, ask the orchestrator directly whether new third party libraries could accelerate any component. For example, prompt *"Are there any additional dependencies that can further improve component performance, and if so what third party library can I add to approved project dependencies?"*

Even though the orchestrator and worker subagents execute builds autonomously inside your Antigravity workspace, Anvil defines all compiler and sanitizer configurations through standard CMake presets in [CMakePresets.json](../CMakePresets.json). If you open the repository in a C++ IDE such as CLion or VS Code, the IDE automatically detects [CMakePresets.json](../CMakePresets.json) and provides one click shortcuts to launch any build or sanitizer preset. Furthermore, you can configure your remote CI/CD pipeline to run `python3 .agents/skills/architect/scripts/sync_manifest.py --check`, `./production_artifacts/build_all.sh`, and the sanitizer workflow presets in [CMakePresets.json](../CMakePresets.json) so remote pull request gates enforce the exact same invariants as local worker subagents.

## Host environment setup

Before starting your first agentic session, verify that your workstation satisfies the [Host prerequisites in README.md](../README.md#L25-L33), unlock Linux kernel PMU counter access so `anvil::perf_scope` can read hardware CPU registers directly, and lock the CPU governor to performance so benchmark cycles remain reproducible.

```bash
sudo sysctl kernel.perf_event_paranoid=1
powerprofilesctl set performance
```
