# Parma Technical Reference Manual

## Overview

Parma is a sophisticated Python-to-SQF transpiler designed for creating ArmA 3 missions and mods. It allows developers to write game logic in Python and automatically converts it to SQF (ArmA's scripting language) with full validation and testing capabilities.

## Architecture

### Core Components

```
Parma System Architecture
├── CLI Interface (parma command)
├── Transpiler Engine (AST-based conversion)
├── Game Framework (Python classes for ArmA entities)
├── SQFVM Integration (Automated testing)
├── Build System (Docker-based cross-compilation)
└── Validation Pipeline (Syntax and logic checking)
```

### Data Flow

1. **Input**: Python source code with game logic
2. **Parsing**: AST analysis of Python syntax
3. **Transpilation**: Conversion to SQF equivalents
4. **Validation**: SQFVM testing (optional)
5. **Output**: Production-ready SQF files

## Supported Python Features

### Core Language Features

#### Data Types
- **Numbers**: `int`, `float` → SQF numbers
- **Strings**: `"text"` → SQF strings with proper escaping
- **Booleans**: `True`/`False` → SQF `true`/`false`
- **None**: → SQF `nil`
- **Lists**: `[1, 2, 3]` → SQF arrays `[1, 2, 3]`
- **Dictionaries**: `{"key": "value"}` → SQF arrays `[["key", "value"]]`

#### Control Flow
```python
# if/elif/else
if condition:
    action()
elif other_condition:
    other_action()
else:
    default_action()

# for loops
for i in range(10):
    do_something(i)

for item in items:
    process(item)

# while loops
while condition:
    update()

# try/except (converted to comments)
try:
    risky_operation()
except Exception as e:
    handle_error(e)
```

### Mathematical Operations

#### Basic Math
```python
result = x + y      # → (x + y)
result = x - y      # → (x - y)
result = x * y      # → (x * y)
result = x / y      # → (x / y)
result = x % y      # → (x % y)
result = x ** y     # → (x ^ y)
```

#### Math Library Functions
```python
import math

# Trigonometry
angle_rad = math.sin(1.57)     # → sin((1.57 * 180 / 3.14159265359))
angle_deg = math.cos(45)       # → cos((45 * 180 / 3.14159265359))
atan_result = math.atan2(y, x) # → atan2(y, x)

# Rounding
floor_val = math.floor(3.7)    # → floor(3.7)
ceil_val = math.ceil(3.2)      # → ceil(3.2)

# Powers and roots
sqrt_val = math.sqrt(16)       # → sqrt(16)
pow_val = math.pow(2, 3)       # → (2 ^ 3)
exp_val = math.exp(1)          # → exp(1)
log_val = math.log(10)         # → ln(10)

# Constants
pi_val = math.pi               # → 3.14159265359
e_val = math.e                 # → 2.71828182846
```

### Random Number Generation

```python
import random

# Basic random
value = random.random()        # → random(1) (0.0 to 1.0)
value = random.uniform(10, 20) # → 10 + (random(10))

# Integer ranges
dice_roll = random.randint(1, 6)  # → 1 + floor(random(6))

# Selections
choice = random.choice(items)  # → items select floor(random(count items))

# Unsupported (marked as warnings)
random.seed(42)               # → // Warning: random.seed() not supported in SQF
random.shuffle(my_list)       # → // Warning: random.shuffle() not supported in SQF
```

### String Operations

```python
# String literals
message = "Hello World"       # → "Hello World"

# Concatenation
full_name = first + " " + last  # → ((first + " ") + last)

# String methods (limited support)
# Most string operations are converted to SQF equivalents where possible
```

### Functions and Classes

#### Function Definitions
```python
def calculate_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance."""
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx*dx + dy*dy)

# Converts to:
# PUBLIC FUNCTION("any","calculate_distance") {
#     dx = (x2 - x1);
#     dy = (y2 - y1);
#     sqrt((dx * dx) + (dy * dy))
# };
```

#### Class Definitions
```python
class GameObject:
    def __init__(self, position):
        self.position = position
        self.active = True

    def update(self):
        if self.active:
            self.do_update()

# Converts to SQF class system using macros
```

## Game Framework API

### Vector3 Class

```python
from game_framework import Vector3

# Creation
pos = Vector3(100, 200, 50)
origin = Vector3(0, 0, 0)

# Operations
direction = pos - origin                    # Vector subtraction
distance = pos.distance(origin)             # Euclidean distance
normalized = direction.normalize()          # Unit vector
moved_pos = pos + direction                 # Vector addition

# Access
x, y, z = pos.x, pos.y, pos.z
```

### Unit Class

```python
from game_framework import Unit

# Creation
soldier = Unit(Vector3(100, 100, 0), "B_soldier_F", "military")

# Properties
soldier.health = 100
soldier.speed = 5.0
soldier.faction = "player"

# Movement
soldier.move_to(target_position)

# Combat
soldier.attack(enemy_unit)

# Waypoints
soldier.waypoints = [
    Vector3(200, 200, 0),
    Vector3(300, 300, 0),
    Vector3(400, 400, 0)
]
```

### Building Class

```python
from game_framework import Building

# Creation
house = Building(Vector3(150, 150, 0), "Land_House_Small_01_F", Vector3(10, 10, 5))

# Properties
house.building_type = "residential"
house.size = Vector3(10, 10, 5)  # width, length, height
```

### World Management

```python
from game_framework import World

world = World()

# Add objects
world.add_object(unit)
world.add_object(building)

# Spatial queries
nearby_units = world.get_units_in_radius(position, 500.0)
nearest_enemy = world.find_nearest_unit(position, "enemy")

# Advanced queries
military_units = world.get_units_in_radius_by_factions(position, 300, ["military", "player"])

# Update all objects
world.update(delta_time)
```

### Game Manager

```python
from game_framework import GameManager

game = GameManager()
game.initialize_game()

# Main game loop
while game.game_running:
    game.update_game(delta_time)

    # Custom logic
    update_ai()
    check_win_conditions()
    spawn_enemies()

# Game state
state = game.get_game_state()
print(f"Score: {state['score']}, Units: {state['unit_count']}")
```

## CLI Interface

### Basic Usage

```bash
# Compile Python to SQF
parma compile input.py

# Specify output file
parma compile input.py -o output.sqf

# Enable verbose output
parma compile input.py --verbose

# Test with SQFVM
parma compile input.py --test

# Get help
parma --help
parma compile --help
```

### Command Reference

#### `parma compile [OPTIONS] INPUT_FILE`

**Options:**
- `-o, --output PATH`: Output SQF file path (default: input.sqf)
- `--verbose`: Enable verbose output
- `--test`: Test generated SQF with SQFVM

**Examples:**
```bash
# Basic compilation
parma compile my_game.py

# With testing and verbose output
parma compile my_game.py --test --verbose

# Custom output location
parma compile src/game.py -o missions/game.sqf
```

## Build System

### Docker Builds

#### Simple Build (Python only)
```bash
./build-docker.sh simple
```
- Builds Parma transpiler
- No SQFVM or cross-compilation
- Fastest build option

#### Full Build (with SQFVM)
```bash
./build-docker.sh full
```
- Includes SQFVM for testing
- Validates generated SQF code
- Recommended for development

#### Cross-Compilation Build
```bash
./build-docker.sh cross
```
- Cross-compiles Windows DLL
- Experimental SQFVM support
- For advanced ArmA integration

### Manual Installation

```bash
# Clone repository
git clone https://github.com/lotherk/parma.git
cd parma

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Use Parma
parma --help
```

## Transpilation Process

### AST Analysis

Parma uses Python's Abstract Syntax Tree (AST) to analyze source code:

1. **Parse**: Convert Python source to AST
2. **Visit**: Traverse AST nodes with custom visitors
3. **Transform**: Convert Python constructs to SQF equivalents
4. **Generate**: Output SQF code with proper formatting

### Node Transformations

#### Function Calls
```python
print("Hello")  # → diag_log "Hello";
len(items)      # → count items
range(5)        # → [0,1,2,3,4]
```

#### Variable Handling
```python
x = 42          # → x = 42;
my_var = value  # → my_var = value;
```

#### Control Structures
```python
if x > 0:       # → if (x > 0) then {
    action()    # →     action();
               # → };
```

### SQF Code Generation

Generated SQF includes:
- **Header**: Version and generation info
- **Includes**: Required macro files
- **Functions**: PUBLIC FUNCTION wrappers
- **Variables**: Properly scoped variables
- **Comments**: Preserved Python docstrings and comments

## SQFVM Integration

### Automatic Testing

When `--test` flag is used:

1. **Generate SQF** from Python source
2. **Create test wrapper** with SQFVM-compatible format
3. **Execute with SQFVM** to validate syntax
4. **Report results** - success or detailed error messages

### Test Output

```bash
$ parma compile my_game.py --test
✓ Compiled my_game.py → my_game.sqf
✓ SQFVM test passed
```

### Error Handling

If SQFVM detects issues:
```bash
⚠ SQFVM test completed with warnings:
[Error] Line 15: Undefined variable 'missing_var'
```

## Examples and Patterns

### Basic Mission Script

```python
def init_mission():
    """Initialize the mission."""
    print("Mission starting...")

    # Create player
    player = Unit(Vector3(5000, 5000, 0), "B_soldier_F", "player")

    # Create objectives
    create_objectives()

    print("Mission initialized")

def create_objectives():
    """Set up mission objectives."""
    # Kill 10 enemies
    # Capture the base
    # Extract safely
    pass

def check_win_condition():
    """Check if mission is complete."""
    # Return True if won, False otherwise
    return False

# Mission entry point
if __name__ == "__main__":
    init_mission()
```

### AI Behavior System

```python
def update_enemy_ai(enemy, player):
    """Update enemy AI behavior."""
    distance = enemy.position.distance(player.position)

    if distance < 50:
        # Close range - attack
        enemy.attack(player)
    elif distance < 300:
        # Medium range - move towards player
        enemy.move_to(player.position)
    else:
        # Long range - patrol randomly
        patrol_x = enemy.position.x + random.uniform(-100, 100)
        patrol_y = enemy.position.y + random.uniform(-100, 100)
        enemy.move_to(Vector3(patrol_x, patrol_y, 0))

def update_all_ai(world, player):
    """Update AI for all enemies."""
    for unit in world.units:
        if unit.faction == "enemy":
            update_enemy_ai(unit, player)
```

### City Generation

```python
def generate_city(world, center, radius):
    """Generate a procedural city."""
    buildings = [
        "Land_House_Small_01_F",
        "Land_House_Small_02_F",
        "Land_Office_01_F",
        "Land_Shop_01_F"
    ]

    # Create grid of buildings
    grid_size = int(radius / 60)
    for x in range(-grid_size, grid_size):
        for y in range(-grid_size, grid_size):
            if random.random() < 0.7:  # 70% chance
                pos_x = center.x + x * 70 + random.uniform(-20, 20)
                pos_y = center.y + y * 70 + random.uniform(-20, 20)

                building_type = random.choice(buildings)
                building = Building(Vector3(pos_x, pos_y, 0), building_type, Vector3(15, 15, 8))
                world.add_object(building)

    # Add civilians
    for _ in range(20):
        civilian_pos = Vector3(
            center.x + random.uniform(-radius, radius),
            center.y + random.uniform(-radius, radius),
            0
        )
        civilian = Unit(civilian_pos, "C_man_1", "civilian")
        world.add_object(civilian)
```

## API Reference

### Transpiler Functions

#### `transpile_python_to_sqf(source_code: str) -> str`
Main transpilation function.

**Parameters:**
- `source_code`: Python source code as string

**Returns:**
- SQF code as string

**Example:**
```python
from parma.transpiler import transpile_python_to_sqf

python_code = "print('Hello')"
sqf_code = transpile_python_to_sqf(python_code)
# Result: diag_log "Hello";
```

### CLI Functions

#### `main()`
Entry point for command-line interface.

### Game Framework Classes

#### `Vector3(x: float, y: float, z: float)`
3D vector class for positions and directions.

**Methods:**
- `__add__(other)`: Vector addition
- `__sub__(other)`: Vector subtraction
- `distance(other)`: Euclidean distance
- `normalize()`: Return unit vector

#### `GameObject(position: Vector3, object_type: str)`
Base class for all game objects.

**Attributes:**
- `position`: Vector3 position
- `object_type`: Type identifier
- `active`: Whether object is active

**Methods:**
- `update(delta_time)`: Update object state

#### `Unit(position, unit_type, faction)`
Represents a game unit with AI.

**Attributes:**
- `health`: Current health
- `max_health`: Maximum health
- `speed`: Movement speed
- `target`: Current target
- `waypoints`: List of waypoints

**Methods:**
- `move_to(target)`: Set movement target
- `attack(target)`: Attack another unit

#### `Building(position, building_type, size)`
Represents a static building.

#### `World()`
Manages all game objects and spatial queries.

**Methods:**
- `add_object(obj)`: Add object to world
- `remove_object(obj)`: Remove object from world
- `get_units_in_radius(pos, radius, faction?)`: Find units in radius
- `find_nearest_unit(pos, faction?, max_dist?)`: Find nearest unit
- `update(delta_time)`: Update all objects

#### `GameManager()`
Main game controller.

**Methods:**
- `initialize_game()`: Set up initial game state
- `update_game(delta_time)`: Update game logic
- `get_game_state()`: Get current game state

## Troubleshooting

### Common Issues

#### "Import not supported"
**Problem:** Using unsupported Python imports
**Solution:** Stick to supported libraries (math, random) or implement functionality directly

#### "Variable not resolved"
**Problem:** Variable scoping issues
**Solution:** Ensure variables are defined before use, avoid complex closures

#### "SQFVM test failed"
**Problem:** Generated SQF has syntax errors
**Solution:** Check Python code for unsupported constructs, simplify complex expressions

#### "Performance issues"
**Problem:** Slow transpilation or large output
**Solution:** Break large files into smaller modules, avoid excessive string operations

### Debug Mode

Enable verbose output for debugging:
```bash
parma compile my_file.py --verbose
```

### Manual SQF Inspection

Check generated SQF directly:
```bash
parma compile input.py
cat input.sqf  # Inspect generated code
```

## Advanced Usage

### Custom Transpiler Extensions

Extend Parma by adding custom AST visitors:

```python
import ast
from parma.transpiler import SQFTranspiler

class CustomTranspiler(SQFTranspiler):
    def visit_CustomNode(self, node):
        # Custom transformation logic
        self.output.append("// Custom SQF code")
```

### Integration with Build Systems

Use Parma in automated build pipelines:

```python
# build.py
import subprocess
from pathlib import Path

def build_mission():
    mission_files = Path("src").glob("**/*.py")

    for py_file in mission_files:
        sqf_file = py_file.with_suffix('.sqf')
        result = subprocess.run([
            "parma", "compile", str(py_file),
            "-o", str(sqf_file), "--test"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Failed to compile {py_file}")
            print(result.stderr)
            return False

    return True
```

### Large Project Organization

Structure large projects:

```
my_arma_mod/
├── src/
│   ├── core/          # Core game systems
│   ├── entities/      # Units, buildings
│   ├── ai/           # AI behaviors
│   ├── world/        # World generation
│   └── ui/           # User interface
├── tests/            # Test files
├── missions/         # Generated SQF files
├── build.py          # Build script
└── pyproject.toml    # Project configuration
```

## Performance Considerations

### Transpilation Speed
- **Fast**: Basic operations, function calls
- **Medium**: Complex expressions, class hierarchies
- **Slow**: Large files with many imports

### SQF Execution Performance
- **Efficient**: Direct SQF equivalents (math operations)
- **Overhead**: Function call wrappers, complex expressions
- **Optimization**: Use SQF-native operations where possible

### Memory Usage
- **Low**: Transpiler itself uses minimal memory
- **Variable**: Generated SQF size depends on input complexity
- **Streaming**: Large files processed without loading entirely

## Future Extensions

### Planned Features
- **More Python libraries**: json, datetime, collections
- **Advanced OOP**: Multiple inheritance, metaclasses
- **Async support**: Coroutine-based mission scripts
- **Debug integration**: Source map generation
- **Plugin system**: Custom transpiler extensions

### Community Contributions
Parma welcomes contributions for:
- Additional library support
- Performance optimizations
- New game framework features
- Documentation improvements
- Test coverage expansion

## Conclusion

Parma provides a complete bridge between Python development and ArmA 3 modding. By understanding its architecture, supported features, and usage patterns, developers can create sophisticated missions and mods using modern Python programming techniques.

The combination of AST-based transpilation, comprehensive testing, and a rich game framework makes Parma a powerful tool for ArmA 3 content creation.