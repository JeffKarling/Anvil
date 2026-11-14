# Strategic architecture over tactical shortcuts

Both human software engineers and artificial intelligence agents share a natural instinct. When presented with a defect and unconstrained autonomy, they gravitate toward tactical shortcuts.

A single agent blasting through a codebase can insert a quick fix in minutes. The bug vanishes from the screen. Beneath the surface, the quick fix leaks private details across public interfaces. It misses crucial state transitions and creates technical debt.

Strategic engineering prevents this degradation by analyzing dependency graphs and anchoring contracts before modifying code. Upfront, it takes longer. Over time, it eliminates refactoring completely.

## A game development lesson in boundary insulation

Consider a game simulation running on deterministic ticks. A presentation layer renders graphics and forwards audio events to a sound hardware coordinator.

During testing, an audio defect appears. An airborne entity emits a pulsating sound while traversing the playfield. When the entity is destroyed, the sound continues playing.

A tactical implementer rushes directly into source files to silence the noise. The developer creates a second audio stream exclusively for the troublesome effect. They copy private simulation constants into public headers and skip automated tests.

A strategic workflow resolves the exact same defect through whole graph analysis. The supervisor delegates investigation to a strategic worker.

The strategic worker insulates contracts by keeping simulation dimensions inside private translation units. Instead of adding effect specific methods, the public contract provides a universal stream clearing interface. The audio device adds queue throttling to eliminate buffer latency. Finally, the strategic worker introduces headless test hooks into the GUI contract. Tactical workers use these hooks to simulate thousands of ticks deterministically.

## The upfront investment of multi agent workflows

On the surface, Anvil implements features slower than single agent alternatives.

A single agent model reads a prompt and modifies files directly. It finishes quickly. Anvil coordinates a multi agent pipeline. It invokes a strategic worker for graph triage and contract anchoring. Next it triggers independent verifiers and dispatches parallel tactical workers into isolated worktrees. Workers and verifiers both run redundant compile passes and runtime sanitizers. They also run static analysis checks.

This pipeline takes noticeably longer wall clock time. Yet a fast single agent fix rarely accounts for the downstream rework it creates. When an agent hacks an interface, human engineers must spend days diagnosing broken abstractions.

Anvil amortizes its upfront compute time across a stable project lifetime. Enforcing contract insulation and deterministic testability from the start eliminates subsequent refactoring.

## Unifying project structure and agent workflows

Autonomous strategic engineering cannot function within an unstructured codebase. When multiple agents edit shared translation units without physical boundaries, context windows saturate and hallucinated edits collide.

* **Physical component boundaries.** Systems must be partitioned into cohesive components with explicit public contracts. Rigid context budgets ensure translation units remain small enough for deep reasoning by worker models.
* **Deterministic state machines.** The orchestrator must act as a strict state machine rather than an active programmer. It enforces orderly progression from contract anchoring to invariant verification.
* **Adversarial verification.** Implementations cannot be trusted based on self reported agent success. Independent verifiers must inspect proposed diffs to prevent assertion dilution.

Fast tactical hacks generate legacy code at machine speed. Disciplined strategic workflows build software that never needs to be refactored.
