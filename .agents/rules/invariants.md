# Anvil workspace invariants

## General
Do not inspect or read files matching .gitignore patterns, especially Build/, build/ or log directories, unless explicitly requested.

## Physical component layout

* **One name rule.** Every directory `targets/<name>/` defines exactly one CMake target `${DIR_NAME}` aliased as `${PROJECT_NAME}::${DIR_NAME}` inside `namespace anvil::<name>`.
* **Public contract.** Public headers reside strictly in `targets/<name>/<name>/<name>.hpp` and register under `PUBLIC FILE_SET ${DIR_NAME} TYPE HEADERS`.
* **Tactical helpers versus strategic targets.** Internal helpers reside at `targets/<name>/<helper>.hpp` and `targets/<name>/<helper>.cpp` outside the `PUBLIC FILE_SET`. Extend an existing component with private helpers when new public interfaces share the same abstraction and header dependencies. Extract a new sibling target `targets/<new_name>/` when a capability is shared by multiple components, introduces distinct domain concepts, or would force existing consumers of `<name>/<name>.hpp` to pull unrelated headers into their compilation and token context.
* **Mandatory shared CMake includes.** Every target `CMakeLists.txt` must include `${CMAKE_BINARY_DIR}/target_properties.cmake` and `${CMAKE_BINARY_DIR}/target_compile_options.cmake` immediately after target creation. Never omit these includes. Apply local flag adjustments after the includes.
* **Colocated verification.** Every library target maintains unit tests in `targets/<name>/<name>TEST/`. Algorithmic and hot path targets maintain hardware PMU benchmarks in `targets/<name>/<name>BENCH/`.

## Header hygiene and third party insulation

* **Mandatory angle brackets.** Every `#include` directive across all headers, sources, tests, and benchmarks must use `<...>`. Quoted includes `#include "..."` are prohibited.
* **Zero third party leakage.** Public headers `<name>/<name>.hpp` must never include third party headers or expose external vendor types.
* **Centralized private linking.** External libraries must be declared globally in `cmake/dependencies.cmake` and linked strictly `PRIVATE` in `targets/<name>/CMakeLists.txt`. Component build files must never invoke `find_package` or `pkg_check_modules`.

## Interface and implementation contracts

* **Strong typing.** Wrap domain primitives in strong structs or scoped `enum class` types. Never place adjacent parameters of the same primitive type in a function signature. Mark single argument constructors `explicit`.
* **Value and resource safety.** Enforce invariants via private constructors and fallible static factories returning `std::optional` or `std::expected`. Manage all resources via RAII and never return raw owning pointers.
* **Ranges and views.** Accept `std::span` or `std::ranges` concepts in public signatures rather than concrete containers. Use `<ranges>` and `std::views` pipelines instead of naked C style `for` loops. Use `std::views::enumerate` for indexed iteration and `std::views::iota` for bounded counts. Slice spans before loops via `span.first(count)` to hoist hardened bounds checks. Never return non-owning views over local temporaries or across mutex boundaries.

## Boundary exception firewall and logging

* **Noexcept operational boundaries.** Public operational functions must be `noexcept` and return `bool` or `std::optional`. Catch all unhandled exceptions at the boundary via `anvil::journal::catch_boundary_exception`.
* **Catalog contracts.** Operational targets define `<name>.catalog` and a closed `struct catalog` with up to eight `anvil::journal::catalog_entry` members and `inline constexpr catalog k_catalog{};` in `<name>.hpp`. Single entry components pass `k_catalog` directly to `catch_boundary_exception(k_catalog)`. Multi entry components pass a specific fallback `catalog_entry` and throw `anvil::journal::catalog_exception` from internal helpers.
* **Structured flight recorder logging.** Emit internal diagnostics generously using `anvil::journal::log` with `journal::severity`, `journal::message`, and `journal::binary_payload`. Keep `journal` free of IPC or network logic.

## Verification synchronization

* **Immediate test and benchmark parity.** Every code or signature change must update `targets/<name>/<name>TEST/` in the same step, verify compilation under both GCC and Clang via `./production_artifacts/build_all.sh custom debug`, and run `<name>BENCH_run` under `Clang_Custom_Release` when a benchmark exists.
