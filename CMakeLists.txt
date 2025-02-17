cmake_minimum_required(VERSION 3.1)

project(KVDK VERSION 1.0
        DESCRIPTION "A fast persistent KV engine for Persistent Memory"
        LANGUAGES CXX)

set(KVDK_ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
include(${KVDK_ROOT_DIR}/cmake/functions.cmake)

set_property(GLOBAL PROPERTY CXX_STANDARD 14)
set(OPT "-msse4 -mavx -mavx2 -O2 -fno-omit-frame-pointer -momit-leaf-frame-pointer")

if (CMAKE_BUILD_TYPE STREQUAL "Release")
    set(FLAGS "-g -DNDEBUG ${OPT}")
else ()
    set(FLAGS "-g ")
endif ()

set(CMAKE_CXX_FLAGS "${FLAGS}")

# source files
set(SOURCES
        engine/engine.cpp
        engine/kv_engine.cpp
        engine/logger.cpp
        engine/hash_table.cpp
        engine/skiplist.cpp
        engine/write_batch.cpp
        engine/hash_list.cpp
        engine/dram_allocator.cpp
        engine/pmem_allocator/pmem_allocator.cpp
        engine/thread_manager.cpp
        engine/utils.cpp
        engine/pmem_allocator/free_list.cpp)


# .a library
add_library(engine SHARED ${SOURCES})
target_include_directories(engine PUBLIC ./include ./extern)
target_link_libraries(engine PUBLIC pthread pmem gflags hwloc)

# executables
add_executable(bench benchmark/bench.cpp)
target_link_libraries(bench PUBLIC engine)

option(BUILD_TESTING "Build the tests" ON)
if (BUILD_TESTING)
    set(TEST_SOURCES tests/tests.cpp)
    enable_testing()
    include(GoogleTest)
    add_subdirectory(extern/gtest)
    add_executable(dbtest ${TEST_SOURCES})
    target_link_libraries(dbtest PUBLIC engine gtest gmock gtest_main)
endif ()

option(BUILD_TUTORIAL "Build the tutorial" ON)
if (BUILD_TUTORIAL)
    set(TUTORIAL_SOURCES examples/tutorial.cpp)
    add_executable(dbtutorial ${TUTORIAL_SOURCES})
    target_link_libraries(dbtutorial PUBLIC engine)
endif ()

add_custom_target(checkers ALL)
add_custom_target(cppstyle)
add_custom_target(cppformat)

find_program(CLANG_FORMAT NAMES clang-format-9 clang-format-9.0 clang-format)
set(CLANG_FORMAT_MINIMUM_REQUIRED "9.0")
if (CLANG_FORMAT)
    get_program_version_major_minor(${CLANG_FORMAT} CLANG_FORMAT_VERSION)
    message(STATUS "Found clang-format: ${CLANG_FORMAT} (version: ${CLANG_FORMAT_VERSION})")
endif ()

if (CHECK_CPP_STYLE)
    if (CLANG_FORMAT)
        if (NOT (CLANG_FORMAT_VERSION VERSION_GREATER_EQUAL CLANG_FORMAT_MINIMUM_REQUIRED))
            message(FATAL_ERROR "minimum required clang-format version is ${CCLANG_FORMAT_MINIMUM_REQUIRED}")
        endif ()
    else ()
        message(FATAL_ERROR "CHECK_CPP_STYLE=ON, but clang-format not found (required version: ${CLANG_FORMAT_MINIMUM_REQUIRED})")
    endif ()

    add_dependencies(checkers cppstyle)
endif ()

add_cppstyle(src ${CMAKE_CURRENT_SOURCE_DIR}/engine/*.c*
        ${CMAKE_CURRENT_SOURCE_DIR}/engine/*.h*
        ${CMAKE_CURRENT_SOURCE_DIR}/examples/*.c*
        ${CMAKE_CURRENT_SOURCE_DIR}/benchmark/*.c*
        ${CMAKE_CURRENT_SOURCE_DIR}/include/kvdk/*.h*
        ${CMAKE_CURRENT_SOURCE_DIR}/tests/*.c*
        ${CMAKE_CURRENT_SOURCE_DIR}/tests/*.h*)
