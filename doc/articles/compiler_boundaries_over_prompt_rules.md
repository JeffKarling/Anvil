# Compiler boundaries over prompt rule bloat

Most AI coding setups try to enforce software quality through negative prompting and style checklists. They fill system prompts with prescriptive mandates such as avoiding raw C arrays, forbidding `std::endl`, mandating specific template patterns, or preferring custom wrappers. This approach creates an illusion of control. In reality, micromanaging code generation through prose checklists harms model performance and produces fragile architectures.

Anvil replaces narrative prompt micromanagement with physical boundaries. Instead of dictating how an agent writes private code, Anvil enforces rigid public contracts and trusts the evolving intelligence of frontier models. The build system, compilers, and hardware counters act as objective arbiters.

## Three failure modes of prompt rule bloat

Loading system prompts with negative rules creates three severe failure modes.

**Attention dilution.** Every negative constraint consumes active context window tokens. Large language models operate on finite attention budgets across their context layers. When a prompt is crowded with what not to do, the model has less attention capacity left for core domain algorithms, numerical precision, and tricky edge cases. Negative rules distract the model from solving the real engineering problem.

**Muddy syntax definition.** Natural language rules are imprecise. A prompt that instructs an agent to write modern functional code often causes the model to overcomplicate simple algorithms with deep template indirection or convoluted abstractions. The model attempts to satisfy vague stylistic adjectives rather than writing clean C++. The resulting code becomes harder to verify, slower to compile, and brittle under maintenance.

**Instant obsolescence.** Frontier models improve in reasoning, standard library familiarity, and code cleanliness every few months. Rigid prompt checklists anchor capable new models to yesterday's heuristics. Prompts designed to prevent bugs in older models actively prevent newer models from adopting simpler, idiomatic language features.

## The relentless arrival of frontier models

The speed at which new models come to market will not slow down. Major AI research institutions release smarter, better trained, and faster models at a rapid cadence. Each generation brings deeper comprehension of the C++ standard library, superior type safety inference, and more natural optimization instincts.

Trying to stay ahead of this trajectory with handwritten prompt rules is a losing battle. A prompt crafted to patch the blind spots of one model generation becomes unnecessary baggage for the next. As models evolve, human prompt engineering rules age quickly.

An architecture that relies on prompt rules requires continuous manual editing whenever models change. In contrast, an architecture built on physical component boundaries embraces model progress automatically. When a stronger model arrives, the codebase benefits immediately without modifying a single system rule.

## Physical boundaries as objective arbiters

Anvil solves the quality problem through physical component design inspired by John Lakos. The agent receives a clean, insulated public contract in `targets/<name>/<name>/<name>.hpp`, a strict token ceiling, and zero vendor leakage rules.

How the model writes the private `.cpp` implementation is left entirely to its intelligence. Anvil imposes zero syntax mandates on private translation units. Instead, quality is enforced by four machine verification gates.

**Dual compiler compilation.** Both Clang and GCC must compile the component cleanly. Warnings are treated as hard errors under strict warning flags.

**Runtime sanitizers.** The component test suite runs under AddressSanitizer and UndefinedBehaviorSanitizer. Any memory leak, buffer overflow, or undefined operation fails the build immediately.

**Safety critical static analysis.** Clang-Tidy runs with Category A checks enabled as build errors. Potential data races, analyzer findings, and bugprone patterns halt the build automatically. Stylistic suggestions are recorded separately as refactor candidates in [manifest.json](../../production_artifacts/manifest.json) rather than blocking progress.

**Hardware performance baselines.** In compute components, hardware PMU harnesses record CPU cycles, instructions per cycle, and cache misses. Real hardware counters determine whether code is fast, eliminating subjective human opinions on efficiency.

## Trusting the evolving intelligence

By stepping back from private syntax micromanagement, Anvil establishes a durable foundation for autonomous engineering. Human developers and the [monitor](file:///home/ello/Programming/New%20Projects%20Folder/Anvil/.agents/agents/monitor/agent.json) supervisor define system topology, public interfaces, and mathematical gates. Frontier models handle the implementation details within those bounded sandboxes.

This hands off philosophy keeps agent attention focused where it matters. Because context windows are unburdened by negative checklists, models write idiomatic, high performance code naturally. As frontier models continue their rapid evolution, Anvil harnesses their expanding intelligence without changing the underlying architecture.
