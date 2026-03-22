#!/bin/bash
# Build script for Parma using Docker

set -e

usage() {
    echo "Usage: $0 [simple|full|cross]"
    echo "  simple - Build Parma transpiler only (no DLL)"
    echo "  full   - Build Parma with SQFVM testing support"
    echo "  cross  - Build with cross-compilation for Windows DLL (experimental)"
    exit 1
}

BUILD_TYPE=${1:-simple}

case $BUILD_TYPE in
    simple)
        echo "Building Parma transpiler with Docker (simple mode)..."
        docker build -f Dockerfile.simple -t parma:latest .
        IMAGE_NAME="parma:latest"
        ;;
    full)
        echo "Building Parma with Docker (full mode with SQFVM testing)..."
        docker build -f Dockerfile.full -t parma-full:latest .
        IMAGE_NAME="parma-full:latest"
        ;;
    cross)
        echo "Building Parma with Docker (cross-compilation mode)..."
        echo "Note: Cross-compilation is experimental and may not work perfectly."
        docker build -f Dockerfile.cross -t parma-cross:latest .
        IMAGE_NAME="parma-cross:latest"
        ;;
    *)
        usage
        ;;
esac

echo "Build complete!"
echo ""
echo "To run Parma transpiler:"
echo "docker run -it --rm $IMAGE_NAME parma --help"
echo ""
echo "To compile a Python file:"
echo "docker run -it --rm -v \$(pwd):/workspace $IMAGE_NAME parma compile /workspace/your_file.py"
echo ""

if [ "$BUILD_TYPE" = "cross" ]; then
    echo "To extract the built DLLs (if successful):"
    echo "mkdir -p output"
    echo "docker run -it --rm -v \$(pwd)/output:/output $IMAGE_NAME cp /app/dll/build/ParmaExtension.dll /output/ 2>/dev/null || echo '64-bit DLL not found'"
    echo "docker run -it --rm -v \$(pwd)/output:/output $IMAGE_NAME cp /app/dll/build32/ParmaExtension.dll /output/ParmaExtension32.dll 2>/dev/null || echo '32-bit DLL not found'"
    echo ""
    echo "DLLs will be available in ./output/ directory"
fi