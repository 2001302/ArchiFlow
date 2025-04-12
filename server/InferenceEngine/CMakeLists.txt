cmake_minimum_required(VERSION 3.30)
project(InferenceEngine)

add_library(InferenceEngine STATIC
        Include/AlgorithmicObject.h
        Src/AlgorithmicObject.cpp
        Src/Tokenizer.cpp
        Include/Tokenizer.h
        Src/InferenceProcessingBase.cpp
        Include/InferenceProcessingBase.h
        Src/AiModelHandler.cpp
        Include/AiModelHandler.h
)

target_include_directories(InferenceEngine PUBLIC Include)

# include directory
target_include_directories(InferenceEngine PUBLIC
        ${CMAKE_SOURCE_DIR}/vcpkg/vcpkg_installed/x64-windows/include
)
# library link
target_link_directories(InferenceEngine PRIVATE
        ${CMAKE_SOURCE_DIR}/vcpkg/vcpkg_installed/x64-windows/lib
)
# library name
# target_link_libraries(InferenceEngine PRIVATE onnxruntime)

#logging
get_target_property(INCLUDE_DIRS InferenceEngine INCLUDE_DIRECTORIES)
message(STATUS "Final include dirs for InferenceEngine: ${INCLUDE_DIRS}")