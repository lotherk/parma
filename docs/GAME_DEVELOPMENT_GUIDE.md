# Parma Game Development Guide

## Overview

Parma enables you to write **open world games** for ArmA 3 entirely in Python. Forget about SQF syntax - write clean, modern Python code and let Parma handle the transpilation.

## Quick Start

```python
# game.py
import math
import random
from game_framework import Vector3, Unit, World, GameManager

# Create your game
game = GameManager()
world = game.world

# Add a player
player = Unit(Vector3(5000, 5000, 0), "B_soldier_F", "player")
world.add_object(player)

# Add enemies
for i in range(10):
    enemy = Unit(Vector3(random.uniform(0, 10000), random.uniform(0, 10000), 0),
                "O_soldier_F", "enemy")
    world.add_object(enemy)

# Game loop
def update():
    # AI logic here
    for unit in world.units:
        if unit.faction == "enemy":
            # Find nearby players
            nearby = world.get_units_in_radius(unit.position, 500, "player")
            if nearby:
                unit.attack(nearby[0])

# Transpile to SQF
# Run: parma compile game.py
```

## Supported Python Features

### Math Functions
```python
import math

# All of these work
angle_rad = math.atan2(dy, dx)
distance = math.sqrt(dx**2 + dy**2)
normalized = math.sin(angle) * speed
floored = math.floor(position)
```

### Random Functions
```python
import random

# Generate random values
chance = random.random()  # 0.0 to 1.0
damage = random.uniform(10, 50)  # Range
direction = random.choice(["north", "south", "east", "west"])
roll = random.randint(1, 20)  # Integer range
```

### Control Flow
```python
# All Python control structures work
if health < 20:
    retreat()
elif ammo > 0:
    attack()
else:
    reload()

for unit in units:
    unit.update()

while game_running:
    update_game()
```

### Data Structures
```python
# Lists and dictionaries
inventory = ["rifle", "pistol", "medkit"]
stats = {"health": 100, "ammo": 30, "score": 0}

# List comprehensions
alive_units = [u for u in units if u.health > 0]
enemy_positions = [u.position for u in units if u.faction == "enemy"]
```

### Classes and Objects
```python
class CustomUnit(Unit):
    def __init__(self, position):
        super().__init__(position, "B_soldier_F", "player")
        self.special_ability = True

    def update(self, delta_time):
        super().update(delta_time)
        if self.special_ability:
            self.do_special_thing()
```

## Game Framework

### Vector3
```python
from game_framework import Vector3

pos = Vector3(100, 200, 50)
target = Vector3(150, 250, 50)

# Math operations
direction = target - pos
distance = pos.distance(target)
normalized = direction.normalize()
new_pos = pos + direction
```

### Units
```python
unit = Unit(position, "B_soldier_F", "military")

# Movement
unit.move_to(target_position)
unit.speed = 8.0  # Units per second

# Combat
unit.attack(enemy_unit)

# Waypoints
unit.waypoints = [point1, point2, point3]
```

### Buildings
```python
building = Building(position, "Land_House_Small_01_F", Vector3(10, 10, 5))
world.add_object(building)
```

### World Management
```python
world = World()

# Add objects
world.add_object(unit)
world.add_object(building)

# Query objects
nearby_units = world.get_units_in_radius(position, 500)
nearest_enemy = world.find_nearest_unit(position, "enemy")
```

### Game Loop
```python
game = GameManager()
game.initialize_game()

while game.game_running:
    game.update_game(0.016)  # 60 FPS

    # Your custom logic
    update_ai()
    check_win_conditions()
```

## Advanced Features

### AI Systems
```python
def ai_system():
    for unit in world.units:
        if unit.faction == "enemy":
            # Patrol behavior
            if not unit.target:
                patrol_point = Vector3(
                    unit.position.x + random.uniform(-200, 200),
                    unit.position.y + random.uniform(-200, 200),
                    0
                )
                unit.move_to(patrol_point)

            # Combat behavior
            nearby_players = world.get_units_in_radius(unit.position, 300, "player")
            if nearby_players:
                unit.attack(nearby_players[0])
```

### Quest System
```python
class Quest:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.completed = False
        self.objectives = []

    def check_completion(self):
        return all(obj.completed for obj in self.objectives)

# Usage
kill_quest = Quest("Eliminate Enemies", "Kill 10 enemy soldiers")
# Add objectives...
```

### Weather System
```python
def update_weather():
    if random.random() < 0.001:  # Rare weather change
        weathers = ["clear", "cloudy", "rain", "storm"]
        world.weather = random.choice(weathers)
```

## Performance Tips

### Efficient Queries
```python
# Good: Use faction filtering
enemies = world.get_units_in_radius(pos, 500, "enemy")

# Bad: Filter manually
all_nearby = world.get_units_in_radius(pos, 500)
enemies = [u for u in all_nearby if u.faction == "enemy"]
```

### Object Pooling
```python
# Reuse objects instead of creating/destroying
inactive_units = [u for u in units if not u.active]

if inactive_units:
    unit = inactive_units[0]
    unit.active = True
    unit.position = spawn_point
```

### Update Frequency
```python
frame_count = 0

def update():
    global frame_count
    frame_count += 1

    # Expensive operations every 10 frames
    if frame_count % 10 == 0:
        update_ai()

    # Very expensive operations every 100 frames
    if frame_count % 100 == 0:
        update_quests()
```

## Deployment

### Transpilation
```bash
# Compile your game
parma compile my_game.py

# Compile and test with SQFVM
parma compile my_game.py --test

# The result is my_game.sqf - ready for ArmA!
```

### SQFVM Testing
Parma can automatically test your generated SQF code using SQFVM (SQF Virtual Machine):

```bash
# Test during compilation
parma compile my_game.py --test

# Build with SQFVM testing support
./build-docker.sh full

# Use in Docker
docker run -it --rm parma-full parma compile my_game.py --test
```

SQFVM validation ensures your generated SQF code is syntactically correct and executable.

### ArmA Integration
1. Copy the generated `.sqf` files to your mission folder
2. Call the functions from your mission's `init.sqf`:
   ```sqf
   // init.sqf
   call compile preprocessFile "my_game.sqf";

   // Start your game
   [] call main_game_loop;
   ```

### Using the DLL (Advanced)
For runtime Python execution in ArmA:
```sqf
// Load the Parma extension
"ParmaExtension" callExtension "load";

// Execute Python code
_result = "ParmaExtension" callExtension "exec:print('Hello from Python!')";
```

## Best Practices

### Code Organization
```
my_game/
├── core/           # Core game systems
├── entities/       # Units, buildings, etc.
├── ai/            # AI behaviors
├── quests/        # Quest system
├── ui/            # User interface
└── main.py        # Entry point
```

### Error Handling
```python
try:
    dangerous_operation()
except Exception as e:
    # Log error in SQF
    diag_log(f"Error: {e}")
    # Continue game
    pass
```

### Memory Management
```python
# Clean up inactive objects
world.objects = [obj for obj in world.objects if obj.active]

# Limit object counts
if len(world.units) > MAX_UNITS:
    # Remove oldest inactive units
    pass
```

## Examples

Check the `examples/` directory for complete game examples:
- Basic mission setup
- AI combat systems
- City generation
- Weather simulation
- Resource management

## Troubleshooting

### Common Issues

**"Function not found" errors:**
- Make sure all imports are at the top
- Check that function names match SQF conventions

**Performance issues:**
- Reduce object counts
- Use efficient queries
- Limit update frequencies

**Transpilation errors:**
- Use only supported Python features
- Check the generated SQF for syntax errors

## Get Started!

1. **Write your game in Python** - Use all the features above
2. **Test locally** - Run `python my_game.py` to verify logic
3. **Transpile** - Run `parma compile my_game.py`
4. **Deploy to ArmA** - Copy `.sqf` files to your mission
5. **Play!** - Enjoy your Python-powered ArmA game

**Happy game development with Parma! 🎮**