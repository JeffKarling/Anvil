# Anvil human engineering manual

Anvil is an agentic C++ project blueprint built exclusively for Google Antigravity on Linux. In this workflow, an experienced C++ engineer stops writing implementation code by hand. You also stop relying on manual code inspection or gut feelings. Instead, you author high level system requirements and curate approved third party libraries. You trust the **anchor constrained capability contraction** algorithm, and your reviews center on structured JSON telemetry produced by the system.

As a template, Anvil configures a portable C++20 baseline across all components in [target_properties.cmake](../cmake/templates/target_properties.cmake). Public interfaces remain minimal and standard. New components created by the orchestrator default to this clean C++20 baseline. The template also provides exemplar foundation components like [journal](../targets/journal/CMakeLists.txt) to demonstrate private C++23 adoption. For example, `journal` uses `std::views::enumerate` and `std::stacktrace` behind its private translation unit without leaking C++23 requirements to upstream callers.

## Native Antigravity orchestration and division of labor

Anvil exploits the concurrent multi agent runtime in Google Antigravity. You never manually spawn or micromanage worker subagents. All interactions pass through the deterministic monitor supervisor while framework automation manages delegated tasks.

**Monitor supervisor.** The primary session acts through the [`monitor`](../.agents/agents/monitor/agent.json) agent. The monitor acts as a deterministic state machine. It does not write C++ source code directly. Instead, it reads requirements, coordinates strategic and tactical workers, and gates progress with verifiers.

**Strategic worker and verifier.** The monitor delegates whole graph partitioning and public contract design to [`strategic_worker`](../.agents/agents/strategic_worker/agent.json). Before any implementation begins, [`strategic_verifier`](../.agents/agents/strategic_verifier/agent.json) audits the public contracts against invariant gates $H_1$ through $H_5$. Once verified, the contracts are committed to establish a fixed boundary.

**Tactical worker and verifier duo.** The monitor delegates private `.cpp` implementations and local optimization loops to short lived worker subagents defined in [`tactical_worker`](../.agents/agents/tactical_worker/agent.json) running in shared worktrees. Once a worker completes its scoped builds, a read only tactical verifier defined in [`tactical_verifier`](../.agents/agents/tactical_verifier/agent.json) audits the diff for test dilution, contract tampering, and benchmark gaming.

**Human direction via prompt recipes.** Rather than formulating ad hoc instructions, human engineers use structured workflows. Detailed prompts for bootstrapping projects, running refactoring passes, and profiling hot paths are collected in the companion guide [prompts.md](guides/prompts.md).

## Provisioning third party libraries as a capability multiplier

The highest leverage action you can take before starting a feature is populating [cmake/dependencies.cmake](../cmake/dependencies.cmake) with vetted third party libraries.

When translating your requirements, the orchestrator explores candidate libraries in [cmake/dependencies.cmake](../cmake/dependencies.cmake). Drawing on deep systems knowledge, it evaluates architectural trade offs, memory layout characteristics, and zero copy efficiency. The orchestrator decides which library best fits the architecture using technical judgment that goes deeper than human heuristics. Once selected, a worker subagent writes a compact private adapter around that library. When no suitable library is registered, the worker subagent writes bespoke C++ algorithms from scratch. Bespoke code consumes far more context tokens, takes more optimization iterations, and carries a larger surface for subtle bugs.

Because Anvil enables link time optimization via `ENABLE_IPO=ON` in release builds and links third party targets strictly `PRIVATE` inside leaf components, registering extra candidate libraries adds zero binary bloat. You do not need to decide in advance which exact library every internal component will use. The more high quality libraries you expose, the better the orchestrator can assemble a fast and reliable application.

### Example third party library expansion

Declare external packages globally in [cmake/dependencies.cmake](../cmake/dependencies.cmake) using standard CMake commands. Below are example libraries across common systems domains.

**Serialization and schema generation.** Provision binary schema tools like `protobuf`, `flatbuffers`, and `capnproto`. Add structured parsers like `simdjson`, `yyjson`, or `sd_json` from `libsystemd` so worker subagents build zero copy parsers without hand written state machines.

**Concurrency and event loops.** Expose `tbb` and `concurrentqueue` for task arenas and lock free queues. Include `liburing` for asynchronous kernel I/O rings and `sd_event` from `libsystemd` for Linux event loops.

**Vectorized math and numerical kernels.** Provide `highway` or `xsimd` for portable SIMD dispatch alongside `eigen3`, `openblas`, or Intel MKL for linear algebra.

**Compression and cryptography.** Register `libzstd` and `liblz4` for high throughput block compression. Add `openssl` and `libsodium` for constant time cryptographic operations.

**Storage and embedded databases.** `sqlite3`, `lmdb`, and `rocksdb` allow stateful components to persist structured data behind transactional guarantees.

**Networking and transport.** Provision `libcurl` and `nghttp2` for HTTP traffic. Add `grpc++` and `zeromq` to cover RPC and low latency message bus transports.

**Command line and configuration.** `CLI11` and `re2` handle entrypoint flag parsing in `targets/app/` and deterministic regular expression matching.

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

All entries in [cmake/dependencies.cmake](../cmake/dependencies.cmake) use `QUIET` discovery by default. This minimizes configuration noise and allows a greenfield project to initialize and run even when nothing exists apart from a main function. Listing a library with `QUIET` signals that the dependency is pre approved for use. Conversely, when you explicitly change a dependency to `REQUIRED`, that serves as a strong directive telling the orchestrator that the library must be enabled and integrated into the design.

Behind the scenes, workers link imported library targets strictly `PRIVATE`. They keep `targets/<name>/<name>/<name>.hpp` completely free of third party headers so vendor upgrades never trigger downstream rebuilds or bloat caller context.

## Mathematical DAG synthesis via the capability contraction algorithm

A signature capability of Anvil is how the orchestrator synthesizes the physical component graph into a directed acyclic graph. Under John Lakos physical design, a component is a self contained physical unit. It consists of a single public header, a private implementation file, and a colocated test suite. Algorithmic components also include a hardware benchmark suite. A physical component graph is the acyclic dependency structure connecting these isolated components.

Human engineers naturally organize code into conceptual taxonomies like a monolithic algorithms component or a broad utils library. For autonomous AI systems, human taxonomies fail. They pull unneeded headers into LLM context windows, serialize worker subagent tasks, and create merge conflicts.

Anvil solves this problem through the **anchor constrained capability contraction algorithm**. The orchestrator decomposes your requirements into atomic capability operations and decorates each operation with six physical coordinates. These coordinates track execution nature and verification profiles alongside external library bindings. They also record compiler flag regimes, token footprints, and churn volatility.

The algorithm groups capabilities into components by solving an optimization problem governed by five hard invariant gates.

**Quotient graph acyclicity.** The resulting component dependency graph must remain strictly acyclic so targets link cleanly and worker waves can execute concurrently in topological order.

**Anchor preservation.** Foundational repository anchors like `journal`, `perf_scope`, and `app` must never be merged into other components because shared observability and entrypoints must stay globally independent.

**Execution and verification parity.** Pure in memory compute kernels are never merged with stateful OS or I/O boundaries. This ensures compute components receive deterministic hardware PMU benchmarks while boundary components stay focused on Lippincott exception firewalls.

**Compiler regime homogeneity.** Capabilities requiring specialized compiler flags like `-fno-fast-math`, SIMD overrides, or private C++23 features are isolated into their own components so non standard flags never leak into unrelated code.

**Context locality.** The combined public and private token footprint of a component and its direct upstream headers must not exceed the worker context ceiling $B_{\max} = 16384$. Every worker fits its entire task in working memory without truncation. For an in depth breakdown of this exact constant, read [The 16384 token ceiling in physical component design](articles/the_16384_token_ceiling.md).

Within this feasible space, the algorithm minimizes a **friction cost function** balancing four physical forces.

**Context waste.** Penalizes pulling unused public functions into downstream callers.

**Blast radius.** Penalizes deep dependency chains and high churn on shared upstream components.

**Scaffolding drag.** Prevents trivial component explosion when capabilities naturally belong together.

**Vendor insulation.** Drives components that wrap external libraries to keep public contracts compact.

The result is a wide and shallow component graph. The orchestrator can dispatch multiple worker subagents in parallel across isolated Git worktrees with zero merge conflicts.

### Mathematical worker subagent sizing from ACCC coordinates

In the Google Gemini AI domain, higher reasoning budgets generate hidden thinking tokens before every tool call. Because thinking tokens multiply across every turn of an edit, compile, and test loop, oversizing a worker on a simple adapter wastes tokens and increases latency.

Anvil combines five component metrics from the algorithm into a deterministic sizing score $\Psi(C_i) \in [0, 1]$ for every component $C_i$.

$$\Psi(C_i) = 0.30 \left(\frac{W(C_i)}{B_{\max}}\right) + 0.30 K(C_i) + 0.20 \min\!\left(1,\, \Theta(C_i)\right) + 0.10 \nu(C_i) + 0.10 \mathbb{I}\!\left(\|\chi(C_i)\|_1 > 0\right)$$

In this equation, $W(C_i) / B_{\max}$ is the context saturation ratio against the $16384$ token ceiling. $K(C_i)$ is empirical churn volatility. $\Theta(C_i)$ is vendor header toxicity load from [cmake/dependencies.cmake](../cmake/dependencies.cmake). $\nu(C_i)$ indicates whether `<name>BENCH` is present, and $\mathbb{I}(\|\chi(C_i)\|_1 > 0)$ indicates specialized local compiler flags. Rapid churn signals active regression risk, while heavy vendor bindings and custom compiler flags add subtle edge cases. The introspection script [sync_manifest.py](../.agents/skills/architect/scripts/sync_manifest.py) computes $\Psi(C_i)$ automatically and maps each component to the model parameter of `invoke_subagent`.

| Sizing score range | `invoke_subagent` model value | Target reasoning profile | Component characteristics |
| :--- | :--- | :--- | :--- |
| $\Psi(C_i) < 0.70$ | `flash` | Standard fast reasoning tier | Adapters, stateful OS boundaries, exception firewalls, single vendor library bindings |
| $\Psi(C_i) \ge 0.70$ | `pro` | High reasoning frontier tier | Hot compute kernels with `<name>BENCH` PMU gates, SIMD regimes, multi library insulation, high churn |

Both $\Psi(C_i)$ and the selected model tier are persisted inside [manifest.json](../production_artifacts/manifest.json) for every component.

### Example component design versus production component design

The project provides hand crafted example components in `targets/` to demonstrate physical encapsulation in code. Proto requirement is split into two components in [item_proto](../targets/item_proto) and [item_store](../targets/item_store). This hand crafted design is deliberately suboptimal because both targets wrap the same Protobuf generated code. Keeping it serves an educational purpose demonstrating less optimal component design.

In production, human engineers should never prescribe whether a schema is split or merged. The core philosophy of Anvil is to trust the algorithm to make the correct decision. For the worked Protobuf case study, read [The Protobuf pedagogic example](articles/protobuf_pedagogic_example.md). For the broader lifecycle philosophy, read [Trust the algorithm in systems architecture](articles/trust_the_algorithm.md). For adversarial verification, read [Verification philosophy in agentic physical design](articles/tactical_and_strategic_verifiers.md).

### How the algorithm calculates component boundaries

The algorithm mathematically decides between a single component and two components by balancing scaffolding drag against blast radius and context waste.

When a schema is consumed by only one operational capability, its consumer fan out is one. In this scenario, splitting into two targets introduces scaffolding drag. Because no other component consumes the schema, keeping it in a separate target creates an extra CMake target and extra build graph edges for zero isolation benefit. Because `item_proto` has a fan out of one in the starter template, [sync_manifest.py](../.agents/skills/architect/scripts/sync_manifest.py) automatically detects `item_proto -> item_store` and records it as an advisory `topology_repartition` telemetry note inside [manifest.json](../production_artifacts/manifest.json) along with its `benefit_score`, `standalone_rework_cost`, and `net_gain`.

When a schema is consumed by multiple independent capabilities, the fan out is greater than one. Merging the schema into one consumer would force secondary consumers to depend on unrelated logic. That introduces high blast radius and context waste. In this scenario, the cost function heavily penalizes the merged layout. The algorithm automatically extracts a dedicated schema target like `item_proto` and links it privately across all consumers.

## Providing structured requirements

Typing a brief request into a chat box creates the false impression that complex systems architecture can be inferred from a casual sentence. Instead, provide structured requirements that the orchestrator can read. The orchestrator can read a file in your workspace, a ticket in an issue tracker, or a specification page.

If you are an experienced C++ engineer, your natural instinct may be to specify low level C++ mechanics such as `std::span` signatures or `noexcept` boundaries. You might also be tempted to prescribe compiler flags or class splits. In Anvil, writing low level specifications is counterproductive. The orchestrator and worker subagents already enforce modern C++ idioms, exception firewalls, and hardware optimizations automatically through invariants. When you step up to a higher level of abstraction and describe what the system must accomplish rather than how to write C++ syntax, the orchestrator makes significantly better architectural and library choices. For an in depth look at why prompt micromanagement fails, read [Compiler boundaries over prompt rule bloat](articles/compiler_boundaries_over_prompt_rules.md).

Focus your requirements on four high level areas.

**External system boundaries and data flow.** Describe where data enters and leaves the application at the OS, storage, or network edge rather than trying to predesign internal components. Concrete descriptions give the orchestrator exact boundary signals. From those descriptions, the orchestrator separates stateful I/O boundaries from pure in memory compute targets so compute kernels receive deterministic hardware counter harnesses.

**Domain accuracy and numerical intent.** State numerical precision requirements in domain terms when they matter. For instance, require exact decimal rounding or strict IEEE 754 NaN and infinity preservation for sensor dropout detection. The orchestrator automatically applies `-fno-fast-math` to whichever internal component implements that math. Instruction cloning via `target_clones` is strictly an autonomous worker task triggered after hardware benchmarking.

**Candidate third party libraries.** Mention which third party libraries you have added to [cmake/dependencies.cmake](../cmake/dependencies.cmake) for major workloads. Primary architectural choices then match your intent while the orchestrator remains free to select secondary utilities.

**Explicit C++ design preferences only when mandatory.** The orchestrator defaults to modern C++ features, strong domain types, and structured flight recorder logging out of the box. State a specific C++ design pattern or error handling convention in your requirements only when you have a strict reason to mandate it. Extra rules restrict the orchestrator from choosing simpler designs.

## Human and orchestrator Git collaboration

In Anvil, Git history is an active input to the mathematical model rather than a passive archive. Following three Git habits keeps the orchestrator, worker subagents, and metrics synchronized.

**Clean working tree gate before orchestration.** The orchestrator spawns worker subagents in shared worktrees branched from `HEAD`. Isolating workers into separate worktrees minimizes context exposure and edit blast radius while preventing file collisions. For an in depth analysis of how this physical isolation compares to conversational multi agent swarms, read [How Anvil verifiers compare to Swarm](articles/how_anvils_verifiers_compare_to_swarm.md). Because worktrees branch from `HEAD`, uncommitted files are invisible to subagents. To prevent silent drift, skills run `sync_manifest.py --require-clean-git` and refuse to start if uncommitted changes exist. Commit or stash all working tree changes before starting an orchestration run.

**Atomic commits keep empirical churn accurate.** Churn volatility measures how often a component changes over recent history. Rapidly changing targets carry higher regression risk and increase blast radius for downstream callers. The script [sync_manifest.py](../.agents/skills/architect/scripts/sync_manifest.py) computes $K(C_i)$ solely from modified file paths in `git log --name-only` over the last 50 commits. It filters out bulk commits touching more than four targets so formatting sweeps or template imports do not skew volatility. Because $K(C_i)$ accounts for 30 percent of the worker sizing score $\Psi(C_i)$, keeping manual commits scoped to one feature or component prevents unrelated targets from looking volatile.

**Ad hoc manual edits and the resync workflow.** When you edit C++ files or `CMakeLists.txt` manually in an IDE, Git hooks automatically run `sync_manifest.py` to update [manifest.json](../production_artifacts/manifest.json) and check mathematical gates $H_1$ through $H_5$. Before handing control back to the orchestrator after manual edits, invoke the resync skill in [.agents/skills/resync/SKILL.md](../.agents/skills/resync/SKILL.md). This brings dirty hardware reports and dual compiler builds back into full parity before committing.

## Available reports and working alongside IDEs and CI/CD

Anvil is built first and foremost for Google Antigravity where you do not need a manual build terminal or manual code review checklists. Trust the algorithm to synthesize component boundaries and delegate implementation loops instead of speculating from human gut feelings.

The system exposes structured reports and records that summarize repository state and surface potential refactorings.

**Versioned repository manifest and advisory refactor telemetry.** Inspect [manifest.json](../production_artifacts/manifest.json) to review the authoritative dependency graph edges, per component coordinates, rework costs, and worker subagent sizing scores $\Psi(C_i)$. The manifest also records invariant gate statuses $H_1$ through $H_5$ and the active `refactor_candidates` array. Each candidate record is classified under `topology_repartition`, `kernel_acceleration`, `contract_insulation`, or `verification_sync` and anchored to its discovery commit hash. Instead of requiring manual human approval flags, each note records a deterministic `benefit_score`, `standalone_rework_cost`, and `net_gain` calculated as $\text{NetGain} = \Delta \Phi_{\text{benefit}} - C_{\text{rework}}$. During requirement evolution, strategic and tactical workers fold these telemetry hints into touched subgraphs under a free rider rework discount and execute standalone refactors on untouched subgraphs whenever `net_gain` is positive. Refer to [prompts.md](guides/prompts.md) for prompts that trigger autonomous refactoring runs.

**Versioned JSON hardware benchmark reports.** Inspect `production_artifacts/profiling/<name>_score_report.json` to review nanosecond latencies, CPU cycle counts, and IPC alongside cache miss ratios. Each report provides hardware bottleneck classifications and a deterministic stopping directive set to `continue_optimizing`, `stop_hardware_saturated`, or `stop_diminishing_returns`. Optimization loops stop objectively instead of guessing.

**Public error catalogs and contract headers.** Each component maintains a structured error catalog in `targets/<name>/<name>.catalog` and a clean public contract in `targets/<name>/<name>/<name>.hpp`. This documents boundary behavior without exposing private implementation details.

Even though the orchestrator and worker subagents execute builds autonomously inside your Antigravity workspace, Anvil defines compiler and sanitizer configurations through standard CMake presets in [CMakePresets.json](../CMakePresets.json). If you open the repository in a C++ IDE such as CLion or VS Code, the IDE automatically detects the presets. Furthermore, you can configure your remote CI/CD pipeline to run `python3 .agents/skills/architect/scripts/sync_manifest.py --check`, `./production_artifacts/build_all.sh`, and the sanitizer presets so remote pull request gates enforce the exact same invariants as local worker subagents.

## Host environment setup

Before starting your first agentic session, unlock Linux kernel PMU counter access so `anvil::perf_scope` can read hardware CPU registers directly. Lock the CPU governor to performance so benchmark cycles remain reproducible.

```bash
sudo sysctl kernel.perf_event_paranoid=1
powerprofilesctl set performance
```
