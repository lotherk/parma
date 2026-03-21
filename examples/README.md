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

1. **Examine the Python code** in each example to understand the mission logic
2. **Run the Python script** to see it work: `python3 examples/01_basic_mission.py`
3. **Transpile to SQF**: `parma compile examples/01_basic_mission.py`
4. **Integrate the generated SQF** into your ArmA mission using the OOP macros

## File Structure

Each example consists of:
- **Python source** (`.py`): The mission logic in Python
- **Generated SQF** (`.sqf`): The transpiled ArmA code (after running `parma compile`)

## Key Features Demonstrated

- **OOP Classes**: Full class/method transpilation with proper SQF syntax
- **Complex Data Structures**: Arrays, dictionaries, nested objects
- **Control Flow**: Loops, conditionals, state machines
- **ArmA Integration**: Real class names, proper SQF commands
- **Performance**: Optimized for ArmA's execution environment
- **Modularity**: Reusable components across different mission types

## Learning Path

Start with simpler examples (01-03) to understand basic concepts, then progress to more complex systems (07-10) for advanced mission development.

## Integration Notes

- All examples use the `loot_system` demo as a base for testing
- Generated SQF requires `#include "macros/oop.h"` at the top
- Examples are designed to work together for complex missions
- Real ArmA class names are used throughout for authenticity

## Contributing

Add your own examples following the naming convention (`NN_descriptive_name.py`) and include comprehensive comments explaining the mission mechanics.