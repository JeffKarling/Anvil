# Trust the algorithm in systems architecture

Human software engineering has historically organized code through narrative taxonomy. Developers split software into conceptual layers like data access tiers, business logic layers, and schema definitions. These divisions feel intuitive to human minds. However, they carry subjective biases that fail when applied to modern AI coding agents.

Anvil abandons narrative taxonomy in favor of objective discrete mathematics. Component boundaries are calculated by an optimization algorithm rather than decided by human intuition or static markdown checklists. Throughout a project lifecycle, the algorithm remains the ultimate authority on how the physical dependency graph is shaped.

For a worked walkthrough using the starter repository's Protocol Buffers targets, read **[The Protobuf pedagogic example](protobuf_pedagogic_example.md)**.

## The illusion of conceptual purity

Traditional software development relies on high level conceptual abstractions. Experienced engineers tend to partition systems by domain labels such as schemas, utilities, or core libraries. Each bucket feels tidy to a human reader regardless of how callers actually use the code.

This conceptual taxonomy carries hidden physical costs. Every component boundary changes compiler visibility, header exposure, and build graph depth. What looks neat in a conceptual diagram often creates either needless scaffolding drag or tangled coupling in real builds.

When software is designed through descriptive prompt rules, language models mimic these human cognitive biases. Prose cannot measure build latency, token overhead, or fault blast radius. Left to subjective labels, agents drift away from physical reality.

## Ways human written rules fail at component design

Consider what happens when AI agents design a system using human written descriptive markdown documents instead of math based constraints. Markdown rules describe abstractions using words rather than physical boundaries. Because prose has no quantitative threshold, subjective taxonomies fail in two opposite directions.

When prose based guidelines instruct an agent to separate concerns and decouple layers, the agent creates targets simply because the words suggest a boundary. Words cannot measure build graph latency or compute the token tax imposed on downstream subagents. That path produces unnecessary fragmentation with deep, narrow graphs that serialize subagent execution and churn the build system.

When code is grouped into broader buckets like a catch all `lib` or `game_physics`, the opposite failure occurs. Throwing unrelated capabilities into one coarse target hinders both velocity and safety as proven by Lakosian analysis. Parallel subagents collide inside the same directory, and worker context windows fill with irrelevant code. Coarse targets also erode safety by mixing pure compute with stateful I/O and blending incompatible compiler flags. They expose vendor headers across boundaries and widen the blast radius of every fault.

Coarse libraries also force developers into harder after the fact C++ designs. When unrelated subsystems like rendering and physics live inside one oversized library, deeply nested helpers eventually need access to distant state. Passing those dependencies down through every intermediate constructor creates tramp data that pollutes unrelated interfaces. To avoid threading parameters through every layer, engineers reach for complex workarounds like service locators and hidden global registries. Others adopt runtime dependency injection frameworks or wrapper objects holding back pointers into foreign subsystems. That accidental complexity disappears when components stay small and bounded. In a graph of shallow physical targets, each component receives its exact dependencies at the boundary so new features stay straightforward C++ rather than indirection machinery.

Healthy component boundaries are never a one time setup. Component selection and the DAG require ongoing adjustments throughout a project lifecycle as requirements shift. Humans rarely refactor component boundaries by hand because restructuring targets and headers across a live build graph is slow and error prone. Instead, teams patch aging coarse libraries with advanced C++ indirection to work around passing an oversized subsystem into a small consumer.

Anvil makes continuous architectural refactoring practical through ongoing algorithmic calculations using pure mathematics. Throughout the project lifecycle, the system continuously evaluates the live graph in [production_artifacts/manifest.json](../../production_artifacts/manifest.json) and records deterministic merge, split, and insulation telemetry notes so strategic and tactical workers can weigh structural net gain against rework cost as requirements evolve.

## Mathematical topology over subjective taxonomy

Anvil solves component partitioning through Anchor Constrained Capability Contraction. The orchestrator decomposes system requirements into atomic capability vertices. Each vertex carries six physical coordinates tracking execution nature, verification profile, and external library bindings. Those coordinates also record local compiler flags, token footprint, and churn rate.

The algorithm contracts capability vertices into physical components by solving a constrained optimization problem.

$$F(G) = \sum C_{\text{scaffold}} + \sum C_{\text{waste}} + \sum C_{\text{blast}} + \sum C_{\text{insulate}}$$

The objective function balances four physical forces subject to hard invariant gates.
* **Quotient graph acyclicity.** The physical directed acyclic graph must remain acyclic.
* **Anchor preservation.** Foundational anchors like `journal`, `perf_scope`, and `app` must never merge into other targets.
* **Execution parity.** Pure in memory compute kernels never merge with stateful OS or I/O boundaries.
* **Compiler regime homogeneity.** Targets requiring specialized local flags such as `-fno-fast-math` or generated code warning suppression are isolated.
* **Context locality.** The combined token footprint of a component and its direct headers must not exceed the subagent context ceiling.

The objective function and invariant gates guard against both extremes. Scaffolding drag $C_{\text{scaffold}}$ penalizes pointless micro splits when consumer fan out is one. At the same time, context waste $C_{\text{waste}}$ and blast radius $C_{\text{blast}}$ punish oversized targets. Vendor insulation $C_{\text{insulate}}$ pairs with execution parity and compiler regime homogeneity under the 16384 token context ceiling. Those constraints forbid collapsing unrelated code into a coarse `lib`.

## Strategic architecture versus tactical implementation

This distinction defines the division of labor in agentic systems development.

Strategic architecture belongs to discrete mathematics. The orchestrator synthesizes and continuously maintains the global directed acyclic graph by minimizing physical friction across invariant gates. It constructs a wide, shallow graph optimized for subagent independence and adapts that topology whenever new requirements arrive.

Tactical implementation belongs to short lived worker agents. Once the strategic manager locks the component vertices, individual subagents implement private translation units inside isolated workspaces. Each worker focuses strictly on its assigned target and direct upstream public contracts.

By substituting subjective narrative taxonomies with continuous mathematical capability contraction, Anvil keeps system architecture deterministic and verified throughout the lifecycle of the codebase.
