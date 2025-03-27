cmake_minimum_required(VERSION 3.30)
project(InferenceEngine)

set(CMAKE_CXX_STANDARD 20)

add_library(InferenceEngine STATIC library.cpp)
add_subdirectory(llama.cpp)