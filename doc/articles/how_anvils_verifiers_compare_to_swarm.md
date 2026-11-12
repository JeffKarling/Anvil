# How Anvil verifiers compare to Swarm

In a community update on Reddit, the Google Antigravity team summarized the motivation behind the Swarm feature. Previously, developers could spin up many agents and subagents within Antigravity, but they rarely played nicely together. Swarm changed that dynamic by coordinating multiple agents to meet user prompts in a shared conversational space.

Both Swarm and Anvil tackle the same fundamental challenge of multi-agent software development. Complex engineering projects quickly overwhelm a single model. Solving large problems requires multiple specialized agents working in concert.

However, Anvil and Swarm take opposing paths to coordinate agents. Swarm coordinates agents through a shared conversational feed. Anvil achieves adversarial verification by structuring agents around physical component boundaries.

## The mechanics of a shared conversational feed

In a conversational swarm, multiple agents share a single message thread. One agent proposes a plan, a second agent challenges assumptions, and a third writes code. They communicate by posting conversational turns to the shared transcript.

This conversational model excels at open-ended discovery. When exploring vague requirements or brainstorming user interface ideas, natural language debate helps models reach consensus. The agents see each other's reasoning and refine their ideas together.

In systems C++, however, a shared conversational feed encounters three severe physical bottlenecks.

**Quadratic token explosion.** As agents converse in a shared channel, the transcript grows with every turn. Because all agents read the common history, every message multiplies across the context window of every active model. Token consumption scales quadratically, quickly consuming reasoning budgets on social banter rather than code.

**Social consensus versus compiler reality.** Large language models are trained to be agreeable. In a shared chat room, conversational debate can converge on plausible compromises that still fail in the physical world. An agent may convince its peers that an algorithm is sound, yet the code contains data races, cache thrashing, or undefined pointer behavior. Conversational consensus cannot replace mechanical compiler verification.

**Workspace collision.** When multiple agents attempt to modify the same repository without physical boundaries, they risk editing overlapping files. Diff reconciliation in a single workspace creates merge conflicts and pollutes version control history.

## Physical target boundaries as an audit firewall

Anvil replaces conversational chat rooms with physical component boundaries rooted in John Lakos software architecture. Instead of placing agents in a shared room, Anvil isolates them inside discrete translation units.

Every component in Anvil occupies a physical directory under `targets/<name>/`. Components publish clean public contracts in `targets/<name>/<name>/<name>.hpp` and hide private translation units inside `targets/<name>/<name>.cpp`.

This physical separation transforms how agents collaborate across three fundamental dimensions.

**Bounded context locality.** A [tactical_worker](../../.agents/agents/tactical_worker/agent.json) never reads a running chat feed of what other workers are doing. It loads only its assigned directory and the public headers of direct upstream dependencies. Total worker context remains bounded within $B_{\max} = 16384$ tokens. Ten workers can run in parallel without multiplying token overhead across each other.

**Isolated shared worktrees.** Antigravity provisions workers in isolated Git worktrees branched from `HEAD`. Because each worker operates in a separate physical filesystem directory, parallel agents never collide on files or produce merge conflicts.

**Adversarial verification without social bias.** In Anvil, verification is adversarial and unyielding. The [tactical_verifier](../../.agents/agents/tactical_verifier/agent.json) never debates the worker. It inspects the candidate diff from a clean, read only perspective. It checks whether unit test assertions were diluted, whether mocks were introduced to bypass real hardware, and whether benchmark workloads were gamed.

## Compilers and hardware as the ultimate arbiters

The deepest difference between Swarm and Anvil lies in where authority resides.

In a conversational swarm, authority is social. The agents decide a feature is complete when their shared discussion reaches consensus.

In Anvil, authority is mechanical. The supervising [monitor](../../.agents/agents/monitor/agent.json) accepts a component only when objective machine gates pass.

Both Clang and GCC must compile the code cleanly under strict warning flags. The unit tests must execute and pass without assertion failures. Runtime sanitizers must report zero memory leaks, buffer overruns, or undefined behavior. Clang-Tidy Category A safety checks must clear with zero errors. In compute components, hardware PMU counters must record valid instruction retirements and cache metrics.

No amount of conversational persuasion can satisfy these gates. The code either compiles and executes correctly on real silicon, or the candidate diff is discarded.

## Choosing the right tool for the engineering domain

Swarm and Anvil serve complementary purposes in the software development lifecycle.

The Swarm conversational model is well suited for high level design ideation, user interviews, and product exploration. When human intent is ambiguous, having multiple agents brainstorm in a shared feed surfaces valuable perspectives.

Anvil is built for production systems engineering where performance and correctness are non-negotiable. By organizing agents around physical component boundaries and mathematical invariant gates, Anvil delivers high velocity software development without context explosion, file collisions, or social compromise.
