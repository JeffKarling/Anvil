# Anvil human engineering manual

Anvil is an agentic C++ project blueprint designed for modern AI coding environments like Antigravity, Claude Code, or Cursor. In this workflow, an experienced C++ engineer stops writing implementation code by hand. Instead of typing boilerplate or running manual compiler loops, you author high level system requirements and curate third party libraries. You then read the clean component code produced by the agents and inspect test and benchmark reports.

As a template, Anvil configures a portable C++20 baseline across all components in [target_properties.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/templates/target_properties.cmake) so public interfaces remain minimal and standard. New components created by the orchestrator default to this clean C++20 baseline. The template also provides exemplar foundation components like [journal](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/targets/journal/CMakeLists.txt) to demonstrate private C++23 adoption. For example, `journal` uses `std::views::enumerate` and `std::stacktrace` behind its private translation unit without leaking C++23 requirements to upstream callers.

## Built in subagent orchestration and division of labor

Anvil includes automated multi agent orchestration as a core built in capability. You never manually spawn, coordinate, or micromanage worker subagents. You interact strictly with the top level orchestrator while the framework manages subagent delegation behind the scenes.

* **Human responsibilities.** You provide structured requirements and curate the global third party library palette in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake). Once the agents finish, you review the generated public contracts in `targets/<name>/<name>/<name>.hpp` and inspect the verification and profiling reports. The orchestrator operates on a best effort basis by analyzing proven third party algorithms and capturing an initial hardware baseline automatically. In day to day work, you can simply tell the agent that an application section feels slow and add a faster library such as Intel MKL to [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) that enables the orchestrator to improve it. Explicit latency numbers are only needed where a hard deadline is known in advance.
* **Orchestrator responsibilities.** The strategic manager reads your requirements and [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake). It partitions the system into a directed acyclic graph of physical components, or DAG. It scaffolds public header contracts and automatically dispatches parallel tactical subagents.
* **Tactical subagent responsibilities.** Short lived worker subagents are launched automatically by the orchestrator inside isolated Git worktrees. Each delegated subagent reads only its assigned component directory and direct upstream public headers to write the private `.cpp` implementation. It then verifies unit tests, sanitizers, and hardware PMU counters before reporting back to the orchestrator.

## Provisioning third party libraries as a capability multiplier

The highest leverage action you can take before starting a feature is populating [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) with a rich selection of vetted third party libraries.

When the orchestrator translates your requirements, it checks every needed capability against the libraries available in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake). When a matching library is available, the orchestrator uses it and delegates a tactical subagent to write a compact multi line private adapter around that library. When no suitable library is registered, the subagent is forced to write bespoke C++ algorithms from scratch. Bespoke code consumes far more context tokens, takes more optimization iterations, and carries a larger surface for subtle bugs.

Because Anvil enables link time optimization via `ENABLE_IPO=ON` in release builds and links third party targets strictly `PRIVATE` inside leaf components, registering extra candidate libraries in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) adds zero binary bloat to components that do not use them. You do not need to decide in advance which exact library every internal component will use. The more high quality libraries you expose in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake), the better the orchestrator can assemble a fast, reliable application.

### Example third party library expansion

Declare external packages globally in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) using standard CMake `find_package` or `pkg_check_modules`. Below are example libraries across common systems domains that give the orchestrator strong building blocks.

* **Serialization and schema generation.** Provision binary schema tools like `protobuf`, `flatbuffers`, and `capnproto`. Add structured parsers like `simdjson`, `yyjson`, or `sd_json` from `libsystemd` so subagents build zero copy parsers without hand written state machines.
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

All entries in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) use `QUIET` discovery by default. This minimizes configuration noise and allows a greenfield project to initialize and run even when nothing exists in the repository apart from a `main` function. Listing a library with `QUIET` signals to the architect that the dependency is pre approved for use. If the architect selects an approved library that is not yet installed on the host, the agent can install it or update the build configuration on demand. Conversely, when you explicitly change a dependency to `REQUIRED`, that serves as a strong directive telling the architect that the library must be enabled and integrated into the design. Inspecting the compiled `targets/app/app` binary with `ldd` confirms that unlinked targets in this palette contribute zero shared library dependencies and zero binary bytes until a subagent explicitly links them `PRIVATE`.

Behind the curtains, the orchestrator and its subagents handle all CMake linkage rules and header insulation automatically. Standard CMake `find_package` imported targets work seamlessly alongside `pkg_check_modules`. Subagents link imported library targets strictly `PRIVATE` and keep `targets/<name>/<name>/<name>.hpp` completely free of third party headers. Even specialized build pipelines such as code generated Protobuf schema components or custom test harnesses are configured by the orchestrator in a completely hands off manner.

## Mathematical DAG synthesis via capability contraction

A signature core capability of Anvil is how the orchestrator synthesizes the physical component graph into a directed acyclic graph. Under John Lakos physical design, a component is a self contained physical unit. It consists of a single public header, a private implementation file, and a colocated test suite. Algorithmic components also include a hardware benchmark suite. A physical component graph is the acyclic dependency structure connecting these isolated components.

Human engineers naturally organize code into conceptual taxonomies like a monolithic algorithms component or a broad utils library. For autonomous AI agents, human taxonomies fail completely. They pull unneeded headers into LLM context windows, serialize subagent tasks, and create merge conflicts.

Anvil solves this problem through an algorithm called Anchor Constrained Capability Contraction. In an agentic workflow, this algorithm creates symmetry between user requirements and physical component architecture. The orchestrator decomposes your requirements into atomic capability operations and decorates each operation with six physical coordinates. These coordinates track execution nature and verification profiles alongside external library bindings. They also record compiler flag regimes, token footprints, and churn volatility.

The algorithm groups capabilities into components by solving an optimization problem governed by five hard invariant gates.

* **Quotient graph acyclicity.** The resulting component dependency graph must remain strictly acyclic.
* **Anchor preservation.** Foundational repository anchors like `journal`, `perf_scope`, and `app` must never be merged into other components.
* **Execution and verification parity.** Pure in memory compute kernels are never merged with stateful OS or I/O boundaries. This ensures compute components receive deterministic hardware PMU benchmarks while boundary components stay focused on Lippincott exception firewalls.
* **Compiler regime homogeneity.** Capabilities requiring specialized compiler flags like `-fno-fast-math`, SIMD overrides, or private C++23 features are isolated into their own components.
* **Context locality.** The combined public and private token footprint of a component and its direct upstream headers must not exceed the tactical worker context ceiling.

Within this feasible space, the algorithm minimizes a friction cost function balancing four physical forces.

* **Context waste.** Penalizes pulling unused public functions into downstream callers.
* **Blast radius.** Penalizes deep dependency chains and high churn on shared upstream components.
* **Scaffolding drag.** Prevents trivial component explosion when capabilities naturally belong together.
* **Vendor insulation.** Drives components that wrap external libraries to keep public contracts compact.

The result is a wide, shallow component graph. Because the graph is wide and shallow, the orchestrator can dispatch multiple tactical subagents in parallel across isolated Git worktrees with zero merge conflicts.

### Living examples versus production decision making

The template provides living example targets in `targets/` to demonstrate physical encapsulation in code.

For Protobuf, the template models the architecture as two components: [item_proto](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/targets/item_proto) and [item_store](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/targets/item_store). This two component structure serves an educational purpose. It proves how a dedicated schema target suppresses compiler warnings on generated code while exporting `.pb.h` headers. It then shows how `item_store` links `item_proto` strictly `PRIVATE` to firewall those vendor headers from the rest of the application.

In production, human engineers should never hand craft or prescribe whether a schema is split or merged. The core philosophy of Anvil is to trust the algorithm in production. The agent evaluates the capability graph through the contraction algorithm and makes the optimal determination autonomously.

### How the algorithm calculates component boundaries

The contraction algorithm mathematically decides between a single component and two components by balancing scaffolding drag against blast radius and context waste.

When a schema is consumed by only one operational capability, its consumer fan out is one. In this scenario, splitting into two targets introduces scaffolding drag without reducing blast radius. Because no other component consumes the schema, keeping it in a separate target creates an extra CMake target, an extra directory, and extra build graph edges for zero isolation benefit. The cost function determines that the merged single component layout has a lower total friction score. The algorithm therefore consolidates the `.proto` compilation directly into the private translation unit of the consumer.

When a schema is consumed by multiple independent capabilities, the fan out is greater than one. Merging the schema into one consumer would force secondary consumers to depend on unrelated logic. That introduces high blast radius and context waste. In this scenario, the cost function heavily penalizes the merged layout. The algorithm automatically extracts a dedicated schema target like `item_proto` and links it privately across all consumers.

## Providing structured requirements

Typing a brief request into a chat box creates the false impression that complex systems architecture can be inferred from a casual sentence. Instead, provide structured requirements that the agent can read. An agent can read a file in your workspace, a ticket in an issue tracker, or a specification page. What matters is that the requirements provide a clear functional foundation.

If you are an experienced C++ engineer, your natural instinct may be to specify low level C++ mechanics such as `std::span` signatures or `noexcept` boundaries. You might also be tempted to prescribe compiler flags or how classes should be split across files. In Anvil, writing low level specifications is counterproductive. The orchestrator and tactical subagents already enforce modern C++20 and C++23 idioms, exception firewalls, and hardware optimizations automatically through [.agents/rules/invariants.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/rules/invariants.md). When you step up to a higher level of abstraction and describe what the system must accomplish rather than how to write the C++ syntax, the orchestrator makes significantly better architectural and library choices.

Focus your requirements on four high level areas.

* **External system boundaries and data flow.** Describe where data enters and leaves the application at the OS, storage, or network edge rather than trying to pre-design internal components. Concrete phrases such as *"receive multicast UDP market packets from a socket and decode order book snapshots"*, *"ingest compressed telemetry batches from disk and filter corrupted records"*, or *"publish service health status to systemd"* give the architect exact boundary signals. While these examples illustrate Linux daemon and network services, the same boundary separation applies to GUI event loops or storage backends. From those high level descriptions, the architect automatically separates stateful I/O boundaries from pure in memory compute targets so compute kernels receive deterministic `<name>BENCH` hardware counter harnesses.
* **Domain accuracy and numerical intent.** You cannot call out internal component names or compiler flags in advance because the orchestrator has not designed the component graph yet. Instead, state numerical precision requirements in domain terms when they matter, such as requiring exact decimal rounding or strict IEEE 754 `NaN` and infinity preservation for sensor dropout detection. The orchestrator automatically applies `-fno-fast-math` to whichever internal component implements that math. Likewise, CPU instruction cloning via `target_clones` is strictly an autonomous subagent task triggered after hardware benchmarking and never needs to be requested by the user.
* **Candidate third party libraries.** Mention which third party libraries you have added to [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) for major workloads, while allowing the orchestrator to pull in any other registered libraries that fit secondary tasks.
* **Explicit C++ design preferences only when mandatory.** The architect defaults to modern C++ features, strong domain types, and structured flight recorder logging out of the box. State a specific C++ design pattern or error handling convention in your requirements only when you have a strict reason to mandate it.

## Working with AI coding agents alongside IDEs and CI/CD

Anvil is built first and foremost for agentic workflows where you do not need a built in CMake preset launcher or manual build terminal. You simply tell the agent to architect from requirements, implement a feature, or optimize a slow path. The orchestrator and its subagents invoke all underlying CMake workflows, unit tests, and hardware PMU benchmarks autonomously.

Your workflow as the human engineer centers on reviewing four artifacts produced by the agents.

* **Public contracts and implementation code.** Read `targets/<name>/<name>/<name>.hpp` to verify clean domain interfaces and inspect `targets/<name>/<name>.cpp` when reviewing implementation logic.
* **Public catalog error definitions.** Read `targets/<name>/<name>.catalog` to inspect documented failure reasons and boundary error contracts without needing to read private source code.
* **Physical dependency graph.** Open `production_artifacts/graphviz/project.svg` in any viewer or browser to inspect the visual component DAG synthesized by the architect.
* **Hardware benchmark and test reports.** Read `production_artifacts/profiling/<name>_score_report.md` to review measured nanosecond latencies, CPU cycle counts, and IPC alongside cache misses. Each report also records a deterministic stopping directive such as `continue_optimizing`, `stop_hardware_saturated`, or `stop_diminishing_returns`.

Even though agents execute builds autonomously inside your agentic workspace, Anvil defines all compiler and sanitizer configurations through standard CMake presets in [CMakePresets.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/CMakePresets.json). This gives you two major advantages outside the agent loop. If you open the repository in a modern C++ IDE such as CLion or VS Code to browse code, the IDE automatically detects [CMakePresets.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/CMakePresets.json) and provides one click shortcuts to launch any build or sanitizer preset. Furthermore, you should configure your remote CI/CD pipeline to run `./production_artifacts/build_all.sh` and the sanitizer workflow presets in [CMakePresets.json](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/CMakePresets.json) so remote pull request gates enforce the exact same invariants as local subagents.

## Host environment setup

Before starting your first agentic session, verify that your workstation satisfies the [Host prerequisites in README.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/README.md#L25-L33) and unlock Linux kernel PMU counter access so `anvil::perf_scope` can read hardware CPU registers directly.

```bash
sudo sysctl kernel.perf_event_paranoid=1
powerprofilesctl set performance
```
