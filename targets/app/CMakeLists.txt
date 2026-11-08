cmake_path(GET CMAKE_CURRENT_LIST_DIR FILENAME DIR_NAME)

add_executable(${DIR_NAME} ${DIR_NAME}.cpp)

include(${CMAKE_BINARY_DIR}/target_properties.cmake)
include(${CMAKE_BINARY_DIR}/target_compile_options.cmake)

target_compile_features(${DIR_NAME} PRIVATE cxx_std_23)

target_link_libraries(${DIR_NAME}
        PRIVATE
        ${PROJECT_NAME}::journal
        ${PROJECT_NAME}::journal_signal_adapter
)
