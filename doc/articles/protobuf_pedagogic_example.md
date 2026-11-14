# The Protobuf pedagogic example

Anvil calculates component boundaries using discrete mathematics rather than human intuition. The starter repository ships with a deliberate architectural contradiction to illustrate this principle. It demonstrates both vendor isolation mechanics and the mathematical proof that favors a simpler graph.

## The educational contradiction in the template

When a developer sees a Protocol Buffers file, their instinct is to create a dedicated schema component. In human thinking, schemas belong in their own layer separate from storage logic.

The starter template includes two components for Protocol Buffers in `targets/item_proto` and `targets/item_store`. Both components compile cleanly. The component `item_proto` sets `SYSTEM ON` to suppress warnings on generated code. The component `item_store` links `item_proto` strictly `PRIVATE` and exposes a pure C++ public header.

Every line of code satisfies Lakosian physical design. Yet in this specific topology, creating two components is objectively an architectural mistake.

The Anvil contraction algorithm proves the design should be a single consolidated component. The cost of establishing and maintaining a separate component outweighs the marginal benefit of extra isolation.

Leaving this split unoptimized demonstrates the automated refactor telemetry in [manifest.json](../../production_artifacts/manifest.json). The manifest generator flags both components under `refactor_candidates`. That JSON entry records an advisory note explaining that `item_proto` has a consumer fan out of one. Merging both components eliminates scaffolding drag with positive net gain.

## Proving the single component calculation

The mathematical correctness of the algorithm becomes clear when analyzing physical forces under Anchor Constrained Capability Contraction.

$$F(G) = \sum C_{\text{scaffold}} + \sum C_{\text{waste}} + \sum C_{\text{blast}} + \sum C_{\text{insulate}}$$

Suppose requirements mandate storing records to disk using Protocol Buffers. No other component reads or writes this format. The consumer fan out of the schema is exactly one.

### The split two component layout

When the schema lives in `item_proto` and is consumed by `item_store`, the algorithm evaluates the physical forces.

* **Scaffolding drag.** The layout introduces an extra directory and CMake build file alongside an additional test suite. Therefore, $C_{\text{scaffold}} > 0$.
* **Blast radius and context waste.** Because no other component consumes `item_proto`, the fan out is one. Creating a separate component isolates no secondary consumer. Therefore, $C_{\text{waste}} = 0$ and $C_{\text{blast}} = 0$.

The split layout incurs non zero scaffolding cost while delivering zero reduction in blast radius or context waste.

$$F(\text{split}) = C_{\text{scaffold}} + C_{\text{insulate}}$$

### The merged single component layout

When the `.proto` file is placed directly inside `item_store`, generated files remain private inside the local build directory.

* **Scaffolding drag.** Only one component directory and one CMake file exist. Only one test suite exists. Therefore, $C_{\text{scaffold}} = 0$.
* **Context waste.** Generated headers are never added to any public file set. Downstream callers see only native C++ domain types in `item_store.hpp`. Downstream context waste is zero.
* **Blast radius.** No external component links the schema. Changes to the schema recompile only `item_store.cpp`. Therefore, $C_{\text{blast}} = 0$.
* **Vendor insulation.** Because generated files exist only inside the private build tree, external components cannot include them.

The optimization function proves that merging the schema into a single component yields a strictly lower friction score.

$$F(\text{merged}) < F(\text{split})$$

## When the mathematics demand a split

The algorithm is never dogmatic. If system requirements change, mathematical forces adjust immediately.

Suppose a new requirement introduces a networking component receiving the same Protocol Buffers packets over UDP. Now two independent components consume the schema. The consumer fan out is two.

If the schema remained merged inside `item_store`, the networking component would be forced to depend on `item_store`. That dependency introduces severe context waste and pulls unrelated storage logic into the networking subagent.

$$C_{\text{waste}} \gg 0, \quad C_{\text{blast}} \gg 0$$

In that topology, the penalty for context waste and blast radius exceeds the cost of scaffolding drag.

$$F(\text{merged}) > F(\text{split})$$

The algorithm automatically contracts the schema into a dedicated `item_proto` component and fans out private edges to both consumers.

The decision is entirely mathematical. No architectural committee or subjective prompt rule is required.
