cmake_minimum_required(VERSION 2.6)
project(clippingSSBDVideos)

set(CMAKE_VERBOSE_MAKEFILE OFF)

# Print compiler and CMake information
MESSAGE(STATUS "CMAKE_C_COMPILER: ${CMAKE_C_COMPILER}")
MESSAGE(STATUS "CMAKE_CXX_COMPILER: ${CMAKE_CXX_COMPILER}")
MESSAGE(STATUS "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
MESSAGE(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")

# OpenCV Configuration
include_directories(~/local/include)
link_directories(~/local/lib)

find_package(OpenCV REQUIRED HINTS ~/local)
MESSAGE(STATUS "OpenCV version: ${OpenCV_VERSION}")
MESSAGE(STATUS "OpenCV libs: ${OpenCV_LIBS}")

# Boost Configuration
include_directories(/usr/local/include)
link_directories(/usr/local/lib)

# C++ and linker flags
list(APPEND CMAKE_CXX_FLAGS "-std=c++11 -pipe -D__STDC_CONSTANT_MACROS -DSTD=std -Wall -O3 -DNDEBUG -ggdb ${CMAKE_CXX_FLAGS}")

# Add executable for clippingSSBDVideos
add_executable(${PROJECT_NAME} clipping.cpp)
target_link_libraries(${PROJECT_NAME} 
    opencv_core 
    opencv_highgui 
    opencv_video 
    opencv_videoio 
    boost_filesystem 
    boost_system
)

# Add executable for clip_segment
add_executable(clip_segment clip_segment.cpp)
target_link_libraries(clip_segment 
    opencv_core 
    opencv_highgui 
    opencv_video 
    opencv_videoio 
    boost_filesystem 
    boost_system
)
