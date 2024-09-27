cmake_minimum_required(VERSION 3.20)

project(ViVoAc_Plugin)

set(CMAKE_CXX_STANDARD 23)

# All warning should be treated as errors
if(MSVC)
    add_compile_options(/W4 /WX)
    add_definitions(-DDETOURS_X86 -DDETOURS_32BIT)

else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# CPM
set(LIB_DIR ${CMAKE_CURRENT_SOURCE_DIR}/libs)
include(cmake/CPM.cmake)

# Add packages
CPMAddPackage(
  NAME JUCE
  GITHUB_REPOSITORY juce-framework/JUCE
  GIT_TAG 8.0.1
  VERSION 8.0.1
  SOURCE_DIR ${LIB_DIR}/juce
)

# add config
include("${CMAKE_SOURCE_DIR}/config.cmake")

# Add the plugin
add_subdirectory(vivoac_plugin)

