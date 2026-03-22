cmake_minimum_required(VERSION 3.10)
project(ParmaExtension)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python - handle cross-compilation
if(CMAKE_CROSSCOMPILING)
    # For cross-compilation, we need to manually specify Python paths
    # These should be set in the toolchain file
    if(NOT PYTHON_INCLUDE_DIR OR NOT PYTHON_LIBRARY)
        message(FATAL_ERROR "For cross-compilation, PYTHON_INCLUDE_DIR and PYTHON_LIBRARY must be set in the toolchain file")
    endif()

    # Check if the paths exist
    if(NOT EXISTS "${PYTHON_INCLUDE_DIR}")
        message(FATAL_ERROR "Python include directory not found: ${PYTHON_INCLUDE_DIR}")
    endif()
    if(NOT EXISTS "${PYTHON_LIBRARY}")
        message(FATAL_ERROR "Python library not found: ${PYTHON_LIBRARY}")
    endif()

    set(Python3_INCLUDE_DIRS "${PYTHON_INCLUDE_DIR}")
    set(Python3_LIBRARIES "${PYTHON_LIBRARY}")
else()
    # Native build
    find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
endif()

# Include directories
include_directories(${Python3_INCLUDE_DIRS})

# Source files
set(SOURCES
    ParmaExtension.cpp
)

# Create shared library
add_library(ParmaExtension SHARED ${SOURCES})

# Link Python libraries
target_link_libraries(ParmaExtension ${Python3_LIBRARIES})

# Set target properties
if(WIN32 OR CMAKE_CROSSCOMPILING)
    # Windows DLL
    set_target_properties(ParmaExtension PROPERTIES
        SUFFIX ".dll"
        PREFIX ""
    )
elseif(UNIX)
    # Unix shared library
    set_target_properties(ParmaExtension PROPERTIES
        SUFFIX ".so"
        PREFIX "lib"
    )
endif()

# Install
install(TARGETS ParmaExtension
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)