cmake_minimum_required(VERSION 3.30)
project(InferenceEngine)

add_library(InferenceEngine STATIC
        Include/AlgorithmicObject.h
        Src/AlgorithmicObject.cpp)

target_include_directories(InferenceEngine PUBLIC Include)

target_compile_options(InferenceEngine PRIVATE -Wall -Werror)