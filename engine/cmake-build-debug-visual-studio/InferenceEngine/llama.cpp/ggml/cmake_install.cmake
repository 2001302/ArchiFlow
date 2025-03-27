# Install script for directory: C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Program Files (x86)/engine")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Debug")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/Llvm/x64/bin/llvm-objdump.exe")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/source/ai engine/engine/cmake-build-debug-visual-studio/InferenceEngine/llama.cpp/ggml/src/cmake_install.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Users/source/ai engine/engine/cmake-build-debug-visual-studio/InferenceEngine/llama.cpp/ggml/src/ggml.lib")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Users/source/ai engine/engine/cmake-build-debug-visual-studio/bin/ggml.dll")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/ggml.dll" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/ggml.dll")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/Llvm/x64/bin/llvm-strip.exe" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/ggml.dll")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE FILE FILES
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-alloc.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-backend.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-blas.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-cuda.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-kompute.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-metal.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-rpc.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-sycl.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-vulkan.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Users/source/ai engine/engine/cmake-build-debug-visual-studio/InferenceEngine/llama.cpp/ggml/src/ggml.lib")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Users/source/ai engine/engine/cmake-build-debug-visual-studio/bin/ggml.dll")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/ggml.dll" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/ggml.dll")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/Llvm/x64/bin/llvm-strip.exe" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/ggml.dll")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE FILE FILES
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-alloc.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-backend.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-blas.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-cuda.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-kompute.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-metal.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-rpc.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-sycl.h"
    "C:/Users/source/ai engine/engine/InferenceEngine/llama.cpp/ggml/include/ggml-vulkan.h"
    )
endif()

