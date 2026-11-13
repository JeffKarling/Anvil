# Anvil versus built in Antigravity tools

Google Antigravity provides powerful built in capabilities for autonomous software engineering. The platform features an Orchestrator model that dynamically routes subtasks across Gemini model tiers including Gemini Carbon, Argon and Hydrogen. It also provides native Swarm message boards and subagent hierarchies that coordinate parallel workers across isolated workspaces.

These built in features prompt an essential question. If Antigravity already provides multi model orchestration and parallel agent swarms, what unique purpose does Anvil serve?

Anvil and Antigravity solve software development challenges at two fundamentally different layers. Antigravity provides the runtime mechanism for inference routing and multi agent execution. Anvil provides the deterministic physical architecture that structures code, bounds attention contexts and prevents architectural entropy.

## Mechanism versus architecture

An agent platform without architectural discipline quickly encounters entropy.

Built in Antigravity tools are intentionally domain agnostic. The Orchestrator model inspects prompt complexity to select an optimal model tier. The native Swarm manages turn pacing and board notifications. Subagent APIs spawn child sessions and branch Git worktrees. None of these mechanisms possess intrinsic knowledge of C++ translation units, Lakosian dependency graphs or runtime memory safety.

Anvil supplies the missing architectural layer. Rooted in the physical design principles of John Lakos, Anvil partitions software into discrete physical targets under `targets/<name>/`. Each component publishes a strict public contract in `targets/<name>/<name>/<name>.hpp` and hides its private implementation inside `targets/<name>/<name>.cpp`.

Anvil does not compete with Antigravity tools. Instead, Anvil configures and constrains them. By establishing physical boundaries and mechanical validation gates, Anvil transforms Antigravity into a deterministic systems engineering engine.

## Model routing versus bounded context locality

The Antigravity Orchestrator model optimizes inference economics. It dispatches frontier reasoning models for complex architectural decisions. Meanwhile, it assigns high speed models to routine implementation and test loops.

This dynamic routing excels on small and well insulated tasks. In unpartitioned legacy codebases, however, model routing cannot solve context dilution. When an implementation task requires reading across dozens of intermingled files, even frontier models experience cognitive fog. A lightweight model like Gemini Hydrogen quickly degrades when presented with thousands of lines of uninsulated code.

Anvil solves this challenge through [the 16384 token ceiling](the_16384_token_ceiling.md). Every physical component in Anvil operates under a hard context boundary of $B_{\max} = 16384$ tokens. This budget includes the public contract, the private implementation, the unit test suite and direct upstream headers.

Guaranteeing that every target fits inside 16384 tokens ensures that workers always operate in their peak dense attention sweet spot. An Antigravity Orchestrator can confidently assign implementation loops to fast models like Gemini Hydrogen. Because physical scope is strictly bounded, the smaller model executes with high precision and near zero instruction drift.

## Conversational swarms versus physical target boundaries

In a native Antigravity Swarm, multiple agents collaborate through a shared conversational message board. One agent outlines a proposal, a peer challenges assumptions and a worker writes code.

This conversational model works well for open ended discovery, user experience design and high level feature brainstorming. In systems programming, however, a shared conversational feed encounters three severe physical bottlenecks.

* **Quadratic token scaling.** As multiple agents converse in a shared channel, the transcript grows with every turn. Because all agents read the shared history, token consumption scales quadratically across every active model. Reasoning budgets are quickly consumed by conversational commentary rather than code generation.

* **Social consensus over compiler reality.** Large language models are trained to be agreeable. In a shared chat room, conversational debate often converges on plausible compromises that fail under real hardware constraints. An agent may convince its peers that an algorithm is sound, yet the code contains data races, cache thrashing or undefined pointer arithmetic. Conversational consensus cannot replace mechanical compiler verification.

* **Workspace collision.** When multiple agents attempt to modify the same repository without physical boundaries, they risk editing overlapping files. Reconciling diffs in a shared workspace produces merge conflicts and pollutes version control history.

Anvil replaces conversational debate with physical isolation. Agents never sit in an open chat room discussing code. Instead, each [tactical_worker](../../.agents/agents/tactical_worker/agent.json) is isolated to a discrete component directory inside a dedicated Git worktree. Workers communicate through public contracts, candidate diffs and compiler diagnostics. Token usage remains strictly linear, and attention remains locked on physical code.

## Adversarial verifiers versus self grading loops

A critical failure mode in autonomous coding is the self grading trap. When a single agent authors implementation code and tests in the same loop, it inevitably faces subtle reward hacking incentives.

If a unit test fails, the fastest route to a green exit code is often modifying the test rather than fixing the underlying C++ logic. Standard agent loops easily slip into assertion dilution, deleting tricky edge cases or introducing mocks that bypass real operating system calls.

Antigravity built in subagents do not inherently prevent self grading. A worker given permission to edit files can modify tests to match broken implementation code.

Anvil eliminates reward hacking through adversarial separation of labor. Component implementation is divided between two distinct agents.

* **The tactical worker.** The [tactical_worker](../../.agents/agents/tactical_worker/agent.json) owns the private `.cpp` file and the test suite inside an isolated Git worktree. It executes compilation loops until scoped builds and tests pass cleanly.

* **The tactical verifier.** The [tactical_verifier](../../.agents/agents/tactical_verifier/agent.json) is an independent critic holding strictly read only tools. It audits candidate diffs in the primary workspace before any merge occurs.

The tactical verifier actively searches for cheating. It rejects candidate diffs that dilute assertions, mock away system complexities or game performance benchmarks with compile time constants. Persuasion is impossible because the verifier never converses with the worker. It evaluates only the candidate diff against immutable contract baselines.

## Mechanical silicon gates as the ultimate arbiters

The deepest difference between built in conversational tools and Anvil lies in where authority resides.

In conversational agent setups, authority is conversational. Work is deemed complete when agents or human reviewers reach consensus that the output looks acceptable.

In Anvil, authority is purely mechanical. The supervising [monitor](../../.agents/agents/monitor/agent.json) accepts a component only when objective machine gates pass.

* **Dual compiler parity.** Both Clang and GCC must compile the component cleanly under strict warning flags.
* **Runtime sanitizers.** The component test suite must pass under AddressSanitizer and UndefinedBehaviorSanitizer without a single leak or memory error.
* **Safety critical static analysis.** Clang-Tidy Category A checks must clear with zero errors.
* **Hardware performance baselines.** In compute components, hardware PMU harnesses record CPU cycles, instructions per cycle and cache misses. Real silicon telemetry determines whether code is fast, eliminating subjective opinions on efficiency.

No amount of persuasive conversational rationale can satisfy these gates. The code either compiles and executes correctly on real silicon, or the candidate diff is discarded.

## Complementary synergy in production engineering

Anvil and built in Antigravity tools are not competing alternatives. They represent complementary halves of a robust autonomous engineering platform.

Antigravity provides the execution engine. Its Orchestrator model reduces operational costs by routing prompts to optimal model tiers. Its subagent infrastructure provisions parallel workers across isolated Git worktrees.

Anvil provides the architectural discipline that makes that engine safe. By enforcing Lakosian physical boundaries, bounding contexts within 16384 tokens and requiring adversarial verification, Anvil prevents code rot and eliminates reward hacking.

Together, they allow engineering organizations to harness frontier AI capabilities with the uncompromising rigor demanded by high performance systems.
