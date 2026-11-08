---
name: feature
description: >-
  Scaffolds and implements a physical component under Anvil.
  Use this skill when adding, creating, or extending a component target in targets/.
---

# Component implementation workflow

## Step 1. Scaffold the target deterministically

For any new component, generate the physical directory hierarchy and boilerplate files using the scaffolding script rather than writing CMake boilerplate manually.

```bash
python3 .agents/skills/feature/scripts/scaffold.py <name>
```

Pass `--no-bench` only for pure schema or signal adapter targets that have no hot computational path.

If the component requires Protobuf code generation, `-fno-fast-math`, private C++23 features, or local SIMD flags, consult `.agents/skills/feature/references/cmake_overrides.md`.

## Step 2. Define the public header and catalog contract

Edit `targets/<name>/<name>/<name>.hpp` and `targets/<name>/<name>.catalog`.
* Keep `<name>.hpp` free of third party headers and macros.
* Define `struct catalog` with 32 character lowercase hex `message_id` strings matching `<name>.catalog`.
* Expose strong types, scoped enums, `std::span` or `std::ranges` inputs, and `noexcept` operational boundaries returning `bool` or `std::optional`.

## Step 3. Write unit tests first

Update `targets/<name>/<name>TEST/<name>TEST.cpp`.
* Retain `static_assert(anvil::journal::is_valid_catalog(anvil::<name>::k_catalog));`.
* Test valid inputs, boundary edge cases, and invalid inputs handled safely without leaking exceptions.
* When verifying emitted log records in memory, redirect the sink via `anvil::journal::detail::set_record_sink`, call `anvil::journal::flush`, and restore via `anvil::journal::detail::reset_record_sink`.

## Step 4. Implement private logic and boundary firewall

Implement `targets/<name>/<name>.cpp`.
* Link any required third party targets from `cmake/dependencies.cmake` as `PRIVATE` in `targets/<name>/CMakeLists.txt`.
* When internal logic spans distinct sub-concerns used only by this component, factor them into private `<helper>.hpp` and `<helper>.cpp` files at `targets/<name>/`, include them via `#include <<helper>.hpp>`, and register `<helper>.cpp` under `PRIVATE` in `target_sources`.
* Wrap every public operational entry point in a `try` block and delegate caught exceptions to `anvil::journal::catch_boundary_exception(k_catalog)`.
* For multi entry catalogs, throw `anvil::journal::catalog_exception(k_catalog.k_entry, "reason")` from internal helpers and pass the fallback entry to `catch_boundary_exception`.

## Step 5. Verify dual compiler builds and capture birth baseline

Run dual compiler verification and record the initial hardware PMU benchmark baseline.

```bash
./production_artifacts/build_all.sh custom debug
./production_artifacts/build_all.sh default release
cmake --build --preset Clang_Custom_Release --target <name>BENCH_run
grep -rn '#include "' targets/
```
