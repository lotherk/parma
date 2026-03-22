# Parma Example Missions

This directory contains 10 complex example missions demonstrating various aspects of Parma's Python-to-SQF transpilation capabilities. Each example showcases different mission mechanics that can be transpiled to functional ArmA 3 SQF code.

## Examples Overview

### 01_basic_mission.py
**Basic Mission Framework** - Demonstrates fundamental mission structure with objectives, win conditions, and progress tracking.

### 02_ai_spawn_system.py
**AI Spawn System** - Shows dynamic AI unit spawning with different types, formations, and group management.

### 03_vehicle_management.py
**Vehicle Management** - Covers vehicle spawning, crew assignment, fuel/repair systems, and service stations.

### 04_dialogue_system.py
**Dialogue System** - Implements NPC conversations with branching dialogue trees and response handling.

### 05_weather_time_system.py
**Weather & Time Management** - Demonstrates dynamic weather changes, time progression, and environmental control.

### 06_multiplayer_coordination.py
**Multiplayer Coordination** - Shows player management, team formation, communication, and objective assignment.

### 07_event_triggers.py
**Event System & Triggers** - Implements event-driven programming with area triggers and conditional activations.

### 08_inventory_management.py
**Inventory & Item Management** - Covers item handling, weight/slot limits, and player-to-player transfers.

### 09_scoring_statistics.py
**Mission Scoring & Statistics** - Demonstrates scoring systems, performance tracking, and mission analytics.

### 10_state_machine_logic.py
**Advanced State Machines** - Shows complex mission flow control using state machines and conditional logic.

## How to Use

### Testing Examples

1. **Run Python examples** to see the logic in action:
   ```bash
   python3 examples/01_basic_mission.py
   ```

2. **Transpile to SQF** for ArmA integration:
   ```bash
   parma compile examples/01_basic_mission.py
   ```

3. **Validate SQF output** (optional):
   ```bash
   python3 ../sqf_validator.py examples/01_basic_mission.sqf
   ```

### Integrating into ArmA Missions

1. **Copy the generated SQF** to your mission directory
2. **Include OOP macros** at the top of your `init.sqf`:
   ```sqf
   #include "macros\oop.h"
   ```

3. **Load the mission classes**:
   ```sqf
   [] execVM "scripts\01_basic_mission.sqf";
   ```

4. **Use the classes** in your mission:
   ```sqf
   _mission = ["new"] call BasicMission;
   ["initialize_mission"] call _mission;
   ```

### Batch Operations

**Transpile all examples:**
```bash
for file in examples/*.py; do parma compile "$file"; done
```

**Run comprehensive validation:**
```bash
python3 examples/validate_examples.py
```

**Validate all SQF outputs:**
```bash
for file in examples/*.sqf; do python3 ../sqf_validator.py "$file"; done
```

## File Structure

Each example consists of:
- **Python source** (`.py`): The mission logic in Python with detailed comments
- **Generated SQF** (`.sqf`): The transpiled ArmA code using Parma's OOP macros
- **Validation status**: All examples use verified SQF commands from the official database

### Example Structure:
```
examples/
├── 01_basic_mission.py      # Python source with mission logic
├── 01_basic_mission.sqf     # Generated SQF using CLASS/MEMBER macros
├── 02_ai_spawn_system.py    # AI spawning and group management
├── 02_ai_spawn_system.sqf   # Transpiled with createUnit commands
└── ...
```

## Validation Status ✅

All examples have been comprehensively validated:

| Example | Python Execution | Transpilation | SQF Commands | Status |
|---------|------------------|---------------|--------------|---------|
| 01_basic_mission.py | ✅ Runs | ✅ Compiles | 12 commands | ✅ Valid |
| 02_ai_spawn_system.py | ✅ Runs | ✅ Compiles | 17 commands | ✅ Valid |
| 03_vehicle_management.py | ✅ Runs | ✅ Compiles | 20 commands | ✅ Valid |
| 04_dialogue_system.py | ✅ Runs | ✅ Compiles | 10 commands | ✅ Valid |
| 05_weather_time_system.py | ✅ Runs | ✅ Compiles | 13 commands | ✅ Valid |
| 06_multiplayer_coordination.py | ✅ Runs | ✅ Compiles | 13 commands | ✅ Valid |
| 07_event_triggers.py | ✅ Runs | ✅ Compiles | 14 commands | ✅ Valid |
| 08_inventory_management.py | ✅ Runs | ✅ Compiles | 9 commands | ✅ Valid |
| 09_scoring_statistics.py | ✅ Runs | ✅ Compiles | 16 commands | ✅ Valid |
| 10_state_machine_logic.py | ✅ Runs | ✅ Compiles | 10 commands | ✅ Valid |

**Summary**: 10/10 examples (100% success rate)
- 🐍 **Python execution**: 10/10 working
- 🔄 **Transpilation**: 10/10 successful
- 🎯 **SQF validation**: 10/10 valid commands detected

## Key Features Demonstrated

- **OOP Classes**: Full class/method transpilation with proper SQF syntax using ArmA OOP macros
- **Complex Data Structures**: Arrays, dictionaries, nested objects (converted to SQF arrays)
- **Control Flow**: Loops (`forEach`), conditionals (`if-then`), state machines
- **ArmA Integration**: Real class names from SQF command database, proper command usage
- **Performance**: Optimized for ArmA's execution environment with efficient SQF patterns
- **Modularity**: Reusable components across different mission types
- **Validation**: All generated SQF uses verified commands from the official database

## Learning Path

Start with simpler examples (01-03) to understand basic concepts, then progress to more complex systems (07-10) for advanced mission development.

### Beginner Level (01-03):
- **01**: Basic class structure, arrays, loops
- **02**: AI spawning, group management, formations
- **03**: Vehicle systems, fuel/repair mechanics

### Intermediate Level (04-06):
- **04**: Dialogue trees, NPC interactions
- **05**: Environmental control, time management
- **06**: Multiplayer coordination, team systems

### Advanced Level (07-10):
- **07**: Event-driven programming, triggers
- **08**: Inventory systems, resource management
- **09**: Scoring systems, statistics tracking
- **10**: State machines, complex mission flow

## Integration Notes

- **OOP Macros Required**: All generated SQF requires `#include "macros/oop.h"` at the top
- **Command Validation**: Generated code uses verified SQF commands from the official database
- **ArmA Compatibility**: Real class names and proper SQF syntax throughout
- **Performance Optimized**: Efficient SQF patterns for ArmA's execution environment
- **Modular Design**: Examples can be combined for complex missions

## Contributing

Add your own examples following the naming convention (`NN_descriptive_name.py`) and include comprehensive comments explaining the mission mechanics.