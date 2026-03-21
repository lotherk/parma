# Example 2: AI Spawn System
# Demonstrates dynamic AI spawning with different unit types and behaviors

import random

class AISpawnSystem:
    def __init__(self):
        self.spawned_units = []
        self.unit_types = {
            "rifleman": ["B_Soldier_F", "O_Soldier_F", "I_Soldier_F"],
            "sniper": ["B_Sniper_F", "O_Sniper_F", "I_Sniper_F"],
            "mg": ["B_Soldier_AR_F", "O_Soldier_AR_F", "I_Soldier_AR_F"],
            "medic": ["B_Medic_F", "O_Medic_F", "I_Medic_F"]
        }
        self.groups = []

    def spawn_unit(self, position, side="EAST", unit_type="rifleman", skill=0.5):
        """Spawn a single AI unit"""
        if unit_type not in self.unit_types:
            unit_type = "rifleman"

        class_name = random.choice(self.unit_types[unit_type])

        unit = {
            "id": f"unit_{len(self.spawned_units)}",
            "class": class_name,
            "position": position,
            "side": side,
            "skill": skill,
            "group": None,
            "alive": True
        }

        self.spawned_units.append(unit)
        return unit

    def spawn_group(self, leader_position, size=4, formation="WEDGE", side="EAST"):
        """Spawn a group of AI units"""
        group_id = f"group_{len(self.groups)}"
        group = {
            "id": group_id,
            "units": [],
            "formation": formation,
            "side": side,
            "leader": None
        }

        # Spawn leader
        leader = self.spawn_unit(leader_position, side, "rifleman", 0.7)
        leader["group"] = group_id
        leader["is_leader"] = True
        group["leader"] = leader["id"]
        group["units"].append(leader)

        # Spawn additional units in formation
        for i in range(size - 1):
            # Position units around leader based on formation
            offset = self._calculate_formation_offset(i, formation)
            unit_pos = [
                leader_position[0] + offset[0],
                leader_position[1] + offset[1],
                leader_position[2]
            ]

            unit = self.spawn_unit(unit_pos, side, "rifleman", 0.5)
            unit["group"] = group_id
            group["units"].append(unit)

        self.groups.append(group)
        return group

    def _calculate_formation_offset(self, index, formation):
        """Calculate position offset for unit in formation"""
        offsets = {
            "WEDGE": [(0, -5), (-4, -8), (4, -8), (0, -11)],
            "LINE": [(-3*index, -5), (-3*index, -5), (-3*index, -5), (-3*index, -5)],
            "COLUMN": [(0, -3*index), (0, -3*index), (0, -3*index), (0, -3*index)]
        }

        if formation in offsets and index < len(offsets[formation]):
            return offsets[formation][index]
        return (random.uniform(-2, 2), random.uniform(-2, 2))

    def move_group(self, group_id, destination, speed="NORMAL"):
        """Move a group to a destination"""
        for group in self.groups:
            if group["id"] == group_id:
                for unit in group["units"]:
                    if unit["alive"]:
                        # In SQF: unit doMove destination
                        unit["destination"] = destination
                        unit["speed"] = speed
                break

    def set_group_behavior(self, group_id, behavior="AWARE", combat_mode="RED"):
        """Set AI behavior for a group"""
        behaviors = ["CARELESS", "SAFE", "AWARE", "COMBAT"]
        combat_modes = ["BLUE", "GREEN", "WHITE", "YELLOW", "RED"]

        if behavior not in behaviors:
            behavior = "AWARE"
        if combat_mode not in combat_modes:
            combat_mode = "RED"

        for group in self.groups:
            if group["id"] == group_id:
                group["behavior"] = behavior
                group["combat_mode"] = combat_mode
                for unit in group["units"]:
                    unit["behavior"] = behavior
                    unit["combat_mode"] = combat_mode
                break

    def get_spawn_statistics(self):
        """Get statistics about spawned units"""
        total_units = len(self.spawned_units)
        alive_units = len([u for u in self.spawned_units if u["alive"]])
        total_groups = len(self.groups)

        return {
            "total_units": total_units,
            "alive_units": alive_units,
            "dead_units": total_units - alive_units,
            "total_groups": total_groups
        }

    def cleanup_dead_units(self):
        """Remove dead units from tracking"""
        self.spawned_units = [u for u in self.spawned_units if u["alive"]]

        # Update groups
        for group in self.groups:
            group["units"] = [u for u in group["units"] if u["alive"]]


# Demo usage
ai_system = AISpawnSystem()

# Spawn some groups
group1 = ai_system.spawn_group([1000, 2000, 0], 4, "WEDGE", "EAST")
group2 = ai_system.spawn_group([1200, 1800, 0], 3, "LINE", "WEST")

# Set behaviors
ai_system.set_group_behavior(group1["id"], "COMBAT", "RED")
ai_system.set_group_behavior(group2["id"], "AWARE", "YELLOW")

# Move groups
ai_system.move_group(group1["id"], [1100, 1900, 0])
ai_system.move_group(group2["id"], [1300, 1700, 0])

print(f"Spawned {len(ai_system.spawned_units)} AI units in {len(ai_system.groups)} groups")
stats = ai_system.get_spawn_statistics()
print(f"Spawn Statistics: {stats}")