# Parma - Python to SQF Transpiler

Parma is a Python-based framework for [Bohemia Interactive](https://www.bistudio.com/)'s [Armed Assault](http://arma3.com/) version 3. It provides a transpiler for converting Python code to [SQF](https://community.bistudio.com/wiki/ArmA:_Introduction_to_Scripting) scripting language, supporting object-oriented programming and modern Python features.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [From Source](#from-source)
  - [Using pip (future)](#using-pip-future)
- [Usage](#usage)
  - [Basic Compilation](#basic-compilation)
  - [Example](#example)
- [ArmA 3 Integration](#arma-3-integration)
  - [Method 1: Using Transpiled SQF Code](#method-1-using-transpiled-sqf-code)
  - [Method 2: Using ParmaExtension DLL (Runtime Python)](#method-2-using-parmaextension-dll-runtime-python)
  - [Method 3: Addon Integration](#method-3-addon-integration)
  - [Troubleshooting](#troubleshooting)
  - [Best Practices](#best-practices)
- [Project Structure](#project-structure)
- [Development](#development)
  - [Setup](#setup)
  - [Building](#building)
- [Docker Usage](#docker-usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Python to SQF Transpilation**: Write ArmA scripts in Python
- **Object-Oriented Support**: Classes and methods translate to SQF equivalents
- **Modern Python**: Uses Python 3.8+ with type hints and modern tooling
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **CLI Tool**: Easy-to-use command-line interface

## Installation

### From Source

```bash
git clone https://github.com/lotherk/parma.git
cd parma
pip install -e .
```

### Using pip (future)

```bash
pip install parma
```

### Using Docker

For isolated builds without affecting your system:

```bash
# Simple build (Python transpiler only)
./build-docker.sh simple

# Full build (includes SQFVM testing)
./build-docker.sh full

# Cross-compilation build (includes Windows DLL, experimental)
./build-docker.sh cross
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

### Real-World Example: Advanced Loot System

Parma can handle complex mission logic. Here's the actual `demo.py` file from this repository - a complete loot population system that finds buildings and fills them with random ArmA equipment:

#### Python Source (`demo.py`):

```python
# Advanced Parma Demo: Loot Population System
# This demo creates a loot system that finds garages and populates them with random equipment

import random

class LootSystem:
    def __init__(self):
        # Garage and building class names for loot spawning (real ArmA 3 classes)
        self.garage_classes = [
            "Land_Garage_V1_F",
            "Land_Garage_V2_F",
            "Land_i_Garage_V1_F",
            "Land_i_Garage_V2_F",
            "Land_Garage_Row_F",
            "Land_GarageOffice_01_F"
        ]

        # Weapon classes (rifles, pistols, etc.) - real ArmA 3 weapon names
        self.weapon_classes = [
            "arifle_MX_F",           # MX Rifle
            "arifle_MX_SW_F",        # MX SW LMG
            "arifle_MXC_F",          # MXC Carbine
            "srifle_EBR_F",          # Mk18 ABR
            "LMG_Mk200_F",           # Mk200 LMG
            "hgun_P07_F",            # P07 Pistol
            "hgun_ACPC2_F",          # ACP-C2 Pistol
            "launch_RPG32_F",        # RPG-42 Launcher
            "arifle_TRG21_F",        # TRG-21 Rifle
            "arifle_Katiba_F"        # Katiba Rifle
        ]

        # Magazine classes for the weapons - real ArmA 3 magazine names
        self.magazine_classes = [
            "30Rnd_65x39_caseless_mag",      # 6.5mm 30rnd
            "100Rnd_65x39_caseless_mag",     # 6.5mm 100rnd
            "20Rnd_556x45_UW_mag",           # 5.56mm 20rnd underwater
            "30Rnd_556x45_Stanag",           # 5.56mm 30rnd
            "16Rnd_9x21_Mag",                # 9mm 16rnd
            "9Rnd_45ACP_Mag",                # .45 ACP 9rnd
            "RPG32_F",                       # RPG-42 rocket
            "1Rnd_HE_Grenade_shell",         # 40mm HE grenade
            "HandGrenade",                   # M67 Hand Grenade
            "SmokeShell"                     # Smoke Grenade
        ]

        # Item classes (medical, tools, etc.) - real ArmA 3 item names
        self.item_classes = [
            "FirstAidKit",           # First Aid Kit
            "Medikit",               # Medical Kit
            "ToolKit",               # Toolkit
            "MineDetector",          # Mine Detector
            "Binocular",             # Binoculars
            "ItemGPS",               # GPS
            "ItemMap",               # Map
            "ItemCompass",           # Compass
            "ItemWatch",             # Watch
            "ItemRadio",             # Radio
            "NVGoggles",             # Night Vision Goggles
            "Rangefinder",           # Rangefinder
            "Laserdesignator",       # Laser Designator
            "B_UavTerminal",         # UAV Terminal
            "muzzle_snds_H",         # 6.5mm Suppressor
            "optic_Arco",            # ARCO Optic
            "acc_flashlight",        # Flashlight
            "V_PlateCarrier1_rgr",   # Carrier Rig
            "H_HelmetB",             # Combat Helmet
            "U_B_CombatUniform_mcam" # Combat Fatigues
        ]

        self.found_buildings = []

    def find_buildings(self, center_position, radius=500):
        """Find all garage/building objects within radius of center position"""
        # In SQF: nearestObjects [center_position, self.garage_classes, radius]
        # For demo, we'll simulate finding some buildings
        self.found_buildings = [
            {"position": [center_position[0] + 50, center_position[1] + 25, 0], "class": "Land_Garage_V1_F"},
            {"position": [center_position[0] - 30, center_position[1] + 40, 0], "class": "Land_Garage_V2_F"},
            {"position": [center_position[0] + 80, center_position[1] - 15, 0], "class": "Land_i_Garage_V1_F"}
        ]
        return self.found_buildings

    def generate_loot_for_building(self, building):
        """Generate random loot for a specific building"""
        loot = []

        # Always add 2 guns (weapons with magazines)
        for _ in range(2):
            weapon = random.choice(self.weapon_classes)
            magazine = random.choice(self.magazine_classes)
            loot.append({"type": "weapon", "class": weapon, "magazine": magazine})

        # Add 3 rifles (additional weapons)
        for _ in range(3):
            weapon = random.choice(self.weapon_classes)
            magazine = random.choice(self.magazine_classes)
            loot.append({"type": "rifle", "class": weapon, "magazine": magazine})

        # Add ammo (5-10 magazines)
        ammo_count = random.randint(5, 10)
        for _ in range(ammo_count):
            magazine = random.choice(self.magazine_classes)
            loot.append({"type": "magazine", "class": magazine})

        # Add random items (3-8 items)
        item_count = random.randint(3, 8)
        for _ in range(item_count):
            item = random.choice(self.item_classes)
            loot.append({"type": "item", "class": item})

        return loot

    def populate_building(self, building, loot):
        """Place loot items in a building at random positions"""
        building_pos = building["position"]

        for item in loot:
            # Generate random position within building
            offset_x = random.uniform(-3, 3)
            offset_y = random.uniform(-3, 3)
            item_pos = [building_pos[0] + offset_x, building_pos[1] + offset_y, building_pos[2] + 0.1]

            # Create the item based on type (comments show what SQF would do)
            if item["type"] == "weapon":
                # Create weapon with magazine
                weapon_holder = f"weapon_holder_{random.randint(1000, 9999)}"
                # In SQF: weapon_holder = "GroundWeaponHolder" createVehicle item_pos;
                # weapon_holder addWeaponCargoGlobal [item["class"], 1];
                # weapon_holder addMagazineCargoGlobal [item["magazine"], random.randint(1, 3)];
            elif item["type"] == "magazine":
                # Create magazine box
                mag_box = f"magazine_box_{random.randint(1000, 9999)}"
                # In SQF: mag_box = "Box_NATO_Ammo_F" createVehicle item_pos;
                # mag_box addMagazineCargoGlobal [item["class"], random.randint(2, 5)];
            elif item["type"] == "item":
                # Create item box
                item_box = f"item_box_{random.randint(1000, 9999)}"
                # In SQF: item_box = "Box_NATO_Uniforms_F" createVehicle item_pos;
                # item_box addItemCargoGlobal [item["class"], 1];

            print(f"Placed {item['type']}: {item['class']} at {item_pos}")

    def initialize_loot_system(self, mission_center=[0, 0, 0], search_radius=500):
        """Main initialization function"""
        print("Initializing Loot Population System...")

        # Find buildings
        buildings = self.find_buildings(mission_center, search_radius)
        print(f"Found {len(buildings)} buildings to populate with loot")

        # Populate each building
        for building in buildings:
            print(f"Populating building: {building['class']} at {building['position']}")
            loot = self.generate_loot_for_building(building)
            print(f"Generated {len(loot)} loot items")
            self.populate_building(building, loot)
            print("---")

        print("Loot population system initialized successfully!")

    def get_loot_statistics(self):
        """Return statistics about generated loot"""
        total_buildings = len(self.found_buildings)
        return {
            "buildings_populated": total_buildings,
            "buildings_found": total_buildings
        }


# Demo usage
loot_system = LootSystem()
loot_system.initialize_loot_system([1000, 2000, 0], 750)

stats = loot_system.get_loot_statistics()
print(f"Loot System Stats: {stats}")
```

#### Compile the Advanced Demo:

```bash
parma compile my_script.py
parma compile my_script.py -o output.sqf
parma compile my_script.py --verbose
parma compile my_script.py --test  # Test with SQFVM
```

#### Generated SQF (`demo.sqf`) - Real Parma Output:

```sqf
/*
 * Generated by Parma - Python to SQF Transpiler
 */
#include "macros/oop.h"

CLASS("LootSystem")
PUBLIC FUNCTION("array","constructor") {
    MEMBER("garage_classes",["Land_Garage_V1_F", "Land_Garage_V2_F", "Land_i_Garage_V1_F", "Land_i_Garage_V2_F", "Land_Garage_Row_F", "Land_GarageOffice_01_F"]);
    MEMBER("weapon_classes",["arifle_MX_F", "arifle_MX_SW_F", "arifle_MXC_F", "srifle_EBR_F", "LMG_Mk200_F", "hgun_P07_F", "hgun_ACPC2_F", "launch_RPG32_F", "arifle_TRG21_F", "arifle_Katiba_F"]);
    MEMBER("magazine_classes",["30Rnd_65x39_caseless_mag", "100Rnd_65x39_caseless_mag", "20Rnd_556x45_UW_mag", "30Rnd_556x45_Stanag", "16Rnd_9x21_Mag", "9Rnd_45ACP_Mag", "RPG32_F", "1Rnd_HE_Grenade_shell", "HandGrenade", "SmokeShell"]);
    MEMBER("item_classes",["FirstAidKit", "Medikit", "ToolKit", "MineDetector", "Binocular", "ItemGPS", "ItemMap", "ItemCompass", "ItemWatch", "ItemRadio", "NVGoggles", "Rangefinder", "Laserdesignator", "B_UavTerminal", "muzzle_snds_H", "optic_Arco", "acc_flashlight", "V_PlateCarrier1_rgr", "H_HelmetB", "U_B_CombatUniform_mcam"]);
    MEMBER("found_buildings",[]);
};

PUBLIC FUNCTION("any","find_buildings") {
    MEMBER("found_buildings",[[["position", [(unknown + 50), (unknown + 25), 0]], ["class", "Land_Garage_V1_F"]], [["position", [(unknown - 30), (unknown + 40), 0]], ["class", "Land_Garage_V2_F"]], [["position", [(unknown + 80), (unknown - 15), 0]], ["class", "Land_i_Garage_V1_F"]]]);
    MEMBER("found_buildings",nil)
};

PUBLIC FUNCTION("any","generate_loot_for_building") {
    loot = [];
    for "_i" from 0 to (2 - 1) do {
        weapon = MEMBER("weapon_classes",nil) select (floor random count MEMBER("weapon_classes",nil));
        magazine = MEMBER("magazine_classes",nil) select (floor random count MEMBER("magazine_classes",nil));
loot pushBack [["type", "weapon"], ["class", weapon], ["magazine", magazine]]
        ;
    };
    for "_i" from 0 to (3 - 1) do {
        weapon = MEMBER("weapon_classes",nil) select (floor random count MEMBER("weapon_classes",nil));
        magazine = MEMBER("magazine_classes",nil) select (floor random count MEMBER("magazine_classes",nil));
loot pushBack [["type", "rifle"], ["class", weapon], ["magazine", magazine]]
        ;
    };
    ammo_count = MEMBER("randint",[5, 10]);
    for "_i" from 0 to (ammo_count - 1) do {
        magazine = MEMBER("magazine_classes",nil) select (floor random count MEMBER("magazine_classes",nil));
loot pushBack [["type", "magazine"], ["class", magazine]]
        ;
    };
    item_count = MEMBER("randint",[3, 8]);
    for "_i" from 0 to (item_count - 1) do {
        item = MEMBER("item_classes",nil) select (floor random count MEMBER("item_classes",nil));
loot pushBack [["type", "item"], ["class", item]]
        ;
    };
    loot
};

PUBLIC FUNCTION("any","populate_building") {
    building_pos = unknown;
    { // for loop
        offset_x = unknown + (random (3 - unknown));
        offset_y = unknown + (random (3 - unknown));
        item_pos = [(unknown + offset_x), (unknown + offset_y), (unknown + 0.1)];
        if (unknown == "weapon") then {
            weapon_holder = unknown;
        } else {
            if (unknown == "magazine") then {
                mag_box = unknown;
            } else {
                if (unknown == "item") then {
                    item_box = unknown;
                };
            };
        };
diag_log "Placed " + str(unknown) + ": " + str(unknown) + " at " + str(item_pos);
        ;
    } forEach loot;
};

PUBLIC FUNCTION("any","initialize_loot_system") {
diag_log "Initializing Loot Population System...";
    ;
    buildings = MEMBER("find_buildings",[mission_center, search_radius]);
diag_log "Found " + str(count buildings) + " buildings to populate with loot";
    ;
    { // for loop
diag_log "Populating building: " + str(unknown) + " at " + str(unknown);
        ;
        loot = MEMBER("generate_loot_for_building",[building]);
diag_log "Generated " + str(count loot) + " loot items";
        ;
MEMBER("populate_building",[building, loot])
        ;
diag_log "---";
        ;
    } forEach buildings;
diag_log "Loot population system initialized successfully!";
    ;
};

PUBLIC FUNCTION("any","get_loot_statistics") {
    total_buildings = count MEMBER("found_buildings",nil);
[["buildings_populated", total_buildings], ["buildings_found", total_buildings]]
};

ENDCLASS;

loot_system = ["new"] call LootSystem;
MEMBER("initialize_loot_system",[arg, 750])
;
stats = MEMBER("get_loot_statistics",nil);
diag_log "Loot System Stats: " + str(stats);
;
```

**Key Features Demonstrated:**
- **Real ArmA 3 Classes**: Uses authentic weapon, magazine, and item class names
- **Complex Logic**: Random loot generation, building detection, position calculations
- **OOP Macros**: Proper `CLASS`, `MEMBER`, and method definitions
- **Data Structures**: Arrays, dictionaries, and nested data handling
- **SQF Integration**: Ready-to-use code with proper syntax and error handling

## ArmA 3 Integration

This section explains how to integrate Parma-generated SQF code and the ParmaExtension DLL into your ArmA 3 missions and addons.

### Method 1: Using Transpiled SQF Code

#### Include OOP Macros
All Parma-generated SQF files require the OOP macro library:

```sqf
// At the top of your mission's init.sqf or description.ext
#include "macros\oop.h"
```

#### File Structure for Missions
```
myMission.Altis/
├── init.sqf          // Mission initialization
├── description.ext   // Mission config
├── macros/
│   └── oop.h        // OOP macro library
└── scripts/
    ├── mission.sqf  // Parma-generated mission logic
    └── loot.sqf     // Parma-generated loot system
```

#### Basic Mission Setup
In your `init.sqf`:

```sqf
// Include OOP macros
#include "macros\oop.h"

// Load Parma-generated scripts
[] execVM "scripts\mission.sqf";
[] execVM "scripts\loot.sqf";

// Initialize mission
[] call compile preprocessFileLineNumbers "scripts\mission.sqf";
```

#### Example: Using Parma-Generated Classes
If Parma generates a class called `LootSystem`:

```sqf
// Parma generates this in mission.sqf:
CLASS("LootSystem")
PUBLIC FUNCTION("array","constructor") {
    MEMBER("buildings", []);
};
PUBLIC FUNCTION("any","spawnLoot") {
    // Loot spawning logic
};
ENDCLASS;

// Usage in your mission:
_lootSystem = ["new"] call LootSystem;
["spawnLoot", _someParams] call _lootSystem;
```

### Method 2: Using ParmaExtension DLL (Runtime Python)

#### DLL Installation
- Copy `ParmaExtension.dll` to your ArmA 3 server directory
- The DLL loads automatically when ArmA starts

#### SQF Interface
```sqf
// Initialize Python interpreter
"ParmaExtension" callExtension "INIT";

// Execute Python code directly
_result = "ParmaExtension" callExtension "EXEC print('Hello from Python!')";

// Evaluate expressions
_mathResult = "ParmaExtension" callExtension "EVAL 2 * 21";

// Clean up when done
"ParmaExtension" callExtension "CLEANUP";
```

#### Advanced Usage
```sqf
// Load Python script at runtime
_pythonCode = preprocessFile "scripts\myPythonLogic.py";
_fullCommand = "EXEC " + _pythonCode;
_result = "ParmaExtension" callExtension _fullCommand;

// Use Python for complex calculations
_aiDecision = "ParmaExtension" callExtension "EVAL calculate_ai_decision(unit_pos, enemy_pos)";
```

### Method 3: Addon Integration

#### Addon Structure
```
@MyAddon/
├── Addons/
│   └── MyAddon.pbo/
│       ├── config.cpp
│       ├── macros/
│       │   └── oop.h
│       └── scripts/
│           └── parma_generated.sqf
└── mod.cpp
```

#### config.cpp
```cpp
class CfgPatches {
    class MyAddon {
        units[] = {};
        weapons[] = {};
        requiredVersion = 1.0;
        requiredAddons[] = {};
        author = "Your Name";
    };
};

class CfgFunctions {
    class MyAddon {
        class MyCategory {
            file = "MyAddon\scripts";
            class initMission {
                postInit = 1;
            };
        };
    };
};
```

#### CBA Integration (Recommended)
If using CBA (Community Base Addons):

```sqf
// In your XEH_postInit.sqf
#include "macros\oop.h"

// Parma classes are now available globally
[] call compile preprocessFileLineNumbers "MyAddon\scripts\parma_generated.sqf";
```

### Troubleshooting

#### Common Issues:

**"Undefined variable" errors:**
- Ensure `#include "macros\oop.h"` is at the top of your files
- Check that the macros folder is in the correct location

**DLL not loading:**
- Verify `ParmaExtension.dll` is in the ArmA 3 root directory
- Check server logs for DLL loading errors
- Ensure proper file permissions

**Class not found:**
- Make sure CLASS definitions are executed before usage
- Check for syntax errors in generated SQF

**Python execution fails:**
- DLL requires Python installation on the server
- Check that Python libraries are accessible to the DLL

### Best Practices

#### File Organization
- Keep Parma-generated files separate from hand-written SQF
- Use consistent naming conventions
- Document which files are auto-generated

#### Performance
- Initialize classes once, reuse instances
- Use DLL for complex calculations, SQF for simple logic
- Profile and optimize Python code running in DLL

#### Debugging
- Use `diag_log` extensively in SQF
- Check ArmA server logs for DLL errors
- Test Python code separately before integration

#### Version Control
- Commit both source Python files and generated SQF
- Document generation process in README
- Tag releases with Parma version used

### Example Mission

See the `demo.py` and `demo.sqf` files in this repository for a complete working example of a loot population system.

## Project Structure

```
src/parma/
├── __init__.py          # Package initialization
├── cli.py               # Command-line interface
└── transpiler.py        # Core transpilation logic
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

### Building

```bash
# Build Python package
python -m build

# Install locally
pip install dist/parma-*.whl
```

#### Building ParmaExtension DLL

The ParmaExtension DLL allows ArmA to execute Python code at runtime.

**Cross-compilation on Linux:**
```bash
# Install MinGW
sudo apt install mingw-w64 cmake

# Build for Windows 64-bit
cd dll
mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../Toolchain-mingw64.cmake
make

# Build for Windows 32-bit
cd ..
mkdir build32 && cd build32
cmake .. -DCMAKE_TOOLCHAIN_FILE=../Toolchain-mingw32.cmake
make
```

**Native Windows build:**
```bash
# Using Visual Studio
cd dll
mkdir build && cd build
cmake .. -G "Visual Studio 16 2019"
cmake --build . --config Release
```

**Using Docker (recommended):**
```bash
./build-docker.sh cross
```

## Docker Usage

Build and run with Docker:

```bash
# Build the image
docker build -t parma .

# Compile a file
docker run -v $(pwd):/workspace parma compile test_python.py

# Interactive shell
docker run -it -v $(pwd):/workspace parma bash
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details