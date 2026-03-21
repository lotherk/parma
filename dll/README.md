# ParmaExtension - ArmA Python DLL

This DLL allows ArmA 3 to execute Python code through the `callExtension` command.

## Features

- **Python Integration**: Execute Python code from within ArmA SQF scripts
- **Embedded Interpreter**: Python interpreter runs inside the DLL
- **SQF Interface**: Clean interface through ArmA's callExtension

## Building

### Prerequisites

- **Windows**: Visual Studio with C++ support, Python development headers
- **Linux**: g++, Python development headers (`python3-dev`)

### Build Commands

```bash
# Unix/Linux
./build.sh

# Windows (from build directory)
cmake -G "Visual Studio 16 2019" ..
cmake --build . --config Release
```

## Installation

1. Copy `ParmaExtension.dll` to your ArmA 3 server directory
2. The DLL will be loaded automatically when ArmA starts

## Usage in SQF

```sqf
// Initialize Python
_result = "ParmaExtension" callExtension "INIT";

// Execute Python code
_result = "ParmaExtension" callExtension "EXEC print('Hello from Python!')";

// Execute Python expressions
_result = "ParmaExtension" callExtension "EVAL 2 + 2";

// Cleanup
_result = "ParmaExtension" callExtension "CLEANUP";
```

## Parma Integration

This DLL is designed to work with Parma (Python to SQF transpiler). You can:

1. Write Python code
2. Transpile to SQF using Parma
3. Use the SQF to call Python functions via this DLL

Example workflow:
```python
# Python code
def calculate_damage(base_damage, armor):
    return base_damage * (1 - armor / 100)

# Transpile to SQF with Parma
# Then in SQF:
_damage = "ParmaExtension" callExtension ("EXEC result = calculate_damage(" + str(_base) + ", " + str(_armor) + ")");
```

## Security Notes

⚠️ **Warning**: This DLL executes arbitrary Python code. Only use in trusted environments!

- The DLL has full access to the system
- Python code can execute system commands
- Use only in development or trusted server environments

## Troubleshooting

- **"Python not found"**: Ensure Python is installed and DLL can find python3.dll
- **"Extension not loaded"**: Check that DLL is in the correct ArmA directory
- **"Command failed"**: Check ArmA server logs for detailed error messages

## Development

The DLL embeds Python interpreter and provides a simple command interface:

- `INIT`: Initialize Python interpreter
- `EXEC <code>`: Execute Python code
- `EVAL <expr>`: Evaluate Python expression
- `CLEANUP`: Clean up interpreter

For more advanced features, modify `ParmaExtension.cpp` and rebuild.