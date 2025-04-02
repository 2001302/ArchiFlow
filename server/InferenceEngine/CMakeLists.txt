add_library(InferenceEngine STATIC
        AlgorithmicObject.h
        AlgorithmicObject.cpp)

target_include_directories(InferenceEngine PUBLIC ${CMAKE_SOURCE_DIR})

target_compile_options(InferenceEngine PRIVATE -Wall -Werror)