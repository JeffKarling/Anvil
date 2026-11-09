# Anvil

*'High velocity agentic C++ engineering forged on a strict physical component architecture.'*

**Anvil** adapts the physical component model of **[Target Layout](https://github.com/JeffKarling/Target_Layout)** and the production verification harness of **[Target Layout Extended](https://github.com/JeffKarling/Target_Layout_Extended)** into a zero noise execution environment built exclusively for Google Antigravity.

This project is **opinionated** and only supports a Linux OS and Google Antigravity development environment.

## The more things change, the more they stay the same

Decades ago, John Lakos introduced physical component design to protect human engineers from cognitive overload and compounding coupling. In an era of autonomous AI systems, those foundational principles matter more than ever. Human short term memory has simply been replaced by the LLM context window, and team coordination overhead has become parallel subagent orchestration.

Good architecture is ultimately applied information theory. By strictly bounding how much state an intelligent system must hold in context to make a safe change, **Anvil** turns thirty year old physical design rules into a force multiplier for modern agentic velocity.

## How physical components unlock agentic speed

* **Context window locality.** Strict one to one physical component boundaries allow a worker subagent to implement, test, and benchmark a capability inside a minimal token budget. Worker subagents read only the public interface headers of direct dependencies and never need to load upstream implementations into context.
* **Mathematical DAG partitioning.** The orchestrator translates user requirements and the global dependency palette into capability vectors, then applies the anchor constrained capability contraction algorithm to synthesize wide, shallow component graphs under hard physical invariant gates.
* **Orchestrator and isolated worker subagents.** A context light orchestrator authors public header contracts first and delegates private implementations to short lived worker subagents running in isolated workspaces. The orchestrator tracks optimization progress, detects plateau stalls, and rolls back failed branches automatically.
* **Zero token bloat.** Human tutorials, narrative documentation, and demonstration components are stripped from the active context window. Repository rules are compressed into dense machine invariants and minimal on demand skills that preserve LLM attention for engineering tasks.
* **Mechanical scaffolding and anti reward hacking verification.** Boilerplate build configurations and component layouts are generated deterministically through skill scripts rather than prose instructions. Every component is gated by colocated unit tests, dual compiler static analysis, runtime sanitizers, and automated performance benchmarks.
* **Curated third party composition.** External libraries are declared centrally and linked privately behind clean domain headers. Worker subagents assemble high performance systems by composing approved libraries inside isolated leaf components with zero link time overhead.
* **Production runtime backbone.** The workspace ships with a minimal foundation including lock free flight recorder logging, boundary exception firewalls, structured system log integration, and built in performance benchmarking.

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
