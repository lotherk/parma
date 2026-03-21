#!/bin/bash
# Build script for ParmaExtension DLL

echo "Building ParmaExtension DLL..."

# Check if we're on Windows
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Windows detected - using MSVC"

    # Create build directory
    mkdir -p build
    cd build

    # Use CMake with Visual Studio generator
    cmake -G "Visual Studio 16 2019" ..
    cmake --build . --config Release

else
    echo "Unix-like system detected - using gcc"

    # Check for required tools
    command -v g++ >/dev/null 2>&1 || { echo "g++ not found. Please install g++."; exit 1; }
    command -v python3-config >/dev/null 2>&1 || { echo "python3-config not found. Please install Python development headers."; exit 1; }

    # Get Python includes and libs
    PYTHON_INCLUDES=$(python3-config --includes)
    PYTHON_LIBS=$(python3-config --libs)

    echo "Python includes: $PYTHON_INCLUDES"
    echo "Python libs: $PYTHON_LIBS"

    # Compile
    g++ -shared -fPIC \
        -o ParmaExtension.dll \
        ParmaExtension.cpp \
        $PYTHON_INCLUDES \
        $PYTHON_LIBS \
        -Wl,--add-stdcall-alias

    echo "Build complete: ParmaExtension.dll"
fi