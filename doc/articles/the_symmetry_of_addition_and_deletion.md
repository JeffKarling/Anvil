# The symmetry of addition and deletion in software architecture

## The classical asymmetry between adding and removing

In classical software development, adding and removing code have completely asymmetric complexity. Adding a feature is cheap and straightforward. A developer writes a new function or appends a class. They can also insert a conditional branch.

Removing a feature in a classical codebase is notoriously terrifying. Codebases accumulate hidden coupling and transitive header leaks over time. Unmapped callers rely on unintended side effects.

Because developers fear breaking production, nobody dares to delete old abstractions. Dead libraries linger in build configurations forever. Classical systems grow monotonically through accretion because deletion requires dangerous software archaeology.

## The structural symmetry of Anvil

Anvil restores mathematical symmetry between addition and deletion. In Anvil, removing a capability has the exact same complexity factor as adding one.

This symmetry stems from strict physical design. The system organizes every capability into a physical target within an acyclic quotient DAG. Public contracts reside strictly in dedicated headers with zero vendor leakage.

Every dependency relationship in Anvil is explicit. When you remove a requirement, the strategic worker does not need to guess. It traces the directed edges downstream to discover every consumer. It disconnects the target and prunes dead entries in [cmake/dependencies.cmake](../../cmake/dependencies.cmake). It also updates the build graph.

## Why the complexity factor is identical

For both additions and removals, the strategic worker solves the exact same constraint problem.

* **Acyclic graph validation.** Adding an edge requires proving that no cycles form. Removing an edge reduces topological constraints and cannot introduce cycles.
* **Contract verification.** Adding a feature demands scaffolding public headers and catalogs. Removing a feature demands updating downstream signatures to excise obsolete types.
* **Deterministic gate enforcement.** Both operations must pass the five hard invariant gates. Both operations run the manifest check in [sync_manifest.py](../../.agents/skills/architect/scripts/sync_manifest.py).
* **Token context bounding.** Adding capabilities risks exceeding the budget of sixteen thousand tokens. Removing capabilities shrinks target contexts and improves model reasoning.

## Codebases that breathe instead of accumulate

Classical systems only expand until their technical debt forces a total rewrite. Teams carry dead features for years because removal costs more than maintenance.

In Anvil, codebases breathe in both directions. Removing obsolete requirements is a first class operation with zero fear. The algorithm optimizes the pruned DAG with the same mechanical precision it brings to new capabilities.
