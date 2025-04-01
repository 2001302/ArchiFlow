cmake_minimum_required(VERSION 3.30)
project(engine)

set(CMAKE_CXX_STANDARD 20)

add_subdirectory(InferenceEngine)
add_subdirectory(Backend)

add_executable(engine main.cpp
)
