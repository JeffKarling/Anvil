cmake_minimum_required(VERSION 3.25)

project(anvil
        VERSION 1.0.0
        DESCRIPTION "High velocity agentic C++ engineering forged on a strict physical component architecture"
        HOMEPAGE_URL "https://github.com/JeffKarling/Anvil"
        LANGUAGES CXX
)

set(PROJECT_LICENSE "MIT-0")

option(ENABLE_WARNING_AS_ERROR "Treat compiler warnings as errors in debug and analysis builds" OFF)
option(ENABLE_IPO "Enable link time optimization for release builds" ON)
option(ENABLE_IWYU "Enable include-what-you-use static analysis" OFF)
option(ENABLE_CPPCHECK "Enable cppcheck static analysis" OFF)
option(BUILD_TESTING "Build unit tests and component benchmarks" ON)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

file(CREATE_LINK
        "${CMAKE_BINARY_DIR}/compile_commands.json"
        "${CMAKE_SOURCE_DIR}/compile_commands.json"
        SYMBOLIC COPY_ON_ERROR
)

find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
    set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
endif()

if(CMAKE_BUILD_TYPE MATCHES ".*Tidy.*")
    set(BUILD_TESTING OFF CACHE BOOL "Build unit tests and component benchmarks" FORCE)
endif()

if(BUILD_TESTING)
    enable_testing()
endif()

add_subdirectory(cmake)

if(BUILD_TESTING)
    set(CMAKE_GTEST_DISCOVER_TESTS_DISCOVERY_MODE PRE_TEST)
    include(GoogleTest)
endif()

add_subdirectory(targets)
