---
name: audit-static
description: >-
  Runs compile-time static analysis, Clang-Tidy checks, Cppcheck scans, and Include-What-You-Use header hygiene.
  Use this skill when running static analysis, checking code quality, or auditing header includes.
---

# Static analysis and header hygiene workflow

## Step 1. Clang-Tidy analysis

```bash
cmake --preset Clang_Tidy
cmake --build --preset Clang_Tidy
```

Fix bugprone, analyzer, and core guideline findings immediately. Log intentional situational exceptions in `production_artifacts/clang_tidy_state.md`.

## Step 2. Cppcheck scan

```bash
cmake --preset GNU_Custom_Debug -DENABLE_CPPCHECK=ON
cmake --build --preset GNU_Custom_Debug
```

## Step 3. Include-What-You-Use header hygiene

```bash
cmake --preset GNU_Custom_Debug -DENABLE_IWYU=ON
cmake --build --preset GNU_Custom_Debug
grep -rn '#include "' targets/
```

Ensure every file directly includes the headers it uses via `<...>` and remove unused transitive includes.

## Step 4. Strict warning gate reset

Reset analysis flags and verify zero warnings under both compilers with warnings treated as errors.

```bash
cmake --preset GNU_Custom_Debug -DENABLE_IWYU=OFF -DENABLE_CPPCHECK=OFF -DENABLE_WARNING_AS_ERROR=ON && cmake --build --preset GNU_Custom_Debug
cmake --preset Clang_Custom_Debug -DENABLE_WARNING_AS_ERROR=ON && cmake --build --preset Clang_Custom_Debug
```
