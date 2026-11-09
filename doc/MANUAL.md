# Anvil human engineering manual

Anvil is an agentic C++ project blueprint built exclusively for Google Antigravity on Linux. In this workflow, an experienced C++ engineer stops writing implementation code by hand and stops relying on manual code inspection or gut feelings. Instead, you author high level system requirements and curate approved third party libraries. You trust the anchor constrained capability contraction algorithm and review the structured JSON telemetry and refactoring records produced by the system.

As a template, Anvil configures a portable C++20 baseline across all components in [target_properties.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/templates/target_properties.cmake) so public interfaces remain minimal and standard. New components created by the orchestrator default to this clean C++20 baseline. The template also provides exemplar foundation components like [journal](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/targets/journal/CMakeLists.txt) to demonstrate private C++23 adoption. For example, `journal` uses `std::views::enumerate` and `std::stacktrace` behind its private translation unit without leaking C++23 requirements to upstream callers.

## Native Antigravity orchestration and division of labor

Anvil exploits the native multi agent runtime in Google Antigravity as a core built in capability. You never manually spawn, coordinate, or micromanage worker subagents. You interact strictly with the top level orchestrator while the framework manages worker subagent delegation behind the scenes.

* **Human focus and available reports.** Rather than speculating on architecture or optimization from old school gut feelings, trust the algorithm and review the versioned JSON telemetry generated in [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json) and `production_artifacts/profiling/<name>_score_report.json`. In this version of Anvil, [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json) surfaces structured `refactor_candidates` records calculated directly from graph topology, context saturation, and hardware PMU telemetry. To explore further performance gains, you can prompt the orchestrator with a question such as *"Are there any additional dependencies that can further improve component performance, and if so what third party library can I add to approved project dependencies?"* Explicit latency numbers are only needed in requirements where a hard deadline is known in advance.
* **Orchestrator on Gemini 4 Argon.** You run the primary Antigravity session on Gemini 4 Argon. Acting through [.agents/skills/architect/SKILL.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/skills/architect/SKILL.md), the orchestrator reads your requirements and [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake). It partitions the system into a directed acyclic graph of physical components, scaffolds public header contracts via [scaffold.py](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/skills/feature/scripts/scaffold.py), records a clean contract anchor commit, and dispatches parallel worker subagents.
* **Worker subagents in shared Git worktrees.** The orchestrator delegates private `.cpp` implementations and local optimization loops to short lived worker subagents defined in [.agents/agents/tactical_worker/agent.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/tactical_worker/agent.json). By invoking `invoke_subagent` with `Workspace` set to `"share"`, the Antigravity language server automatically provisions an isolated Git worktree sharing the parent `.git` object store and prunes it upon completion. Each worker subagent reads only its assigned `targets/<name>/` directory and direct upstream public headers `targets/<dep>/<dep>/<dep>.hpp` to write the private implementation, verify unit tests, and capture hardware PMU counters.

## Provisioning third party libraries as a capability multiplier

The highest leverage action you can take before starting a feature is populating [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) with a rich selection of vetted third party libraries.

When the orchestrator translates your requirements, it checks every needed capability against the libraries available in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake). When a matching library is available, the orchestrator uses it and delegates a worker subagent to write a compact private adapter around that library. When no suitable library is registered, the worker subagent is forced to write bespoke C++ algorithms from scratch. Bespoke code consumes far more context tokens, takes more optimization iterations, and carries a larger surface for subtle bugs.

Because Anvil enables link time optimization via `ENABLE_IPO=ON` in release builds and links third party targets strictly `PRIVATE` inside leaf components, registering extra candidate libraries in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) adds zero binary bloat to components that do not use them. You do not need to decide in advance which exact library every internal component will use. The more high quality libraries you expose in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake), the better the orchestrator can assemble a fast, reliable application.

### Example third party library expansion

Declare external packages globally in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) using standard CMake `find_package` or `pkg_check_modules`. Below are example libraries across common systems domains that give the orchestrator strong building blocks.

* **Serialization and schema generation.** Provision binary schema tools like `protobuf`, `flatbuffers`, and `capnproto`. Add structured parsers like `simdjson`, `yyjson`, or `sd_json` from `libsystemd` so worker subagents build zero copy parsers without hand written state machines.
* **Concurrency and event loops.** Expose `tbb` and `concurrentqueue` for task arenas and lock free queues. Include `liburing` for asynchronous kernel I/O rings and `sd_event` from `libsystemd` for Linux event loops.
* **Vectorized math and numerical kernels.** Provide `highway` or `xsimd` for portable SIMD dispatch alongside `eigen3`, `openblas`, or Intel MKL for linear algebra.
* **Compression and cryptography.** Register `libzstd` and `liblz4` for high throughput block compression. Add `openssl` and `libsodium` for constant time cryptographic operations.
* **Storage and embedded databases.** `sqlite3`, `lmdb`, and `rocksdb` allow stateful components to persist structured data behind transactional guarantees.
* **Networking and transport.** Provision `libcurl` and `nghttp2` for HTTP traffic. Add `grpc++` and `zeromq` to cover RPC and low latency message bus transports.
* **Command line and configuration.** `CLI11` and `re2` handle entrypoint flag parsing in `targets/app/` and deterministic regular expression matching.

```cmake
# Approved third party library palette in cmake/dependencies.cmake
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

All entries in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) use `QUIET` discovery by default. This minimizes configuration noise and allows a greenfield project to initialize and run even when nothing exists in the repository apart from a `main` function. Listing a library with `QUIET` signals to the orchestrator that the dependency is pre approved for use. If the orchestrator selects an approved library that is not yet installed on the host, the orchestrator can install it or update the build configuration on demand. Conversely, when you explicitly change a dependency to `REQUIRED`, that serves as a strong directive telling the orchestrator that the library must be enabled and integrated into the design. Inspecting the compiled `targets/app/app` binary with `ldd` confirms that unlinked targets in this palette contribute zero shared library dependencies and zero binary bytes until a worker subagent explicitly links them `PRIVATE`.

Behind the curtains, the orchestrator and worker subagents handle all CMake linkage rules and header insulation automatically. Standard CMake `find_package` imported targets work seamlessly alongside `pkg_check_modules`. Worker subagents link imported library targets strictly `PRIVATE` and keep `targets/<name>/<name>/<name>.hpp` completely free of third party headers. Even specialized build pipelines such as code generated Protobuf schema components or custom test harnesses are configured by the orchestrator in a completely hands off manner.

## Mathematical DAG synthesis via the capability contraction algorithm

A signature core capability of Anvil is how the orchestrator synthesizes the physical component graph into a directed acyclic graph. Under John Lakos physical design, a component is a self contained physical unit. It consists of a single public header, a private implementation file, and a colocated test suite. Algorithmic components also include a hardware benchmark suite. A physical component graph is the acyclic dependency structure connecting these isolated components.

Human engineers naturally organize code into conceptual taxonomies like a monolithic algorithms component or a broad utils library. For autonomous AI systems, human taxonomies fail completely. They pull unneeded headers into LLM context windows, serialize worker subagent tasks, and create merge conflicts.

Anvil solves this problem through the anchor constrained capability contraction algorithm. In an agentic workflow, this algorithm creates symmetry between user requirements and physical component architecture. The orchestrator decomposes your requirements into atomic capability operations and decorates each operation with six physical coordinates. These coordinates track execution nature and verification profiles alongside external library bindings. They also record compiler flag regimes, token footprints, and churn volatility.

The anchor constrained capability contraction algorithm groups capabilities into components by solving an optimization problem governed by five hard invariant gates.

* **Quotient graph acyclicity.** The resulting component dependency graph must remain strictly acyclic.
* **Anchor preservation.** Foundational repository anchors like `journal`, `perf_scope`, and `app` must never be merged into other components.
* **Execution and verification parity.** Pure in memory compute kernels are never merged with stateful OS or I/O boundaries. This ensures compute components receive deterministic hardware PMU benchmarks while boundary components stay focused on Lippincott exception firewalls.
* **Compiler regime homogeneity.** Capabilities requiring specialized compiler flags like `-fno-fast-math`, SIMD overrides, or private C++23 features are isolated into their own components.
* **Context locality.** The combined public and private token footprint of a component and its direct upstream headers must not exceed the worker subagent context ceiling $B_{\max} = 16384$.

Within this feasible space, the algorithm minimizes a friction cost function balancing four physical forces.

* **Context waste.** Penalizes pulling unused public functions into downstream callers.
* **Blast radius.** Penalizes deep dependency chains and high churn on shared upstream components.
* **Scaffolding drag.** Prevents trivial component explosion when capabilities naturally belong together.
* **Vendor insulation.** Drives components that wrap external libraries to keep public contracts compact.

The result is a wide, shallow component graph. Because the graph is wide and shallow, the orchestrator can dispatch multiple worker subagents in parallel across isolated Git worktrees with zero merge conflicts.

### Mathematical worker subagent sizing from ACCC coordinates

In Gemini models, higher reasoning budgets generate hidden thinking tokens before every tool call. Because thinking tokens multiply across every turn of an edit, compile, and test loop, oversizing a worker subagent on a simple adapter wastes tokens and increases latency.

Anvil combines five component metrics from the anchor constrained capability contraction algorithm into a deterministic sizing score $\Psi(C_i) \in [0, 1]$ for every component $C_i$.

$$\Psi(C_i) = 0.30 \left(\frac{W(C_i)}{B_{\max}}\right) + 0.30 K(C_i) + 0.20 \min\!\left(1,\, \Theta(C_i)\right) + 0.10 \nu(C_i) + 0.10 \mathbb{I}\!\left(\|\chi(C_i)\|_1 > 0\right)$$

In this equation, $W(C_i) / B_{\max}$ is the context saturation ratio against the $16384$ token ceiling, $K(C_i)$ is empirical churn volatility, $\Theta(C_i)$ is vendor header toxicity load from [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake), $\nu(C_i)$ indicates whether `<name>BENCH` is present, and $\mathbb{I}(\|\chi(C_i)\|_1 > 0)$ indicates specialized local compiler flags. The introspection script [.agents/skills/architect/scripts/sync_manifest.py](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/skills/architect/scripts/sync_manifest.py) computes $\Psi(C_i)$ automatically and maps each component to the `Model` parameter of `invoke_subagent`.

| Sizing score range | `invoke_subagent` `Model` value | Target reasoning profile | Component characteristics |
| :--- | :--- | :--- | :--- |
| $\Psi(C_i) < 0.30$ | `flash_lite` | Minimal thinking budget and fastest execution | Thin glue adapters, small $W(C_i)$, zero vendor toxicity, unit tests only |
| $0.30 \le \Psi(C_i) < 0.70$ | `flash` | Standard fast reasoning tier | Stateful OS boundaries, Lippincott exception firewalls, single vendor library bindings |
| $\Psi(C_i) \ge 0.70$ | `pro` | High reasoning frontier tier | Hot compute kernels with `<name>BENCH` PMU gates, SIMD regimes, multi library insulation, high churn $K(C_i)$ |

Both $\Psi(C_i)$ and the selected `Model` tier are persisted inside `production_artifacts/manifest.json` for every component.

### Living examples versus production decision making

The template provides living example targets in `targets/` to demonstrate physical encapsulation in code.

For Protobuf, the template models the architecture as two components in [item_proto](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/targets/item_proto) and [item_store](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/targets/item_store). This two component structure serves an educational purpose. It proves how a dedicated schema target suppresses compiler warnings on generated code while exporting `.pb.h` headers. It then shows how `item_store` links `item_proto` strictly `PRIVATE` to firewall those vendor headers from the rest of the application.

In production, human engineers should never hand craft or prescribe whether a schema is split or merged. The core philosophy of Anvil is to trust the anchor constrained capability contraction algorithm in production.

### How the algorithm calculates component boundaries

The anchor constrained capability contraction algorithm mathematically decides between a single component and two components by balancing scaffolding drag against blast radius and context waste.

When a schema is consumed by only one operational capability, its consumer fan out is one. In this scenario, splitting into two targets introduces scaffolding drag without reducing blast radius. Because no other component consumes the schema, keeping it in a separate target creates an extra CMake target, an extra directory, and extra build graph edges for zero isolation benefit. Because `item_proto` has a fan out of one in the starter template, `sync_manifest.py` automatically detects `item_proto -> item_store` and records it as a `topology_repartition` candidate inside `production_artifacts/manifest.json` with `user_directive` defaulted to `"ignored"`.

When a schema is consumed by multiple independent capabilities, the fan out is greater than one. Merging the schema into one consumer would force secondary consumers to depend on unrelated logic. That introduces high blast radius and context waste. In this scenario, the cost function heavily penalizes the merged layout. The algorithm automatically extracts a dedicated schema target like `item_proto` and links it privately across all consumers.

## Providing structured requirements

Typing a brief request into a chat box creates the false impression that complex systems architecture can be inferred from a casual sentence. Instead, provide structured requirements that the orchestrator can read. The orchestrator can read a file in your workspace, a ticket in an issue tracker, or a specification page. What matters is that the requirements provide a clear functional foundation.

If you are an experienced C++ engineer, your natural instinct may be to specify low level C++ mechanics such as `std::span` signatures or `noexcept` boundaries. You might also be tempted to prescribe compiler flags or how classes should be split across files. In Anvil, writing low level specifications is counterproductive. The orchestrator and worker subagents already enforce modern C++20 and C++23 idioms, exception firewalls, and hardware optimizations automatically through [.agents/rules/invariants.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/rules/invariants.md). When you step up to a higher level of abstraction and describe what the system must accomplish rather than how to write the C++ syntax, the orchestrator makes significantly better architectural and library choices.

Focus your requirements on four high level areas.

* **External system boundaries and data flow.** Describe where data enters and leaves the application at the OS, storage, or network edge rather than trying to pre-design internal components. Concrete phrases such as *"receive multicast UDP market packets from a socket and decode order book snapshots"*, *"ingest compressed telemetry batches from disk and filter corrupted records"*, or *"publish service health status to systemd"* give the orchestrator exact boundary signals. While these examples illustrate Linux daemon and network services, the same boundary separation applies to GUI event loops or storage backends. From those high level descriptions, the orchestrator automatically separates stateful I/O boundaries from pure in memory compute targets so compute kernels receive deterministic `<name>BENCH` hardware counter harnesses.
* **Domain accuracy and numerical intent.** You cannot call out internal component names or compiler flags in advance because the orchestrator has not designed the component graph yet. Instead, state numerical precision requirements in domain terms when they matter, such as requiring exact decimal rounding or strict IEEE 754 `NaN` and infinity preservation for sensor dropout detection. The orchestrator automatically applies `-fno-fast-math` to whichever internal component implements that math. Likewise, CPU instruction cloning via `target_clones` is strictly an autonomous worker subagent task triggered after hardware benchmarking and never needs to be requested by the user.
* **Candidate third party libraries.** Mention which third party libraries you have added to [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) for major workloads, while allowing the orchestrator to pull in any other registered libraries that fit secondary tasks.
* **Explicit C++ design preferences only when mandatory.** The orchestrator defaults to modern C++ features, strong domain types, and structured flight recorder logging out of the box. State a specific C++ design pattern or error handling convention in your requirements only when you have a strict reason to mandate it.

## Human and orchestrator Git collaboration

In Anvil, Git history is an active input to the mathematical model rather than a passive archive. Following three Git habits keeps the orchestrator, worker subagents, and ACCC metrics synchronized.

* **Hard clean working tree gate before orchestration.** When the orchestrator spawns worker subagents with `Workspace` set to `"share"`, Antigravity branches isolated Git worktrees from `HEAD`. Uncommitted files in your working tree are invisible to those worktrees. Both [.agents/skills/architect/SKILL.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/skills/architect/SKILL.md) and [.agents/skills/performance/SKILL.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/skills/performance/SKILL.md) run `sync_manifest.py --require-clean-git` at Step 1 and refuse to start if `git status --porcelain` is non empty. Always commit your edits to [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) or requirement specifications before starting an orchestration run.
* **Natural atomic commits keep empirical churn $K(C_i)$ accurate.** The introspection script [.agents/skills/architect/scripts/sync_manifest.py](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/skills/architect/scripts/sync_manifest.py) measures component churn volatility $K(C_i)$ from modified file paths in `git log --name-only` over a sliding window of recent commits and ignores bulk commits that touch more than four targets at once. You do not need special commit message prefixes, but keeping manual commits scoped to a single feature or component avoids inflating $K(C_i)$ and prevents simple components from being pushed into higher cost worker subagent tiers.
* **Ad hoc manual edits and the `resync` workflow.** When you edit C++ files or `CMakeLists.txt` manually in an IDE or ask for a quick ad hoc fix outside the `architect` workflow, the lifecycle hook in [.agents/hooks.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/hooks.json) and the Git `pre-commit` hook automatically run `sync_manifest.py` to update `production_artifacts/manifest.json` and check fast mathematical gates $H_1$ through $H_5`. Before handing control back to the orchestrator after manual edits, invoke the `resync` skill in [.agents/skills/resync/SKILL.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/skills/resync/SKILL.md) so dirty `<name>BENCH_run` hardware reports and dual compiler builds are brought back into full parity and committed cleanly.

## Available reports and working alongside IDEs and CI/CD

Anvil is built first and foremost for Google Antigravity where you do not need a manual build terminal or manual code review checklists. Trust the anchor constrained capability contraction algorithm to synthesize component boundaries and delegate implementation loops instead of speculating from human gut feelings.

In this version of Anvil, the system exposes structured reports and records that summarize the state of the repository and surface potential refactorings.

* **Versioned repository manifest and refactor candidates.** Inspect [manifest.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/production_artifacts/manifest.json) to review the authoritative dependency graph `edges`, per component ACCC coordinates, and worker subagent sizing scores $\Psi(C_i)$. The manifest also records invariant gate statuses $H_1$ through $H_5$ and the active `refactor_candidates` array. You should regularly review the JSON records inside `refactor_candidates` for algorithmically discovered refactoring potential rather than relying on manual intuition. Each candidate record is classified under `topology_repartition`, `kernel_acceleration`, `contract_insulation`, or `verification_sync`. Every record is anchored to its discovery Git commit hash via `discovered_at_commit` and controlled by a binary `user_directive` set to `"ignored"` or `"approved"`.
* **Versioned JSON hardware benchmark reports.** Inspect `production_artifacts/profiling/<name>_score_report.json` to review structured nanosecond latencies, CPU cycle counts, and IPC alongside cache miss ratios. Each report also provides hardware bottleneck classifications and a deterministic stopping directive set to `continue_optimizing`, `stop_hardware_saturated`, or `stop_diminishing_returns`.
* **Public error catalogs and contract headers.** Each component maintains a structured error catalog in `targets/<name>/<name>.catalog` and a clean public contract in `targets/<name>/<name>/<name>.hpp` that documents boundary behavior without exposing private implementation details.
* **Prompting for third party dependency opportunities.** Instead of guessing which code path to rewrite, ask the orchestrator directly whether new third party libraries could accelerate any component. For example, prompt *"Are there any additional dependencies that can further improve component performance, and if so what third party library can I add to approved project dependencies?"*

Even though the orchestrator and worker subagents execute builds autonomously inside your Antigravity workspace, Anvil defines all compiler and sanitizer configurations through standard CMake presets in [CMakePresets.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/CMakePresets.json). If you open the repository in a C++ IDE such as CLion or VS Code, the IDE automatically detects [CMakePresets.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/CMakePresets.json) and provides one click shortcuts to launch any build or sanitizer preset. Furthermore, you can configure your remote CI/CD pipeline to run `python3 .agents/skills/architect/scripts/sync_manifest.py --check`, `./production_artifacts/build_all.sh`, and the sanitizer workflow presets in [CMakePresets.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/CMakePresets.json) so remote pull request gates enforce the exact same invariants as local worker subagents.

## Host environment setup

Before starting your first agentic session, verify that your workstation satisfies the [Host prerequisites in README.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/README.md#L25-L33) and unlock Linux kernel PMU counter access so `anvil::perf_scope` can read hardware CPU registers directly.

```bash
sudo sysctl kernel.perf_event_paranoid=1
powerprofilesctl set performance
```
