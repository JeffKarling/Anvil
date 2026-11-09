# Anvil

*'High velocity agentic C++ engineering forged on a strict physical component architecture.'*

**Anvil** adapts the physical component model of **[Target Layout](https://github.com/JeffKarling/Target_Layout)** and the production verification harness of **[Target Layout Extended](https://github.com/JeffKarling/Target_Layout_Extended)** into a zero noise execution environment built exclusively for Google Antigravity.

This project is **opinionated** and only supports a Linux OS and Google Antigravity development environment.

## The more things change, the more they stay the same

Decades ago, John Lakos introduced physical component design to protect human engineers from cognitive overload and compounding coupling. In an era of autonomous AI agents, those foundational principles matter more than ever. Human short term memory has simply been replaced by the LLM context window, and team coordination overhead has become parallel subagent orchestration.

Good architecture is ultimately applied information theory. By strictly bounding how much state an intelligent system must hold in context to make a safe change, **Anvil** turns thirty year old physical design rules into a force multiplier for modern agentic velocity.

## How physical components unlock agentic speed

* **Context window locality.** Strict one to one physical component boundaries allow an agent to implement, test, and benchmark a capability inside a minimal token budget. Agents read only public interface headers of direct dependencies and never need to load upstream implementations into context.
* **Mathematical DAG partitioning.** Lead architect agents translate user requirements and the global dependency palette into capability vectors, then apply anchor constrained capability contraction to synthesize wide, shallow component graphs under hard physical invariant gates.
* **Strategic manager and isolated tactical workers.** A context light strategic manager authors public header contracts first and delegates private implementations to short lived tactical workers running in isolated Git worktrees via Antigravity subagents. The manager tracks search tree progress, detects plateau stalls, and rolls back poisoned branches.
* **Zero token bloat.** Human tutorials, narrative documentation, and demonstration components are stripped from the active agent context. Repository rules are compressed into dense machine invariants and minimal on demand skills that preserve LLM attention for engineering tasks.
* **Mechanical scaffolding and anti reward hacking verification.** Boilerplate CMake configurations and component layouts are generated deterministically through skill scripts rather than prose instructions. Every component is gated by colocated unit tests, dual compiler static analysis, and runtime sanitizers. Hot path components are further verified by hardware PMU counter benchmarks via `perf_scope`.
* **Curated third party composition.** External libraries are declared centrally in `cmake/dependencies.cmake` and linked privately behind clean domain headers. Agents assemble high performance systems by composing approved libraries inside isolated leaf components with zero link time overhead under LTO.
* **Production runtime backbone.** The workspace ships with a minimal foundation including lock free flight recorder logging and Lippincott boundary exception firewalls. It also provides systemd journald integration and hardware performance counter gates.

## Host prerequisites

* Linux kernel with `perf_event_paranoid <= 1`
* CMake `>= 3.25` and `ninja` alongside `pkg-config` and `ccache`
* `clang++` and `g++` with `libstdc++exp` for C++20 and C++23 standard library support
* Static analysis tools `clang-tidy`, `cppcheck`, and `include-what-you-use`
* Profiling tool `perf`
* Core test discovery framework GoogleTest via CMake or PkgConfig
* Exemplar libraries in [cmake/dependencies.cmake](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/cmake/dependencies.cmake) for template starter components, including `libsystemd` for `journal` and sample packages `protobuf` and `tbb`

## Human engineering manual and architectural lineage

Human engineers should read **[MANUAL.md](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/MANUAL.md)** for best practices on directing Anvil inside Google Antigravity. The manual explains how to curate third party libraries, write high level requirements specifications, and collaborate with the orchestrator across Git commits.

To understand the foundational physical layout rules, visit **[Target Layout](https://github.com/JeffKarling/Target_Layout)**. For deep architectural rationale and enterprise patterns, visit the **[Target Layout Extended documentation](https://jeffkarling.github.io/Target_Layout_Extended/)**.

## License

Licensed under [MIT-0](LICENSE).
