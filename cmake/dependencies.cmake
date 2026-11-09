include_guard(GLOBAL)

find_package(PkgConfig GLOBAL QUIET)

# Approved third party library palette with quiet discovery by default to minimize noise and allow greenfield initialization.
# Marking a dependency REQUIRED signals a mandatory architectural requirement from the human engineer.
# Each entry carries an @anvil_toxicity weight in [0.0, 1.0] for ACCC vendor insulation and Psi subagent sizing.

# @anvil_toxicity: libsystemd = 0.25
pkg_check_modules(libsystemd GLOBAL QUIET IMPORTED_TARGET libsystemd)

# @anvil_toxicity: protobuf = 0.85
pkg_check_modules(protobuf GLOBAL QUIET IMPORTED_TARGET protobuf)
find_program(PROTOC_EXECUTABLE NAMES protoc)

# @anvil_toxicity: tbb = 0.65
pkg_check_modules(tbb GLOBAL QUIET IMPORTED_TARGET tbb)

if(BUILD_TESTING)
    # @anvil_toxicity: GTEST = 0.50
    pkg_check_modules(GTEST GLOBAL QUIET IMPORTED_TARGET gtest gtest_main)
endif()

# High throughput block compression
# @anvil_toxicity: zstd = 0.20
pkg_check_modules(zstd GLOBAL QUIET IMPORTED_TARGET libzstd)

# Embedded relational storage
# @anvil_toxicity: sqlite3 = 0.25
pkg_check_modules(sqlite3 GLOBAL QUIET IMPORTED_TARGET sqlite3)

# High performance hashing and cryptography
# @anvil_toxicity: xxhash = 0.15
pkg_check_modules(xxhash GLOBAL QUIET IMPORTED_TARGET libxxhash)
# @anvil_toxicity: OpenSSL = 0.60
find_package(OpenSSL QUIET)

# Asynchronous kernel I/O and network transport
# @anvil_toxicity: liburing = 0.30
pkg_check_modules(liburing GLOBAL QUIET IMPORTED_TARGET liburing)
# @anvil_toxicity: curl = 0.45
pkg_check_modules(curl GLOBAL QUIET IMPORTED_TARGET libcurl)

# Linear algebra and vectorized mathematics
# @anvil_toxicity: eigen3 = 0.90
pkg_check_modules(eigen3 GLOBAL QUIET IMPORTED_TARGET eigen3)
