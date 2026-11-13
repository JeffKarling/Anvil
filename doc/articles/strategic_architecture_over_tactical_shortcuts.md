# Strategic architecture over tactical shortcuts

Both human software engineers and artificial intelligence agents share a natural instinct. When presented with a defect and unconstrained autonomy, they gravitate toward tactical shortcuts.

A single agent model blasting through a codebase can insert a quick fix with impressive speed. The bug vanishes from the screen in minutes. On the surface, the problem appears solved. Beneath the surface, the system degrades. The quick fix leaks private details across public interfaces, misses crucial state transitions, and creates technical debt that requires costly refactoring later.

Strategic engineering prevents this degradation by analyzing dependency graphs and anchoring contracts before modifying code. This disciplined approach represents the primary breakthrough of agentic software development. However, strategic programming requires accepting an uncomfortable truth. Up front, it takes longer.

## A game development lesson in audio and GUI boundaries

Real world game development illustrates this contrast. Consider a game simulation running on deterministic ticks. A presentation layer renders graphics and forwards audio events to a sound hardware coordinator.

During testing, an audio defect appears. An airborne target emits a pulsating sound while traversing the playfield. When the entity is destroyed, the sound continues playing. The audio also persists when a player dies, pauses the game, or returns to the menu.

A tactical implementer rushes directly into source files to silence the noise. The investigation never leaves the surface layer.

The tactical fix applies manual stop calls inside the GUI loop and adds a custom stop command to the public audio contract. To silence that specific sound without halting background music, the developer creates a second hardware audio stream exclusively for the troublesome effect. The developer also copies private simulation constants into public headers, saturates the audio hardware queue with unchecked audio packets, and skips automated tests because building a headless GUI harness feels inconvenient.

A strategic workflow resolves the exact same defect through whole graph analysis. In this model, the supervisor never touches private implementation code. It delegates investigation to a strategic worker.

The strategic worker insulates contracts by keeping simulation dimensions inside private translation units. Instead of adding fragile effect specific audio methods, the public contract provides a universal stream clearing interface. The audio device adds queue throttling to eliminate buffer latency, allowing explosion sounds to preempt background loops instantly. Finally, the strategic worker introduces headless test hooks into the GUI contract. Tactical workers use these hooks to simulate thousands of ticks deterministically. They verify audio cutoffs across player deaths, wave resets, and game over states.

## The honest cost of subagent delegation

We must be honest about execution speed. On the surface, Anvil implements features and bug fixes slower than single agent alternatives.

A single agent model reads a prompt, modifies files directly, and completes in minutes. In contrast, Anvil refuses to take shortcuts. The monitor supervisor coordinates a deliberate multi agent pipeline. It invokes a strategic worker for graph triage and contract anchoring. Next it triggers independent verifiers and dispatches parallel tactical workers into isolated worktrees. Workers and verifiers both run redundant compile passes, runtime sanitizers, and static analysis checks.

This pipeline takes noticeably longer wall clock time. Yet a fast single agent fix rarely accounts for the downstream rework it creates. When an agent hacks an interface or ignores buffer saturation, human engineers must spend days diagnosing latency or untangling broken abstractions.

Anvil amortizes its upfront compute time across a stable project lifetime. By enforcing contract insulation and deterministic testability from the start, subsequent refactoring is eliminated completely. You invest additional clock time once to avoid perpetual maintenance costs.

## Unifying project structure and agent workflows

Autonomous strategic engineering cannot function within an unstructured codebase. When multiple agents edit shared translation units without physical boundaries, context windows saturate and hallucinated edits collide.

Software architecture and agent workflows must be designed as one cohesive system.

**Physical component boundaries.** Systems must be partitioned into self contained components with explicit public contracts. Rigid context budgets ensure translation units remain small enough for deep reasoning by worker models.

**Deterministic state machines.** The orchestrator must act as a strict state machine rather than an active programmer. It enforces orderly progression from contract anchoring to invariant verification and parallel tactical waves.

**Adversarial verification.** Implementations cannot be trusted based on self reported agent success. Independent verifiers must inspect proposed diffs to prevent assertion dilution and invariant evasion.

Fast tactical hacks generate legacy code at machine speed. Disciplined strategic workflows build software that never needs to be refactored.
