"""Game Development Utilities for Parma - Open World Game Framework."""

import random
import math
from typing import List, Dict, Any, Tuple, Optional

# Game Constants
WORLD_SIZE = 10000
GRID_SIZE = 100
MAX_UNITS = 500
RESPAWN_TIME = 30

class Vector3:
    """3D Vector for positions and directions."""
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance(self, other: 'Vector3') -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def normalize(self) -> 'Vector3':
        length = self.distance(Vector3(0, 0, 0))
        if length > 0:
            return Vector3(self.x/length, self.y/length, self.z/length)
        return Vector3(0, 0, 0)

class GameObject:
    """Base class for all game objects."""
    def __init__(self, position: Vector3, object_type: str = "default"):
        self.position = position
        self.object_type = object_type
        self.id = id(self)  # Unique ID
        self.active = True

    def update(self, delta_time: float):
        """Update object state. Override in subclasses."""
        pass

    def destroy(self):
        """Mark object for destruction."""
        self.active = False

class Unit(GameObject):
    """Game unit with AI and behavior."""
    def __init__(self, position: Vector3, unit_type: str, faction: str = "neutral"):
        super().__init__(position, "unit")
        self.unit_type = unit_type
        self.faction = faction
        self.health = 100
        self.max_health = 100
        self.speed = 5.0
        self.target = None
        self.waypoints: List[Vector3] = []

    def move_to(self, target: Vector3):
        """Set movement target."""
        self.target = target

    def attack(self, target: 'Unit'):
        """Attack another unit."""
        if target.faction != self.faction:
            self.target = target

    def update(self, delta_time: float):
        """Update unit AI and movement."""
        if self.target:
            direction = (self.target.position - self.position).normalize()
            distance = self.position.distance(self.target.position)

            if distance > 1.0:
                # Move towards target
                self.position.x += direction.x * self.speed * delta_time
                self.position.y += direction.y * self.speed * delta_time
                self.position.z += direction.z * self.speed * delta_time
            else:
                # Reached target
                self.target = None

        # Update waypoints if following a path
        if self.waypoints and not self.target:
            next_waypoint = self.waypoints[0]
            self.move_to(next_waypoint)
            if self.position.distance(next_waypoint) < 1.0:
                self.waypoints.pop(0)

class Building(GameObject):
    """Static building or structure."""
    def __init__(self, position: Vector3, building_type: str, size: Vector3):
        super().__init__(position, "building")
        self.building_type = building_type
        self.size = size
        self.occupants: List[Unit] = []

class World:
    """Game world manager."""
    def __init__(self):
        self.objects: List[GameObject] = []
        self.units: List[Unit] = []
        self.buildings: List[Building] = []
        self.time = 0.0
        self.weather = "clear"

    def add_object(self, obj: GameObject):
        """Add object to world."""
        self.objects.append(obj)
        if isinstance(obj, Unit):
            self.units.append(obj)
        elif isinstance(obj, Building):
            self.buildings.append(obj)

    def remove_object(self, obj: GameObject):
        """Remove object from world."""
        if obj in self.objects:
            self.objects.remove(obj)
        if isinstance(obj, Unit) and obj in self.units:
            self.units.remove(obj)
        elif isinstance(obj, Building) and obj in self.buildings:
            self.buildings.remove(obj)

    def update(self, delta_time: float):
        """Update all objects in world."""
        self.time += delta_time

        # Update all objects
        for obj in self.objects[:]:  # Copy list to avoid modification during iteration
            if obj.active:
                obj.update(delta_time)
            else:
                self.remove_object(obj)

    def find_nearest_unit(self, position: Vector3, faction: Optional[str] = None, max_distance: float = 1000.0) -> Optional[Unit]:
        """Find nearest unit to position."""
        nearest = None
        min_distance = max_distance

        for unit in self.units:
            if faction and unit.faction != faction:
                continue
            distance = position.distance(unit.position)
            if distance < min_distance:
                min_distance = distance
                nearest = unit

        return nearest

    def get_units_in_radius(self, position: Vector3, radius: float, faction: Optional[str] = None) -> List[Unit]:
        """Get all units within radius of position."""
        units_in_range = []
        for unit in self.units:
            if faction and unit.faction != faction:
                continue
            if position.distance(unit.position) <= radius:
                units_in_range.append(unit)
        return units_in_range

    def get_units_in_radius_by_factions(self, position: Vector3, radius: float, factions: List[str]) -> List[Unit]:
        """Get all units within radius of position that match any of the given factions."""
        units_in_range = []
        for unit in self.units:
            if unit.faction not in factions:
                continue
            if position.distance(unit.position) <= radius:
                units_in_range.append(unit)
        return units_in_range

class GameManager:
    """Main game manager."""
    def __init__(self):
        self.world = World()
        self.player = None
        self.game_running = True
        self.score = 0

    def initialize_game(self):
        """Set up initial game state."""
        # Create player
        self.player = Unit(Vector3(5000, 5000, 0), "B_soldier_F", "player")

        # Create some enemy units
        for i in range(10):
            enemy_pos = Vector3(
                random.uniform(0, WORLD_SIZE),
                random.uniform(0, WORLD_SIZE),
                0
            )
            enemy = Unit(enemy_pos, "O_soldier_F", "enemy")
            self.world.add_object(enemy)

        # Create some buildings
        for i in range(5):
            building_pos = Vector3(
                random.uniform(0, WORLD_SIZE),
                random.uniform(0, WORLD_SIZE),
                0
            )
            building = Building(building_pos, "Land_House_Small_01_F", Vector3(10, 10, 5))
            self.world.add_object(building)

        self.world.add_object(self.player)

    def update_game(self, delta_time: float):
        """Main game update loop."""
        self.world.update(delta_time)

        # Simple AI: enemies attack player if close
        if self.player:
            for unit in self.world.units:
                if unit.faction == "enemy" and unit.target is None:
                    distance_to_player = unit.position.distance(self.player.position)
                    if distance_to_player < 500:
                        unit.attack(self.player)
                    else:
                        # Patrol randomly
                        if random.random() < 0.01:  # 1% chance per frame
                            patrol_target = Vector3(
                                unit.position.x + random.uniform(-200, 200),
                                unit.position.y + random.uniform(-200, 200),
                                unit.position.z
                            )
                            unit.move_to(patrol_target)

    def spawn_enemy_reinforcements(self):
        """Spawn enemy reinforcements."""
        spawn_pos = Vector3(
            random.uniform(0, WORLD_SIZE),
            random.uniform(0, WORLD_SIZE),
            0
        )
        enemy = Unit(spawn_pos, "O_soldier_F", "enemy")
        self.world.add_object(enemy)

    def check_win_condition(self) -> bool:
        """Check if player has won."""
        enemy_count = len([u for u in self.world.units if u.faction == "enemy"])
        return enemy_count == 0

# Global game instance
game = GameManager()

def start_game():
    """Initialize and start the game."""
    print("Initializing open world game...")
    game.initialize_game()
    print(f"Game started! Player at {game.player.position.x}, {game.player.position.y}")
    print(f"Created {len(game.world.units)} units and {len(game.world.buildings)} buildings")

def update_game_loop(delta_time: float = 0.016):  # ~60 FPS
    """Update game state."""
    game.update_game(delta_time)

    # Periodic enemy spawns
    if random.random() < 0.001:  # Very rare chance
        game.spawn_enemy_reinforcements()

    # Check win condition
    if game.check_win_condition():
        print("Congratulations! You won the game!")
        game.game_running = False

def get_game_state() -> Dict[str, Any]:
    """Get current game state for debugging/UI."""
    return {
        "time": game.world.time,
        "player_health": game.player.health if game.player else 0,
        "unit_count": len(game.world.units),
        "building_count": len(game.world.buildings),
        "score": game.score,
        "weather": game.world.weather
    }

# Initialize when module loads
if __name__ == "__main__":
    start_game()