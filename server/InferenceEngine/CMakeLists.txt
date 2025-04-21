cmake_minimum_required(VERSION 3.30)
project(InferenceEngine)

add_library(InferenceEngine STATIC
        Src/AlgorithmicObject.h
        Src/AlgorithmicObject.cpp
        Src/ProcessingBase.cpp
        Src/ProcessingBase.h
        Src/AiModelHandler.cpp
        Src/AiModelHandler.h
        Src/ProcessingTextGeneraor.cpp
        Src/ProcessingTextGeneraor.h
        Src/ProcessingImageGenerator.cpp
        Src/ProcessingImageGenerator.h
)

target_include_directories(InferenceEngine PUBLIC Include)

# include directory
target_include_directories(InferenceEngine PUBLIC
        ${CMAKE_SOURCE_DIR}/Llama.cpp/include
)

# library link
target_link_directories(InferenceEngine PRIVATE
        ${CMAKE_BINARY_DIR}/Llama.cpp/src
)

# library name
target_link_libraries(InferenceEngine PRIVATE llama)

#logging
get_target_property(INCLUDE_DIRS InferenceEngine INCLUDE_DIRECTORIES)
message(STATUS "Final include dirs for InferenceEngine: ${INCLUDE_DIRS}")