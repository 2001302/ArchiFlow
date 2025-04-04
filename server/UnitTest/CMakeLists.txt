cmake_minimum_required(VERSION 3.30)
project(UnitTest)

#set vcpkg path
set(CMAKE_PREFIX_PATH "${CMAKE_SOURCE_DIR}/../vcpkg/vcpkg_installed/x64-windows")

#logging
message(STATUS "GTest_DIR = ${GTest_DIR}")
find_package(GTest CONFIG REQUIRED)

add_executable (UnitTest
        test.h
        test.cpp)

target_link_libraries(UnitTest PRIVATE GTest::gtest GTest::gtest_main)