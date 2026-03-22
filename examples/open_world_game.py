#!/usr/bin/env python3
"""
Open World Game Example for Parma
This demonstrates a complete game written in Python that transpiles to SQF.
"""

import math
import random
from typing import List, Dict, Any, Tuple

# Import our game framework
from game_framework import Vector3, Unit, Building, World, GameManager, start_game, update_game_loop, get_game_state, game

def create_city(world: World, center: Vector3, radius: float = 500.0):
    """Create a small city with buildings and civilians."""
    print(f"Creating city at {center.x}, {center.y} with radius {radius}")

    # Create buildings in a grid pattern
    building_types = [
        "Land_House_Small_01_F",
        "Land_House_Small_02_F",
        "Land_House_Big_01_F",
        "Land_Office_01_F",
        "Land_Shop_01_F"
    ]

    grid_size = int(radius / 50)
    for x in range(-grid_size, grid_size + 1):
        for y in range(-grid_size, grid_size + 1):
            if random.random() < 0.3:  # 30% chance of building
                building_x = center.x + x * 60 + random.uniform(-10, 10)
                building_y = center.y + y * 60 + random.uniform(-10, 10)

                building_type = random.choice(building_types)
                building = Building(
                    Vector3(building_x, building_y, 0),
                    building_type,
                    Vector3(10, 10, 8)
                )
                world.add_object(building)

    # Create some civilians
    for i in range(20):
        civilian_pos = Vector3(
            center.x + random.uniform(-radius, radius),
            center.y + random.uniform(-radius, radius),
            0
        )
        civilian = Unit(civilian_pos, "C_man_1", "civilian")
        civilian.speed = 2.0  # Civilians walk slower
        world.add_object(civilian)

def setup_military_patrols(world: World):
    """Set up military patrol routes."""
    patrol_points = [
        Vector3(2000, 2000, 0),
        Vector3(8000, 2000, 0),
        Vector3(8000, 8000, 0),
        Vector3(2000, 8000, 0)
    ]

    for i in range(8):
        # Create patrol unit
        start_point = random.choice(patrol_points)
        soldier = Unit(start_point, "B_soldier_F", "military")
        soldier.speed = 4.0

        # Create patrol route
        route = patrol_points[:]  # Copy the list
        random.shuffle(route)
        soldier.waypoints = route

        world.add_object(soldier)

def setup_ambient_events(world: World):
    """Set up ambient world events like wildlife, vehicles, etc."""
    # Add some wildlife
    for i in range(15):
        animal_pos = Vector3(
            random.uniform(0, 10000),
            random.uniform(0, 10000),
            0
        )
        if random.random() < 0.7:
            animal = Unit(animal_pos, "Sheep_random_F", "wildlife")
        else:
            animal = Unit(animal_pos, "Hen_random_F", "wildlife")
        animal.speed = 1.0
        world.add_object(animal)

    # Add some parked vehicles
    vehicle_types = ["C_Offroad_01_F", "C_Hatchback_01_F", "C_SUV_01_F"]
    for i in range(10):
        vehicle_pos = Vector3(
            random.uniform(0, 10000),
            random.uniform(0, 10000),
            0
        )
        # For now, represent vehicles as special units
        vehicle = Unit(vehicle_pos, random.choice(vehicle_types), "vehicle")
        vehicle.speed = 0  # Stationary
        world.add_object(vehicle)

def ai_system_update(world: World):
    """Advanced AI system for all units."""
    for unit in world.units:
        if unit.faction == "civilian":
            # Civilian AI - wander around aimlessly
            if random.random() < 0.005:  # Very occasional direction change
                wander_target = Vector3(
                    unit.position.x + random.uniform(-100, 100),
                    unit.position.y + random.uniform(-100, 100),
                    unit.position.z
                )
                # Keep within world bounds
                wander_target.x = max(0, min(10000, wander_target.x))
                wander_target.y = max(0, min(10000, wander_target.y))
                unit.move_to(wander_target)

        elif unit.faction == "military":
            # Military AI - patrol and respond to threats
            nearby_enemies = world.get_units_in_radius(unit.position, 300, "enemy")
            if nearby_enemies:
                # Engage nearest enemy
                nearest_enemy = min(nearby_enemies,
                                  key=lambda e: unit.position.distance(e.position))
                unit.attack(nearest_enemy)
            # Patrol logic is handled by waypoints in the Unit class

        elif unit.faction == "enemy":
            # Enemy AI - hunt players and civilians
            nearby_targets = world.get_units_in_radius_by_factions(unit.position, 400,
                                                                 ["player", "civilian", "military"])
            if nearby_targets:
                target = random.choice(nearby_targets)
                if target:
                    unit.attack(target)

def weather_system(world: World):
    """Dynamic weather system."""
    # Simple weather changes
    if random.random() < 0.001:  # Very rare weather change
        weathers = ["clear", "cloudy", "rain", "storm"]
        new_weather = random.choice(weathers)
        world.weather = new_weather
        print(f"Weather changed to: {new_weather}")

def resource_management():
    """Manage game resources and economy."""
    # This would handle resource gathering, trading, etc.
    # For now, just a placeholder
    pass

def quest_system():
    """Handle quests and missions."""
    # This would manage quest states, objectives, rewards
    # For now, just a placeholder
    pass

def save_game_state(filename: str = "savegame.json"):
    """Save current game state."""
    # In a real implementation, this would serialize the game state
    print(f"Saving game to {filename}")
    # Note: JSON support would need to be implemented in the transpiler

def load_game_state(filename: str = "savegame.json"):
    """Load game state from file."""
    print(f"Loading game from {filename}")
    # Note: JSON support would need to be implemented in the transpiler

# Main game loop
def main_game_loop():
    """Main game update loop."""
    start_game()

    # Set up the world
    world = game.world

    # Create cities
    create_city(world, Vector3(2500, 2500, 0), 400)
    create_city(world, Vector3(7500, 7500, 0), 300)
    create_city(world, Vector3(2500, 7500, 0), 350)
    create_city(world, Vector3(7500, 2500, 0), 250)

    # Set up military
    setup_military_patrols(world)

    # Set up ambient world
    setup_ambient_events(world)

    print(f"World setup complete! {len(world.units)} units, {len(world.buildings)} buildings")

    # Main game loop
    frame_count = 0
    while game.game_running and frame_count < 1000:  # Limit for demo
        update_game_loop(0.1)  # 10 FPS for demo

        # Update AI every few frames
        if frame_count % 10 == 0:
            ai_system_update(world)

        # Update weather occasionally
        if frame_count % 100 == 0:
            weather_system(world)

        # Periodic resource updates
        if frame_count % 50 == 0:
            resource_management()

        # Quest updates
        if frame_count % 200 == 0:
            quest_system()

        frame_count += 1

        # Print status occasionally
        if frame_count % 100 == 0:
            state = get_game_state()
            print(f"Frame {frame_count}: {state['unit_count']} units, weather: {state['weather']}")

    print("Game loop ended")
    final_state = get_game_state()
    print(f"Final state: {final_state}")

if __name__ == "__main__":
    try:
        main_game_loop()
    except Exception as e:
        print(f"Game crashed with error: {e}")
        # In a real game, we'd save crash logs here