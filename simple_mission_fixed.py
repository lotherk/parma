#!/usr/bin/env python3
"""
Fixed Simple ArmA 3 Mission Example
Cleaner Python that transpiles better to SQF
"""

import random
import math

def create_units():
    """Create units at random positions"""
    units = []

    for i in range(5):
        # Random position
        x = random.uniform(100, 900)
        y = random.uniform(100, 900)

        # Create unit info
        unit_name = "unit_" + str(i)
        print("Created unit " + unit_name + " at (" + str(int(x)) + ", " + str(int(y)) + ")")

        unit_info = {
            "name": unit_name,
            "position": [x, y, 0],
            "type": "B_soldier_F"
        }
        units.append(unit_info)

    return units

def move_units_randomly(units):
    """Make units move to random positions"""
    for unit in units:
        # Get current position
        current_x = unit["position"][0]
        current_y = unit["position"][1]

        # Calculate new position
        new_x = current_x + random.uniform(-50, 50)
        new_y = current_y + random.uniform(-50, 50)

        # Keep in bounds
        new_x = max(0, min(1000, new_x))
        new_y = max(0, min(1000, new_y))

        print(unit["name"] + " moving to (" + str(int(new_x)) + ", " + str(int(new_y)) + ")")

        # Update position
        unit["position"] = [new_x, new_y, 0]

def calculate_distances(units):
    """Calculate distances between close units"""
    for i in range(len(units)):
        for j in range(len(units)):
            if i != j:
                unit1 = units[i]
                unit2 = units[j]

                dx = unit1["position"][0] - unit2["position"][0]
                dy = unit1["position"][1] - unit2["position"][1]
                distance = math.sqrt(dx*dx + dy*dy)

                if distance < 100:  # Close units
                    print(unit1["name"] + " and " + unit2["name"] + " are " + str(int(distance)) + " meters apart")

def mission_loop():
    """Main mission loop"""
    print("Starting ArmA 3 mission...")

    # Initialize
    units = create_units()
    print("Created " + str(len(units)) + " units")

    # Simulate some game loops
    for loop in range(3):
        print("\n--- Game Loop " + str(loop + 1) + " ---")
        move_units_randomly(units)
        calculate_distances(units)

    print("\nMission complete!")

if __name__ == "__main__":
    mission_loop()