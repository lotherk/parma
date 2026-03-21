# Parma - Python to SQF Transpiler

Parma is a Python-based framework for [Bohemia Interactive](https://www.bistudio.com/)'s [Armed Assault](http://arma3.com/) version 3. It provides a transpiler for converting Python code to [SQF](https://community.bistudio.com/wiki/ArmA:_Introduction_to_Scripting) scripting language, supporting object-oriented programming and modern Python features.

## Features

- **Python to SQF Transpilation**: Write ArmA scripts in Python
- **Object-Oriented Support**: Classes and methods translate to SQF equivalents
- **Modern Python**: Uses Python 3.8+ with type hints and modern tooling
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **CLI Tool**: Easy-to-use command-line interface
- **ArmA Integration**: Includes DLL for runtime Python execution

## Installation

### From Source

```bash
git clone https://github.com/lotherk/rarma.git
cd rarma
pip install -e .
```

### Using pip (future)

```bash
pip install parma
```

## Usage

### Basic Compilation

```bash
# Compile a Python file to SQF
parma compile my_script.py

# Specify output file
parma compile my_script.py -o output.sqf

# Verbose output
parma compile my_script.py --verbose
```

### Example

Create a Python script (`mission.py`):

```python
class ArmaMission:
    def __init__(self):
        self.mission_name = "Python Mission"
        self.player_count = 0

    def add_player(self, name):
        self.player_count += 1
        print(f"Player {name} joined")

    def start(self):
        if self.player_count > 0:
            print(f"Mission {self.mission_name} starting!")
        else:
            print("No players to start mission")

# Run the mission
mission = ArmaMission()
mission.add_player("Alice")
mission.start()
```

Compile to SQF:

```bash
parma compile mission.py
```

This generates `mission.py.sqf` with SQF code that uses the OOP macro system.

## DLL Integration

Parma includes `ParmaExtension.dll` for runtime Python execution in ArmA:

```sqf
// Initialize Python in SQF
"ParmaExtension" callExtension "INIT";

// Execute Python code
_result = "ParmaExtension" callExtension "EXEC print('Hello from Python!')";

// Clean up
"ParmaExtension" callExtension "CLEANUP";
```

## Docker Usage

Build and run with Docker:

```bash
# Build the image
docker build -t parma .

# Compile a file
docker run -v $(pwd):/workspace parma compile test_mission.py

# Interactive shell
docker run -it -v $(pwd):/workspace parma bash
```

## Project Structure

```
src/parma/
├── __init__.py          # Package initialization
├── cli.py               # Command-line interface
└── transpiler.py        # Core transpilation logic

dll/
├── ParmaExtension.cpp   # ArmA extension DLL
├── CMakeLists.txt       # Build configuration
└── README.md           # DLL documentation
```

## Development

### Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
flake8 src/

# Format code
black src/
```

### Building the DLL

```bash
cd dll
# Unix
./build.sh
# Windows
cmake -G "Visual Studio 16 2019" .
cmake --build . --config Release
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details