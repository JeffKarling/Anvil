include_guard(GLOBAL)

find_package(PkgConfig GLOBAL QUIET)

# Approved third party library palette with quiet discovery by default to minimize noise and allow greenfield initialization.
# Marking a dependency REQUIRED signals a mandatory architectural requirement from the human engineer.

pkg_check_modules(libsystemd GLOBAL QUIET IMPORTED_TARGET libsystemd)
pkg_check_modules(protobuf GLOBAL QUIET IMPORTED_TARGET protobuf)
find_program(PROTOC_EXECUTABLE NAMES protoc)
pkg_check_modules(tbb GLOBAL QUIET IMPORTED_TARGET tbb)

if(BUILD_TESTING)
    pkg_check_modules(GTEST GLOBAL QUIET IMPORTED_TARGET gtest gtest_main)
endif()

# High throughput block compression
pkg_check_modules(zstd GLOBAL QUIET IMPORTED_TARGET libzstd)

# Embedded relational storage
pkg_check_modules(sqlite3 GLOBAL QUIET IMPORTED_TARGET sqlite3)

# High performance hashing and cryptography
pkg_check_modules(xxhash GLOBAL QUIET IMPORTED_TARGET libxxhash)
find_package(OpenSSL QUIET)

# Asynchronous kernel I/O and network transport
pkg_check_modules(liburing GLOBAL QUIET IMPORTED_TARGET liburing)
pkg_check_modules(curl GLOBAL QUIET IMPORTED_TARGET libcurl)

# Linear algebra and vectorized mathematics
pkg_check_modules(eigen3 GLOBAL QUIET IMPORTED_TARGET eigen3)
