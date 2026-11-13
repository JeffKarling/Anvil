# The Protobuf pedagogic example

Anvil abandons narrative taxonomy in favor of discrete mathematics. In Anvil, component boundaries are calculated by an optimization algorithm rather than decided by human intuition or markdown checklists.

Understanding why the algorithm recommends a single component for Protocol Buffers shows this principle in concrete code. The starter repository ships with a deliberate contradiction so developers can inspect both the mechanics of vendor isolation and the mathematical proof that favors a simpler graph.

## The illusion of conceptual purity

Traditional software development relies on intuitive conceptual categories. When an experienced programmer sees a Protocol Buffers file, their instinct is to create a dedicated schema library. In human thinking, schemas belong in their own layer separate from storage logic.

This conceptual taxonomy carries hidden costs. Every physical component introduces scaffolding overhead. A new directory requires its own build targets and export sets alongside separate compile options and test suites.

## The educational paradox in the Anvil template

The Anvil template deliberately retains two components for Protocol Buffers in [targets/item_proto](../../targets/item_proto) and [targets/item_store](../../targets/item_store).

This choice is intentionally paradoxical and serves as an educational demonstration.

Both targets compile cleanly under Clang and GCC. The component `item_proto` sets `SYSTEM ON` and suppresses warnings on generated code. The component `item_store` links `item_proto` strictly `PRIVATE` and exposes a pure C++ public header. Unit tests pass across both compilers, and hardware benchmarks track execution cycles.

Every line of code is correct according to Lakosian physical design. Yet in this specific topology, creating two components is objectively the wrong architectural choice. The Anvil contraction algorithm proves the design should be a single consolidated component because the relative costs of establishing and maintaining a new target outweigh the marginal benefit of extra isolation.

Anvil includes this suboptimal two component structure for educational demonstration. It proves that an individually flawless component can still represent an architectural failure in the global graph. The project keeps both targets so developers can observe clean cross component linkage, private vendor insulation, and generated code warning suppression in live code.

Leaving this split unoptimized in the initial starter commit also demonstrates Anvil's automated refactor telemetry in [production_artifacts/manifest.json](../../production_artifacts/manifest.json). When the manifest generator inspects the graph, it flags `item_proto` and `item_store` inside `refactor_candidates` under `REF-TOPO-item_proto-item_store`. That JSON entry records a `topology_repartition` advisory note with a summary explaining that `item_proto` has a consumer fan out of one and that merging both targets eliminates scaffolding drag with a positive `net_gain`. The starter repository is committed as a frozen snapshot prior to running an autonomous refactor wave so developers can inspect the raw telemetry in `manifest.json`.

This Protobuf example illustrates that engineers should trust the Anvil algorithm instead of subjectively designing component boundaries. Automated mathematical partitioning protects project velocity, stability, and performance.

## Proving the single component calculation

The mathematical correctness of the algorithm becomes clear when analyzing the physical forces on `item_store` under Anchor Constrained Capability Contraction.

$$F(G) = \sum C_{\text{scaffold}} + \sum C_{\text{waste}} + \sum C_{\text{blast}} + \sum C_{\text{insulate}}$$

Suppose the requirements mandate storing structured records to disk using Protocol Buffers. No other component in the system reads or writes this format. The consumer fan out of the schema is exactly one.

Rather than committing blindly to a single layout, the algorithm generates and scores competing topological alternatives. For this capability, it evaluates the split two component layout against the merged single component layout.

### The split two component layout

When the schema is extracted into `item_proto` and consumed by `item_store`, the algorithm evaluates the physical forces.

**Scaffolding drag.** The layout introduces an extra target directory and CMake build file along with an additional library target and test scaffolding.

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

The optimization function proves that merging the schema into a single component yields a strictly lower friction score.

## When the mathematics demand a split

The algorithm is never dogmatic. If the system requirements change, the mathematical forces change immediately.

Suppose a new requirement introduces a high speed network ingestion component that receives the same Protocol Buffers packets over UDP. Now two independent components consume the schema. The consumer fan out is two.

If the schema were merged into `item_store`, the networking component would be forced to depend on `item_store`. That dependency introduces severe context waste and pulls unrelated storage logic into the networking subagent.

$$C_{\text{waste}} \gg 0, \quad C_{\text{blast}} \gg 0$$

In that topology, the penalty for context waste and blast radius exceeds the cost of scaffolding drag.

$$F(\text{merged}) > F(\text{split})$$

The optimization algorithm automatically contracts the schema into a dedicated `item_proto` target and fans out private edges to both `item_store` and the networking component.

When a new requirement arrives, the strategic worker inspects the full global graph and the advisory `refactor_candidates` telemetry in [production_artifacts/manifest.json](../../production_artifacts/manifest.json). It weighs each note against the incoming requirements using deterministic `net_gain` and rework costs. A second Protocol Buffers consumer directly supersedes an earlier single consumer note like `REF-TOPO-item_proto-item_store`. Once the networking target links `item_proto`, the strategic worker ignores the obsolete contraction hint and the manifest generator recomputes consumer fan out as two, dropping the merge candidate automatically.

The decision is entirely mathematical. No human convention, architectural committee, or subjective prompt rule was required. For the broader philosophy behind continuous mathematical architecture across the project lifecycle, read **[Trust the algorithm in systems architecture](trust_the_algorithm.md)**.

