#!/usr/bin/env python3
"""Deterministic physical component scaffolder for Anvil."""

import argparse
import pathlib
import sys
import uuid


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a physical component under targets/<name>/")
    parser.add_argument("name", help="Component name in snake_case")
    parser.add_argument("--no-bench", action="store_true", help="Omit the <name>BENCH directory")
    args = parser.parse_args()

    name = args.name.strip()
    if not name.isidentifier():
        print(f"Error: '{name}' is not a valid C++ identifier.", file=sys.stderr)
        return 1

    repo_root = pathlib.Path(__file__).resolve().parents[4]
    target_dir = repo_root / "targets" / name
    if target_dir.exists():
        print(f"Error: Target directory {target_dir} already exists.", file=sys.stderr)
        return 1

    header_dir = target_dir / name
    test_dir = target_dir / f"{name}TEST"
    bench_dir = target_dir / f"{name}BENCH"

    header_dir.mkdir(parents=True)
    test_dir.mkdir(parents=True)
    if not args.no_bench:
        bench_dir.mkdir(parents=True)

    msg_id = uuid.uuid4().hex
    bench_subdir = f"    add_subdirectory(${{DIR_NAME}}BENCH)\n" if not args.no_bench else ""

    (target_dir / "CMakeLists.txt").write_text(
        f"""cmake_path(GET CMAKE_CURRENT_LIST_DIR FILENAME DIR_NAME)

add_library(${{DIR_NAME}} STATIC)
add_library(${{PROJECT_NAME}}::${{DIR_NAME}} ALIAS ${{DIR_NAME}})

include(${{CMAKE_BINARY_DIR}}/target_properties.cmake)
include(${{CMAKE_BINARY_DIR}}/target_compile_options.cmake)

target_sources(${{DIR_NAME}}
        PRIVATE
        ${{DIR_NAME}}.cpp

        PUBLIC
        FILE_SET ${{DIR_NAME}}
        TYPE HEADERS
        FILES
        ${{DIR_NAME}}/${{DIR_NAME}}.hpp
)

target_link_libraries(${{DIR_NAME}}
        PUBLIC
        ${{PROJECT_NAME}}::journal
)

if(BUILD_TESTING)
    add_subdirectory(${{DIR_NAME}}TEST)
{bench_subdir}endif()
""",
        encoding="utf-8",
    )

    (header_dir / f"{name}.hpp").write_text(
        f"""#pragma once

#include <cstddef>
#include <journal/journal.hpp>
#include <span>

namespace anvil::{name} {{

struct catalog {{
  anvil::journal::catalog_entry k_boundary_fault{{
      .message_id = "{msg_id}",
      .component = "{name}",
      .summary = "Unhandled fault caught at {name} boundary firewall"}};
}};

inline constexpr catalog k_catalog{{}};

[[nodiscard]] auto execute(std::span<const std::byte> payload) noexcept -> bool;

}} // namespace anvil::{name}
""",
        encoding="utf-8",
    )

    (target_dir / f"{name}.cpp").write_text(
        f"""#include <{name}/{name}.hpp>

namespace anvil::{name} {{

auto execute(std::span<const std::byte> payload) noexcept -> bool {{
  namespace jrn = anvil::journal;
  try {{
    jrn::log(jrn::severity::debug, jrn::message{{"{name} execute invoked"}},
             jrn::binary_payload{{payload}});
    return true;
  }} catch (...) {{
    return jrn::catch_boundary_exception(k_catalog);
  }}
}}

}} // namespace anvil::{name}
""",
        encoding="utf-8",
    )

    (target_dir / f"{name}.catalog").write_text(
        f"""-- {msg_id}
Subject: Unhandled fault caught at {name} boundary firewall
Defined-By: anvil::{name}

An unhandled exception reached the noexcept boundary of anvil::{name} and was
intercepted by the Lippincott boundary firewall.
""",
        encoding="utf-8",
    )

    (test_dir / "CMakeLists.txt").write_text(
        """cmake_path(GET CMAKE_CURRENT_LIST_DIR FILENAME DIR_NAME)
string(REGEX REPLACE "TEST$" "" COMPONENT_NAME ${DIR_NAME})

add_executable(${DIR_NAME} ${DIR_NAME}.cpp)

include(${CMAKE_BINARY_DIR}/target_properties.cmake)
include(${CMAKE_BINARY_DIR}/target_compile_options.cmake)

target_compile_features(${DIR_NAME} PRIVATE cxx_std_23)

target_compile_options(${DIR_NAME} PRIVATE
        $<$<CXX_COMPILER_ID:Clang>:-Wno-global-constructors>
)

target_link_libraries(${DIR_NAME}
        PRIVATE
        ${PROJECT_NAME}::${COMPONENT_NAME}
        PkgConfig::GTEST
)

gtest_discover_tests(${DIR_NAME})
""",
        encoding="utf-8",
    )

    (test_dir / f"{name}TEST.cpp").write_text(
        f"""#include <array>
#include <cstddef>
#include <gtest/gtest.h>
#include <{name}/{name}.hpp>

namespace {{

static_assert(anvil::journal::is_valid_catalog(anvil::{name}::k_catalog));

TEST({name}Test, ExecuteHandlesEmptyPayload) {{
  std::array<std::byte, 0U> const empty{{}};
  EXPECT_TRUE(anvil::{name}::execute(empty));
}}

}} // namespace
""",
        encoding="utf-8",
    )

    if not args.no_bench:
        (bench_dir / "CMakeLists.txt").write_text(
            """cmake_path(GET CMAKE_CURRENT_LIST_DIR FILENAME DIR_NAME)
string(REGEX REPLACE "BENCH$" "" COMPONENT_NAME ${DIR_NAME})

add_executable(${DIR_NAME} ${DIR_NAME}.cpp)

include(${CMAKE_BINARY_DIR}/target_properties.cmake)
include(${CMAKE_BINARY_DIR}/target_compile_options.cmake)

target_compile_definitions(${DIR_NAME} PRIVATE
        COMPONENT_BASELINE_PATH="${CMAKE_CURRENT_SOURCE_DIR}/baseline.json"
        COMPONENT_REPORT_PATH="${PROJECT_SOURCE_DIR}/production_artifacts/profiling/${COMPONENT_NAME}_score_report.json"
)

target_link_libraries(${DIR_NAME}
        PRIVATE
        ${PROJECT_NAME}::${COMPONENT_NAME}
        ${PROJECT_NAME}::perf_scope
)

add_test(NAME ${DIR_NAME} COMMAND ${DIR_NAME})

add_custom_target(${DIR_NAME}_run
        COMMAND $<TARGET_FILE:${DIR_NAME}>
        DEPENDS ${DIR_NAME}
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        COMMENT "Running component benchmark ${DIR_NAME} and evaluating against baseline.json"
        VERBATIM
)
""",
            encoding="utf-8",
        )

        (bench_dir / f"{name}BENCH.cpp").write_text(
            f"""#include <array>
#include <cstddef>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <{name}/{name}.hpp>
#include <perf_scope/perf_scope.hpp>
#include <system_error>

int main() {{
  namespace ps = anvil::perf_scope;

  std::array<std::byte, 64U> const payload{{}};
  auto const current_metrics = ps::measure_workload(1000U, [&payload]() {{
    (void)anvil::{name}::execute(payload);
  }});

  ps::score_baseline default_birth{{}};
  default_birth.component = "{name}";
  default_birth.birth_metrics = current_metrics;

  std::filesystem::path const baseline_path = COMPONENT_BASELINE_PATH;
  auto const baseline = ps::load_or_create_baseline(baseline_path, default_birth);
  auto const evaluation = ps::evaluate_performance(baseline, current_metrics);
  auto const report = ps::format_performance_report(baseline, evaluation);

  std::cout << report;

  std::filesystem::path const report_path = COMPONENT_REPORT_PATH;
  if (report_path.has_parent_path()) {{
    std::error_code ec;
    std::filesystem::create_directories(report_path.parent_path(), ec);
  }}
  std::ofstream out(report_path, std::ios::out | std::ios::trunc);
  if (out.is_open()) {{
    out << report;
  }}
  return 0;
}}
""",
            encoding="utf-8",
        )

    print(f"Scaffolded physical component at {target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
