# Anvil versus built in Antigravity tools

Google Antigravity provides conversational tools for autonomous software engineering. Its Orchestrator model and conversational swarms excel at high level exploration and research. They draft initial requirements.

Anvil complements these tools during implementation. Where Antigravity discovers what to build, Anvil provides the deterministic physical architecture required to build it safely. Rooted in John Lakos physical design, Anvil partitions software into discrete physical components with isolated contracts.

## Upstream orchestration versus downstream implementation

Conversational swarms shine during exploratory phases. They gather context across large codebases. They research technical trade offs and draft detailed system requirements.

Once requirements are defined, conversational debate becomes a liability for code generation. Unpartitioned repositories cause severe context dilution. They trigger quadratic token growth and workspace merge collisions.

Anvil replaces conversational debate with physical isolation. Software is decomposed into discrete components fitting within an attention sweet spot. The monitor supervisor dispatches isolated subagents for code generation and verification. Bounded context allows models to implement features with high precision and zero drift.

## Adversarial verification and compiler enforced firewalls

Autonomous coding easily falls into self grading traps. When an agent writes implementation code and test suites simultaneously, it faces incentives to dilute assertions.

Anvil eliminates reward hacking through physical separation of labor.

* **Tactical workers.** A dedicated [tactical_worker](../../.agents/agents/tactical_worker/agent.json) authors implementation code and tests in an isolated Git worktree.
* **Tactical verifiers.** An independent read only [tactical_verifier](../../.agents/agents/tactical_verifier/agent.json) audits candidate diffs before any merge occurs.

Authority never resides in conversational consensus. Code enters the main tree only when it clears strict compiler firewalls and mechanical validation gates.

## Complementary synergy in production engineering

Antigravity and Anvil form a complete engineering pipeline.

Antigravity operates upstream. It directs research and explores dependencies. It also writes structured requirements.

Anvil operates downstream. It takes those requirements and bounds context within fixed token ceilings. It deploys isolated subagents guarded by mechanical compiler gates.