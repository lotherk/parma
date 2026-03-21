# Parma - ArmA 3 Integration Guide

This guide explains how to integrate Parma-generated SQF code and the ParmaExtension DLL into your ArmA 3 missions and addons.

## Method 1: Using Transpiled SQF Code

### 1. **Include OOP Macros**
All Parma-generated SQF files require the OOP macro library:

```sqf
// At the top of your mission's init.sqf or description.ext
#include "macros\oop.h"
```

### 2. **File Structure for Missions**
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

### 3. **Basic Mission Setup**
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

### 4. **Example: Using Parma-Generated Classes**
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

## Method 2: Using ParmaExtension DLL (Runtime Python)

### 1. **DLL Installation**
- Copy `ParmaExtension.dll` to your ArmA 3 server directory
- The DLL loads automatically when ArmA starts

### 2. **SQF Interface**
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

### 3. **Advanced Usage**
```sqf
// Load Python script at runtime
_pythonCode = preprocessFile "scripts\myPythonLogic.py";
_fullCommand = "EXEC " + _pythonCode;
_result = "ParmaExtension" callExtension _fullCommand;

// Use Python for complex calculations
_aiDecision = "ParmaExtension" callExtension "EVAL calculate_ai_decision(unit_pos, enemy_pos)";
```

## Method 3: Addon Integration

### 1. **Addon Structure**
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

### 2. **config.cpp**
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

### 3. **CBA Integration** (Recommended)
If using CBA (Community Base Addons):

```sqf
// In your XEH_postInit.sqf
#include "macros\oop.h"

// Parma classes are now available globally
[] call compile preprocessFileLineNumbers "MyAddon\scripts\parma_generated.sqf";
```

## Troubleshooting

### Common Issues:

**1. "Undefined variable" errors:**
- Ensure `#include "macros\oop.h"` is at the top of your files
- Check that the macros folder is in the correct location

**2. DLL not loading:**
- Verify `ParmaExtension.dll` is in the ArmA 3 root directory
- Check server logs for DLL loading errors
- Ensure proper file permissions

**3. Class not found:**
- Make sure CLASS definitions are executed before usage
- Check for syntax errors in generated SQF

**4. Python execution fails:**
- DLL requires Python installation on the server
- Check that Python libraries are accessible to the DLL

## Best Practices

### 1. **File Organization**
- Keep Parma-generated files separate from hand-written SQF
- Use consistent naming conventions
- Document which files are auto-generated

### 2. **Performance**
- Initialize classes once, reuse instances
- Use DLL for complex calculations, SQF for simple logic
- Profile and optimize Python code running in DLL

### 3. **Debugging**
- Use `diag_log` extensively in SQF
- Check ArmA server logs for DLL errors
- Test Python code separately before integration

### 4. **Version Control**
- Commit both source Python files and generated SQF
- Document generation process in README
- Tag releases with Parma version used

## Example Mission

See the `demo.py` and `demo.sqf` files in this repository for a complete working example of a loot population system.

## Support

For issues specific to Parma integration:
1. Check this documentation
2. Verify your ArmA 3 installation
3. Test with the provided demo files
4. Report issues with specific error messages