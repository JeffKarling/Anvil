# Compiler boundaries over prompt rule bloat

Most AI coding setups attempt to enforce code quality through negative prompts and style checklists. They fill system prompts with prescriptive rules against specific syntax or library choices. This approach creates an illusion of control. Micromanaging code generation through prose checklists harms model performance and produces fragile software.

Anvil replaces narrative prompt micromanagement with physical boundaries and discrete mathematics. Instead of dictating how an agent writes private code, Anvil enforces rigid public contracts. Compilers and sanitizers act as objective arbiters. Hardware counters verify performance.

## Three failure modes of prompt rule bloat

Loading system prompts with negative rules creates three distinct failure modes.

* **Attention dilution.** Negative rules consume active context tokens. When a prompt is crowded with restrictions, the model has less attention capacity for core algorithms and edge cases.
* **Muddy syntax definition.** Natural language rules are inherently imprecise. Instructing an agent to write modern code often causes the model to add unnecessary template indirection.
* **Instant obsolescence.** Frontier models improve in reasoning and standard library familiarity every few months. Rigid prompt checklists anchor capable new models to obsolete heuristics.

## Physical boundaries as objective arbiters

Anvil solves quality through physical component design. The agent receives a clean public contract in `targets/<name>/<name>/<name>.hpp`. It also receives a strict token ceiling and zero vendor leakage rules.

How the model writes the private `.cpp` implementation is left entirely to its intelligence. Anvil imposes zero syntax mandates on private translation units. Instead, quality is enforced by four machine verification gates.

* **Dual compiler compilation.** Both Clang and GCC must compile the component cleanly under strict warning flags.
* **Runtime sanitizers.** The component test suite runs under AddressSanitizer and UndefinedBehaviorSanitizer. Any memory leak or undefined operation fails the build immediately.
* **Static analysis.** Clang-Tidy runs with Category A checks enabled as build errors. Concurrency faults and bugprone patterns halt the build automatically.
* **Hardware performance baselines.** In compute components, hardware PMU harnesses record CPU cycles and cache misses. Real hardware counters determine efficiency objectively.

## Trusting evolving intelligence

By eliminating syntax micromanagement, Anvil establishes a durable foundation for autonomous engineering. Human developers and the [monitor](../../.agents/agents/monitor/agent.json) supervisor define system topology and mathematical gates. Frontier models handle implementation details within those bounded sandboxes.

Because context windows remain unburdened by negative checklists, models write idiomatic code naturally. As frontier models continue their rapid evolution, Anvil harnesses their expanding intelligence without changing the underlying architecture.
