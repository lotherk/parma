import random
import math

def generate_random_units(count):
    units = []
    for i in range(count):
        x = random.uniform(0, 10000)
        y = random.uniform(0, 10000)
        z = random.uniform(0, 100)
        unit_type = random.choice(["B_Soldier_F", "B_Soldier_GL_F", "B_Soldier_AR_F"])
        units.append({
            "id": i,
            "position": [x, y, z],
            "type": unit_type,
            "health": 100,
            "ammo": 30
        })
    return units

def calculate_distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    dz = pos1[2] - pos2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def find_closest_unit(target_pos, units):
    closest = None
    min_distance = float('inf')
    for unit in units:
        dist = calculate_distance(target_pos, unit["position"])
        if dist < min_distance:
            min_distance = dist
            closest = unit
    return closest

def spawn_units_on_map():
    print("Generating random units...")
    units = generate_random_units(1000)

    print("Spawning units...")
    for unit in units:
        pos = unit["position"]
        unit_type = unit["type"]
        # In SQF: createUnit [pos, group, "this setUnitLoadout unit_type"]
        print(f"Spawning {unit_type} at {pos}")

    print("Finding closest unit to center...")
    center = [5000, 5000, 0]
    closest = find_closest_unit(center, units)
    if closest:
        print(f"Closest unit: {closest['id']} at distance {calculate_distance(center, closest['position'])}")

    return units

def complex_ai_behavior(units):
    groups = {}
    for unit in units:
        group_id = unit["id"] // 10
        if group_id not in groups:
            groups[group_id] = []
        groups[group_id].append(unit)

    print("Processing AI groups...")
    for group_id, group_units in groups.items():
        leader = group_units[0]
        print(f"Group {group_id} led by unit {leader['id']}")

        for unit in group_units[1:]:
            # Move towards leader
            leader_pos = leader["position"]
            unit_pos = unit["position"]
            # Complex movement logic would go here
            print(f"Unit {unit['id']} moving towards leader at {leader_pos}")

def weather_simulation():
    weather_types = ["clear", "cloudy", "rain", "storm"]
    current_weather = random.choice(weather_types)

    if current_weather == "rain":
        intensity = random.uniform(0.1, 1.0)
        print(f"Setting rain with intensity {intensity}")
    elif current_weather == "storm":
        print("Creating lightning effects")
        for i in range(5):
            x = random.uniform(0, 10000)
            y = random.uniform(0, 10000)
            print(f"Lightning strike at ({x}, {y})")

def inventory_management():
    weapons = ["arifle_MX_F", "arifle_MXC_F", "arifle_MXM_F"]
    magazines = ["30Rnd_65x39_caseless_mag", "30Rnd_65x39_caseless_mag_Tracer"]

    player_inventory = {
        "primary": random.choice(weapons),
        "magazines": [random.choice(magazines) for _ in range(5)],
        "items": ["FirstAidKit", "HandGrenade"]
    }

    print("Player inventory:")
    for key, value in player_inventory.items():
        print(f"  {key}: {value}")

def main():
    print("Starting complex ArmA mission...")

    units = spawn_units_on_map()
    complex_ai_behavior(units)
    weather_simulation()
    inventory_management()

    print("Mission setup complete!")

if __name__ == "__main__":
    main()