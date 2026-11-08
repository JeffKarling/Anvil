# Local CMake target overrides and code generation patterns

Always include both `target_properties.cmake` and `target_compile_options.cmake` immediately after `add_library`. Apply local overrides directly below those includes.

## Strict IEEE 754 floating point semantics

Custom release presets pass `-ffast-math`. Append `-fno-fast-math` when a target requires strict NaN, infinity, or IEEE 754 rounding behavior.

```cmake
target_compile_options(${DIR_NAME} PRIVATE
        $<$<CONFIG:Clang_Release,Clang_RelWithDebInfo,GNU_Release>:-fno-fast-math>
)
```

## Private language standard adoption

A component can compile its private translation unit with a newer C++ standard while keeping its public header on the baseline standard.

```cmake
target_compile_features(${DIR_NAME} PRIVATE cxx_std_23)
```

## Localized SIMD instruction sets

Enable hardware specific vector instructions privately on compute kernels without affecting neighboring components.

```cmake
target_compile_options(${DIR_NAME} PRIVATE
        $<$<CXX_COMPILER_ID:Clang>:-mavx2 -mfma>
        $<$<CXX_COMPILER_ID:GNU>:-mavx2 -mfma>
)
```

## Machine generated Protobuf target recipe

When creating a dedicated schema component for `.proto` files, suppress compiler warnings on generated code and disable static analysis on the target while retaining global hardening and optimization flags.

```cmake
cmake_path(GET CMAKE_CURRENT_LIST_DIR FILENAME DIR_NAME)

add_library(${DIR_NAME} STATIC)
add_library(${PROJECT_NAME}::${DIR_NAME} ALIAS ${DIR_NAME})

include(${CMAKE_BINARY_DIR}/target_properties.cmake)
include(${CMAKE_BINARY_DIR}/target_compile_options.cmake)

target_compile_options(${DIR_NAME} PRIVATE
        $<$<CXX_COMPILER_ID:Clang>:-Wno-global-constructors -Wno-conversion -Wno-sign-conversion>
        $<$<CXX_COMPILER_ID:GNU>:-Wno-conversion -Wno-sign-conversion>
)

add_custom_command(
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${DIR_NAME}/${DIR_NAME}.proto
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_BINARY_DIR}/${DIR_NAME}
        OUTPUT
            ${CMAKE_CURRENT_BINARY_DIR}/${DIR_NAME}/${DIR_NAME}.pb.cc
            ${CMAKE_CURRENT_BINARY_DIR}/${DIR_NAME}/${DIR_NAME}.pb.h
        COMMENT "Generating ${DIR_NAME} C++ header and translation unit from ${DIR_NAME}.proto"
        COMMAND ${PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR}/${DIR_NAME} ${DIR_NAME}.proto --cpp_out=${CMAKE_CURRENT_BINARY_DIR}/${DIR_NAME}
        VERBATIM
)

target_sources(${DIR_NAME}
        PRIVATE
        ${CMAKE_CURRENT_BINARY_DIR}/${DIR_NAME}/${DIR_NAME}.pb.cc

        PUBLIC
        FILE_SET ${DIR_NAME}
        TYPE HEADERS
        BASE_DIRS ${CMAKE_CURRENT_BINARY_DIR}
        FILES
        ${CMAKE_CURRENT_BINARY_DIR}/${DIR_NAME}/${DIR_NAME}.pb.h
)

set_target_properties(${DIR_NAME} PROPERTIES
        SYSTEM ON
        CXX_CLANG_TIDY ""
        CXX_INCLUDE_WHAT_YOU_USE ""
        CXX_CPPCHECK ""
)

target_link_libraries(${DIR_NAME}
        PUBLIC
        PkgConfig::protobuf
)
```
