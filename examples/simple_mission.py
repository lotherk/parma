#!/usr/bin/env python3
"""
Simple ArmA 3 Mission Example
Write Python, get working SQF!
"""

import random
import math

# Create some units and make them do things
def create_units():
    """Create units at random positions"""
    units = []

    for i in range(5):
        # Random position
        x = random.uniform(100, 900)
        y = random.uniform(100, 900)

        # Create unit (this becomes SQF createUnit)
        unit_name = f"unit_{i}"
        print(f"Created unit {unit_name} at ({x:.1f}, {y:.1f})")

        units.append({
            "name": unit_name,
            "position": [x, y, 0],
            "type": "B_soldier_F"
        })

    return units

def move_units_randomly(units):
    """Make units move to random positions"""
    for unit in units:
        # Calculate new position
        current_x, current_y = unit["position"][0], unit["position"][1]
        new_x = current_x + random.uniform(-50, 50)
        new_y = current_y + random.uniform(-50, 50)

        # Keep in bounds
        new_x = max(0, min(1000, new_x))
        new_y = max(0, min(1000, new_y))

        print(f"{unit['name']} moving from ({current_x:.1f}, {current_y:.1f}) to ({new_x:.1f}, {new_y:.1f})")

        # Update position
        unit["position"] = [new_x, new_y, 0]

def calculate_distances(units):
    """Calculate distances between units"""
    if len(units) < 2:
        return

    for i, unit1 in enumerate(units):
        for j, unit2 in enumerate(units):
            if i != j:
                dx = unit1["position"][0] - unit2["position"][0]
                dy = unit1["position"][1] - unit2["position"][1]
                distance = math.sqrt(dx*dx + dy*dy)

                if distance < 100:  # Close units
                    print(f"{unit1['name']} and {unit2['name']} are {distance:.1f} meters apart")

def mission_loop():
    """Main mission loop"""
    print("Starting ArmA 3 mission...")

    # Initialize
    units = create_units()
    print(f"Created {len(units)} units")

    # Simulate some game loops
    for loop in range(3):
        print(f"\n--- Game Loop {loop + 1} ---")
        move_units_randomly(units)
        calculate_distances(units)

    print("\nMission complete!")

if __name__ == "__main__":
    mission_loop()