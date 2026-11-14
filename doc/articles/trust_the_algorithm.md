# Trust the algorithm in systems architecture

Human software engineering has historically organized code through narrative taxonomy. Developers split software into conceptual layers like data access tiers and business logic layers. These divisions feel intuitive to human minds. However, they carry subjective biases that fail when applied to modern AI coding agents.

Anvil abandons narrative taxonomy in favor of discrete mathematics. Component boundaries are calculated by an optimization algorithm rather than decided by human intuition. Throughout a project lifecycle, the algorithm remains the ultimate authority on how the physical dependency graph is shaped.

## The illusion of conceptual purity

Traditional software development relies on high level conceptual categories. Experienced engineers partition systems by domain labels like schemas or core libraries. Each bucket feels tidy to a human reader regardless of how callers actually use the code.

This conceptual taxonomy carries hidden physical costs. Every component boundary changes compiler visibility and header exposure. It also changes build graph depth. What looks neat in a conceptual diagram often creates needless scaffolding drag or tangled coupling in real builds.

Left to subjective labels, language models mimic human cognitive biases. Prose cannot measure build latency or token overhead. Without quantitative constraints, agents drift away from physical reality.

## Ways subjective rules fail at component design

Subjective taxonomies fail in two opposite directions.

When guidelines instruct an agent to decouple layers, the agent creates excessive components simply because words suggest a boundary. That path produces needless fragmentation with deep graphs that serialize subagent execution.

When code is grouped into broad buckets like a catch all utility library, the opposite failure occurs. Throwing unrelated capabilities into one coarse component erodes safety. It mixes pure compute with stateful I/O and exposes vendor headers across boundaries. It also forces developers into indirection workarounds like service locators and dynamic registries.

Healthy component boundaries require ongoing mathematical adjustments as requirements shift. Anvil continuously evaluates the live graph in [manifest.json](../../production_artifacts/manifest.json) to record deterministic refactoring telemetry.

## Mathematical topology over subjective taxonomy

Anvil solves component partitioning through Anchor Constrained Capability Contraction. The system decomposes requirements into atomic capability vertices. Each vertex carries execution coordinates and compiler regimes alongside token footprints.

The algorithm contracts capability vertices into physical components by solving a constrained optimization problem.

$$F(G) = \sum C_{\text{scaffold}} + \sum C_{\text{waste}} + \sum C_{\text{blast}} + \sum C_{\text{insulate}}$$

The objective function balances four physical forces subject to hard invariant gates.

* **Quotient graph acyclicity.** The physical directed acyclic graph must remain acyclic.
* **Anchor preservation.** Foundational anchors like `journal` and `app` must never merge into other components.
* **Execution parity.** Pure in memory compute kernels never merge with stateful OS or I/O boundaries.
* **Compiler regime homogeneity.** Components requiring specialized local flags are isolated.
* **Context locality.** The combined token footprint of a component and its direct headers must not exceed the context ceiling of sixteen thousand tokens.

Scaffolding drag $C_{\text{scaffold}}$ penalizes pointless micro splits. At the same time, context waste $C_{\text{waste}}$ and blast radius $C_{\text{blast}}$ punish oversized components.

## Strategic architecture versus tactical implementation

This distinction defines the division of labor in agentic systems development.

Strategic architecture belongs to discrete mathematics. The orchestrator synthesizes the global directed acyclic graph by minimizing physical friction across invariant gates. It constructs a wide and shallow graph optimized for subagent independence.

Tactical implementation belongs to short lived worker agents. Once the strategic manager locks the component vertices, individual subagents implement private translation units inside isolated workspaces. Each worker focuses strictly on its assigned component and direct upstream public contracts.
