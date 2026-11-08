---
name: audit-sans
description: >-
  Runs unit test suites across dual compilers Clang and GCC, standard library deep hardening, and runtime sanitizers.
  Use this skill when running sanitizers, checking for memory leaks, data races, or cross-compiler parity.
---

# Runtime sanitizers and dual compiler audit workflow

## Step 1. AddressSanitizer and LeakSanitizer

```bash
cmake --workflow --preset Clang_ASan_Verify
cmake --workflow --preset GNU_ASan_Verify
cmake --workflow --preset Clang_LSan_Verify
```

## Step 2. UndefinedBehaviorSanitizer

```bash
cmake --workflow --preset Clang_UBSan_Verify
cmake --workflow --preset GNU_UBSan_Verify
```

## Step 3. ThreadSanitizer

```bash
cmake --workflow --preset Clang_TSan_Verify
```

## Step 4. Dual compiler parity and deep standard library hardening

```bash
./production_artifacts/build_all.sh custom debug
./production_artifacts/build_all.sh default release
./production_artifacts/build_all.sh custom deep
```

Resolve any sanitizer trace, bounds violation, or compiler warning before completing the audit.
