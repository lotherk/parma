#!/usr/bin/env python3
"""
Random Units Mission - Python version
Creates random units across the map for ArmA mission
"""

import random

class RandomUnitsMission:
    def __init__(self):
        self.unit_types = [
            "B_Soldier_F",      # BLUFOR Rifleman
            "O_Soldier_F",      # OPFOR Rifleman
            "I_Soldier_F",      # Independent Rifleman
            "B_Soldier_GL_F",   # BLUFOR Grenadier
            "O_Soldier_AR_F",   # OPFOR Autorifleman
            "I_Soldier_M_F"     # Independent Marksman
        ]
        self.created_units = []

    def get_random_position(self):
        """Get a random position on the map"""
        # Altis map bounds (approximate)
        x = random.uniform(0, 30720)  # Map width
        y = random.uniform(0, 30720)  # Map height
        return [x, y, 0]

    def create_random_unit(self, side="BLUFOR"):
        """Create a single random unit"""
        unit_type = random.choice(self.unit_types)
        position = self.get_random_position()

        # Create unit at position
        unit = {
            'type': unit_type,
            'position': position,
            'side': side
        }

        self.created_units.append(unit)
        return unit

    def create_multiple_units(self, count=10, side="BLUFOR"):
        """Create multiple random units"""
        units = []
        for i in range(count):
            unit = self.create_random_unit(side)
            units.append(unit)
        return units

    def get_all_positions(self):
        """Get positions of all created units"""
        positions = []
        for unit in self.created_units:
            positions.append(unit['position'])
        return positions

    def count_units(self):
        """Return total number of created units"""
        return len(self.created_units)

    def cleanup_units(self):
        """Clean up all created units"""
        self.created_units.clear()

# Mission execution
mission = RandomUnitsMission()

# Create 15 random BLUFOR units
blufor_units = mission.create_multiple_units(15, "BLUFOR")

# Create 10 random OPFOR units
opfor_units = mission.create_multiple_units(10, "OPFOR")

# Create 5 independent units
independent_units = mission.create_multiple_units(5, "INDEPENDENT")

# Display mission info
total_units = mission.count_units()
print(f"Created {total_units} units across the map")

# Get all unit positions for markers or other uses
all_positions = mission.get_all_positions()
print(f"Units deployed at {len(all_positions)} locations")