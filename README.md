# Anvil

*'High velocity agentic C++ engineering forged on a strict physical component architecture.'*

Anvil adapts the physical component model of [Target Layout](https://github.com/JeffKarling/Target_Layout) and the verification harness of [Target Layout Extended](https://github.com/JeffKarling/Target_Layout_Extended) into a zero noise execution environment built exclusively for Google Antigravity.

This project is opinionated and supports only a Linux OS and Google Antigravity development environment.

## The more things change, the more they stay the same

Decades ago, John Lakos introduced physical component design to protect human engineers from cognitive overload and compounding coupling. In an era of autonomous AI systems, those foundational principles matter more than ever. Human short term memory has simply been replaced by the LLM context window. Team coordination overhead has become parallel subagent orchestration.

Good architecture is ultimately applied information theory. By strictly bounding how much state an intelligent system must hold in context to make a safe change, Anvil turns thirty year old physical design rules into a force multiplier for modern agentic velocity.

## How physical components unlock agentic speed

* **Context window locality.** Strict one to one physical component boundaries allow a worker subagent to implement, test, and benchmark a capability inside a minimal token budget. Worker subagents read only the public interface headers of direct dependencies. They never load upstream implementations into context.
* **Mathematical DAG partitioning.** The orchestrator translates user requirements and the global dependency palette into capability vectors. It applies the anchor constrained capability contraction algorithm to synthesize wide, shallow component graphs under hard physical invariant gates.
* **Deterministic monitor and worker subagents.** A lightweight monitor supervisor coordinates strategic and tactical workers while gating progress with verifiers. Workers author clean contracts and implement private code in isolated shared worktrees.
* **Zero token bloat.** Human tutorials, narrative documentation, and demonstration components are stripped from the active context window. Repository rules are compressed into dense machine invariants and minimal on demand skills that preserve LLM attention for engineering tasks.
* **Mechanical scaffolding and adversarial verification.** Boilerplate build configurations and component layouts are generated deterministically through skill scripts. Every component is gated by colocated unit tests, dual compiler static analysis, runtime sanitizers, and automated performance benchmarks.
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

## Documentation directory

### Engineering manuals and prompt cookbooks

* **[General engineering manual](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/MANUAL.md).** Comprehensive systems manual covering ACCC mathematical graph synthesis, invariant gates $H_1$ through $H_5$, worker sizing scores $\Psi$, and dependency insulation.
* **[Human prompt cookbook and workflows](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/guides/prompts.md).** Tested prompt templates and workflows for greenfield project bootstrap, senior developer refactor review, hardware PMU benchmarking, and ad hoc git resynchronization.
* **[Anvil Template](https://github.com/JeffKarling/AnvilTemplate).** Cleaned starter blueprint stripped of exemplar components and documentation, preserving only the root prompt cheat sheet.

### Deep dive architectural articles

* **[Trust the algorithm in systems architecture](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/articles/trust_the_algorithm.md).** Discrete mathematical partitioning versus human narrative taxonomy in AI system design.
* **[The Protobuf pedagogic example](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/articles/protobuf_pedagogic_example.md).** Case study demonstrating why splitting single consumer schemas causes scaffolding drag.
* **[Verification philosophy in agentic physical design](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/articles/tactical_and_strategic_verifiers.md).** Adversarial verification, independent auditors, and preventing reward hacking in parallel subagents.
* **[Compiler boundaries over prompt rule bloat](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/articles/compiler_boundaries_over_prompt_rules.md).** Replacing fragile prompt rules with physical compiler walls while adapting to accelerating model release velocity.
* **[How Anvil verifiers compare to Swarm](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/articles/how_anvils_verifiers_compare_to_swarm.md).** Physical target verification versus shared conversational feeds in multi agent systems.
* **[The 16384 token ceiling in physical component design](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/doc/articles/the_16384_token_ceiling.md).** Information theory, attention degradation, and binary power sizing in agentic context windows.

## License

Licensed under [MIT-0](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/LICENSE).
