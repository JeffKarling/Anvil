# Trust the algorithm in systems architecture

Human software engineering has historically organized code through narrative taxonomy. Developers split software into conceptual layers like data access tiers, business logic layers, and schema definitions. These divisions feel intuitive to human minds. However, they carry subjective biases that fail when applied to modern AI coding agents.

Anvil abandons narrative taxonomy in favor of objective discrete mathematics. In Anvil, component boundaries are calculated by an optimization algorithm rather than decided by human intuition or markdown checklists.

Understanding why the algorithm recommended a single component for Protocol Buffers reveals the difference between subjective programming and mathematical systems design.

## The illusion of conceptual purity

Traditional software development relies on high level abstractions. When an experienced programmer sees a Protocol Buffers file, their instinct is to create a dedicated schema library. In human thinking, schemas belong in their own conceptual category.

This conceptual taxonomy carries hidden costs. Every physical component introduces scaffolding overhead. A new directory requires its own build targets, export sets, compile options, and test suites.

When software is designed through descriptive prompt rules, language models mimic human cognitive biases. If an agent is given text guidelines instructing it to separate concerns, the agent uncritically fractures the codebase into tiny micro components. Each component appears neat in isolation. Together, they create deep dependency graphs, fragmented context windows, and build system churn.

## The educational paradox in the Anvil template

The Anvil template deliberately retains two components for Protocol Buffers: [targets/item_proto](../../targets/item_proto) and [targets/item_store](../../targets/item_store).

This choice is intentionally paradoxical.

Both targets compile cleanly under Clang and GCC. The component `item_proto` sets `SYSTEM ON` and suppresses warnings on generated code. The component `item_store` links `item_proto` strictly `PRIVATE` and exposes a pure C++ public header. Unit tests pass across both compilers, and hardware benchmarks track execution cycles.

Every line of code is correct according to Lakosian physical design. Yet in this specific topology, creating two components is objectively the wrong architectural choice because the contraction algorithm proves the design should be a single consolidated component.

Anvil includes this two component structure for educational demonstration. It proves that an individually flawless component can still represent an architectural failure in the global graph. The template keeps both targets so developers can observe clean cross component linkage, private vendor insulation, and generated code warning suppression in living code.

In production, human engineers should never subjectively design this boundary. They must trust the Anvil algorithm.

## Why prompt rules produce architectural bloat

Consider what happens when an AI agent designs a system using descriptive markdown documents.

Markdown rules describe abstractions using words. A typical rule document tells the agent to keep schemas independent from storage and decouple data definitions from business logic.

These text rules lack physical resistance. Words cannot measure build graph latency. Prose cannot compute the token tax imposed on downstream subagents. When an agent follows markdown instructions, it creates a separate target because the words suggested a boundary, regardless of whether that boundary serves any actual consumer.

Subjective taxonomies inevitably lead to target explosion. The resulting graph becomes deep and narrow. Deep graphs serialize subagent execution, bloat context windows with transitive headers, and invite merge conflicts. Worse, relying on prose misses out on the compound efficiency gains that a mathematically contracted graph provides through parallel subagent execution and minimal token overhead.

## Mathematical topology over subjective taxonomy

Anvil solves component partitioning through Anchor Constrained Capability Contraction. The orchestrator decomposes system requirements into atomic capability vertices. Each vertex carries six physical coordinates measuring execution nature, verification requirements, external library bindings, compiler flags, token footprint, and churn rate.

The algorithm contracts capability vertices into physical components by solving a constrained optimization problem.

$$F(G) = \sum C_{\text{scaffold}} + \sum C_{\text{waste}} + \sum C_{\text{blast}} + \sum C_{\text{insulate}}$$

The objective function balances four physical forces subject to hard invariant gates.
* **Quotient graph acyclicity.** The physical directed acyclic graph must remain acyclic.
* **Anchor preservation.** Foundational anchors like `journal`, `perf_scope`, and `app` must never merge into other targets.
* **Execution parity.** Pure in memory compute kernels never merge with stateful OS or I/O boundaries.
* **Compiler regime homogeneity.** Targets requiring local flags like `-fno-fast-math` or Protobuf warning suppression are isolated.
* **Context locality.** The combined token footprint of a component and its direct headers must not exceed the subagent context ceiling.

## Proving the single component calculation

The mathematical correctness of the algorithm becomes evident when analyzing the forces on `item_store`.

Suppose the requirements mandate storing structured records to disk using Protocol Buffers. No other component in the system reads or writes this format. The consumer fan out of the schema is exactly one.

Rather than blindly committing to a single predetermined layout, the core intelligence of the algorithm lies in systematically generating and scoring competing topological alternatives. For this capability, it evaluates the split candidate topology against the contracted candidate topology.

### The split two component layout

When the schema is extracted into `item_proto` and consumed by `item_store`, the algorithm evaluates the physical forces.

**Scaffolding drag.** The layout introduces an extra target directory, an extra CMake build file, an additional library target, and extra test scaffolding.

$$C_{\text{scaffold}} > 0$$

**Blast radius and context waste.** Because no other component in the workspace consumes `item_proto`, the fan out is one. Creating a separate target does not isolate any secondary consumer from changes.

$$C_{\text{waste}} = 0, \quad C_{\text{blast}} = 0$$

**Total friction score.** The split layout incurs non zero scaffolding cost while delivering zero reduction in blast radius or context waste.

$$F(\text{split}) = C_{\text{scaffold}} + C_{\text{insulate}}$$

### The merged single component layout

When the `.proto` file is placed directly inside `item_store`, the custom compilation command generates `.pb.h` and `.pb.cc` privately inside the local build directory of `item_store`.

**Scaffolding drag.** Only one target directory, one CMake file, and one test suite exist.

$$C_{\text{scaffold}} = 0$$

**Context waste.** The generated header is never added to any public file set. Downstream callers see only native C++ domain types in `item_store.hpp`. Downstream context waste is zero.

$$C_{\text{waste}} = 0$$

**Blast radius.** No external component links the schema. Changes to the `.proto` definition recompile only `item_store.cpp`.

$$C_{\text{blast}} = 0$$

**Vendor insulation.** Because the generated files exist only inside the private build tree, external components cannot include them. Vendor insulation reaches its theoretical maximum.

$$F(\text{merged}) < F(\text{split})$$

The mathematical optimization function proves that merging the schema into a single component yields a strictly lower friction score.

## When the mathematics demand a split

The algorithm is never dogmatic. If the system requirements change, the mathematical forces change immediately.

Suppose a new requirement introduces a high speed network ingestion component that receives the same Protocol Buffers packets over UDP. Now two independent components consume the schema. The consumer fan out is two.

If the schema were merged into `item_store`, the networking component would be forced to depend on `item_store`. That dependency introduces severe context waste and pulls unrelated storage logic into the networking subagent.

$$C_{\text{waste}} \gg 0, \quad C_{\text{blast}} \gg 0$$

In that topology, the penalty for context waste and blast radius exceeds the cost of scaffolding drag.

$$F(\text{merged}) > F(\text{split})$$

The optimization algorithm automatically contracts the schema into a dedicated `item_proto` target and fans out private edges to both `item_store` and the networking component.

The decision is entirely mathematical. No human convention, architectural committee, or subjective prompt rule was required.

## Strategic architecture versus tactical implementation

This distinction highlights the division of labor in agentic systems development.

Strategic architecture belongs to discrete mathematics. The orchestrator synthesizes the global directed acyclic graph by minimizing physical friction across invariant gates. It constructs a wide, shallow graph optimized for subagent independence.

Tactical implementation belongs to short lived worker agents. Once the strategic manager locks the component vertices, individual subagents implement private translation units inside isolated workspaces. Each worker focuses strictly on its assigned target and direct upstream public contracts.

By substituting subjective narrative taxonomies with mathematical capability contraction, Anvil ensures that system architecture remains deterministic, objective, and verified.
