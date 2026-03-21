cmake_minimum_required(VERSION 3.10)
project(ParmaExtension)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Include directories
include_directories(${Python3_INCLUDE_DIRS})

# Source files
set(SOURCES
    ParmaExtension.cpp
)

# Create DLL
add_library(ParmaExtension SHARED ${SOURCES})

# Link Python libraries
target_link_libraries(ParmaExtension ${Python3_LIBRARIES})

# Set target properties for Windows DLL
if(WIN32)
    set_target_properties(ParmaExtension PROPERTIES
        SUFFIX ".dll"
        PREFIX ""
    )
endif()

# Install
install(TARGETS ParmaExtension
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)