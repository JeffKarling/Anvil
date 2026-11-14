# The 16384 token ceiling in physical component design

In Anvil, every physical component operates under a hard mathematical context ceiling of $B_{\max} = 16384$ tokens. This constant sits at the intersection of binary memory conventions and physical design limits. It aligns with transformer attention dynamics.

## Exact binary power

The number $16384$ is $2^{14}$. In computer science, powers of two represent natural boundaries for memory pages and buffer allocations.

Using $2^{14}$ establishes an exact binary boundary. It provides a clean mathematical baseline for context window partitioning and sizing equations across the codebase.

## The token footprint of a Lakosian component

Under John Lakos physical component design, a single component represents one conceptual abstraction implemented across a cohesive physical unit. In Anvil, this unit comprises four elements.

* One public header `targets/<name>/<name>/<name>.hpp` defining the interface.
* One private implementation `targets/<name>/<name>.cpp` holding internal logic.
* One unit test suite `targets/<name>/<name>TEST/<name>TEST.cpp` verifying behavior.
* Optional private internal helpers and direct upstream public headers.

A well partitioned C++ component spans between 500 and 1500 lines of code. In modern C++, one line averages roughly 8 to 10 tokens.

A cohesive 1500 line component and its direct upstream interfaces consume roughly 12000 to 14000 tokens. Setting $B_{\max} = 16384$ establishes a realistic ceiling that accommodates a complete physical component while forbidding bloated god components.

## Dense attention sweet spot

Modern frontier models support context windows exceeding one million tokens. However, raw context capacity does not equal dense reasoning capability.

As context length expands, attention distribution thins across the sequence. Models experience subtle recall degradation and instruction drift when reasoning across unconstrained contexts.

At 16384 tokens, frontier models operate in their peak dense attention sweet spot. Needle retrieval and cross file type inference operate with near perfect fidelity. Bounding components to 16384 tokens guarantees that a [tactical_worker](../../.agents/agents/tactical_worker/agent.json) never experiences cognitive fog.

## Turn headroom in the edit compile test loop

A tactical worker executes an iterative loop. It reads contracts and drafts code. It invokes compilers and repairs errors.

Bounding static source code $W(C_i)$ within 16384 tokens preserves headroom in the working window. The worker retains space for reasoning chains and test execution output. The agent finishes its task without triggering context compaction.

## The mathematical trigger for invariant gate H5

In Anvil, $B_{\max}$ acts as the threshold for Invariant Gate $H_5$ in [sync_manifest.py](../../.agents/skills/architect/scripts/sync_manifest.py).

Whenever the combined token footprint of a component and its direct upstream headers exceeds 16384 tokens, the gate fails immediately.

$$W(C_i) > B_{\max}$$

The manifest introspection script flags the component as an invariant violation. It generates a `REF-TOPO-SPLIT` candidate in [manifest.json](../../production_artifacts/manifest.json). This threshold prevents code rot objectively before a component can expand uncontrollably.

## Normalizing the subagent sizing score

In the sizing equation, $B_{\max}$ normalizes the context saturation term.

$$\text{saturation} = \frac{W(C_i)}{B_{\max}}$$

This keeps the saturation metric bounded between 0.0 and 1.0. A component approaching 16384 tokens receives a high saturation score that pushes its worker sizing $\Psi(C_i)$ into the `pro` tier. Compact components stay near 0.20 saturation, allowing the [monitor](../../.agents/agents/monitor/agent.json) supervisor to dispatch fast `flash` workers.
