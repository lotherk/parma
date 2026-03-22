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
    echo "Unix-like system detected"

    # Check if cross-compiling for Windows
    if command -v x86_64-w64-mingw32-g++ >/dev/null 2>&1; then
        echo "MinGW detected - cross-compiling for Windows"

        # Check for Python cross-compilation support (this may need adjustment)
        PYTHON_INCLUDES="-I/usr/x86_64-w64-mingw32/include/python3.9"  # Adjust version as needed
        PYTHON_LIBS="-L/usr/x86_64-w64-mingw32/lib -lpython39"  # Adjust version as needed

        echo "Using cross-compilation includes: $PYTHON_INCLUDES"
        echo "Using cross-compilation libs: $PYTHON_LIBS"

        # Cross-compile for Windows
        x86_64-w64-mingw32-g++ -shared \
            -o ParmaExtension.dll \
            ParmaExtension.cpp \
            $PYTHON_INCLUDES \
            $PYTHON_LIBS \
            -Wl,--add-stdcall-alias

        echo "Cross-compilation complete: ParmaExtension.dll"

    elif command -v g++ >/dev/null 2>&1; then
        echo "Building on Linux with g++ (note: this will create a Linux .so file, not Windows .dll)"

        # Check for required tools
        command -v python3-config >/dev/null 2>&1 || { echo "python3-config not found. Please install Python development headers."; exit 1; }

        # Get Python includes and libs
        PYTHON_INCLUDES=$(python3-config --includes)
        PYTHON_LIBS=$(python3-config --libs)

        echo "Python includes: $PYTHON_INCLUDES"
        echo "Python libs: $PYTHON_LIBS"

        # Compile (will create .so instead of .dll)
        g++ -shared -fPIC \
            -o ParmaExtension.so \
            ParmaExtension.cpp \
            $PYTHON_INCLUDES \
            $PYTHON_LIBS

        echo "Build complete: ParmaExtension.so (Linux shared library)"
        echo "Note: For ArmA 3 (Windows), you need to cross-compile with MinGW or build on Windows"

    else
        echo "No suitable compiler found. Please install g++ or MinGW-w64."
        exit 1
    fi
fi