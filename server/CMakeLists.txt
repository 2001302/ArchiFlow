cmake_minimum_required(VERSION 3.30)
project(Server)

add_subdirectory(Llama.cpp)
add_subdirectory(InferenceEngine)
add_subdirectory(Backend)
add_subdirectory(UnitTest)