# Advanced Parma Demo: Loot Population System
# This demo creates a loot system that finds garages and populates them with random equipment

import random

class LootSystem:
    def __init__(self):
        # Garage and building class names for loot spawning
        self.garage_classes = [
            "Land_Garage_V1_F",
            "Land_Garage_V2_F",
            "Land_i_Garage_V1_F",
            "Land_i_Garage_V2_F",
            "Land_Garage_Row_F",
            "Land_GarageOffice_01_F"
        ]

        # Weapon classes (rifles, pistols, etc.)
        self.weapon_classes = [
            "arifle_MX_F",           # MX Rifle
            "arifle_MX_SW_F",        # MX SW LMG
            "arifle_MXC_F",          # MXC Carbine
            "srifle_EBR_F",          # Mk18 ABR
            "LMG_Mk200_F",           # Mk200 LMG
            "hgun_P07_F",            # P07 Pistol
            "hgun_ACPC2_F",          # ACP-C2 Pistol
            "launch_RPG32_F",        # RPG-42 Launcher
            "arifle_TRG21_F",        # TRG-21 Rifle
            "arifle_Katiba_F"        # Katiba Rifle
        ]

        # Magazine classes for the weapons
        self.magazine_classes = [
            "30Rnd_65x39_caseless_mag",      # 6.5mm 30rnd
            "100Rnd_65x39_caseless_mag",     # 6.5mm 100rnd
            "20Rnd_556x45_UW_mag",           # 5.56mm 20rnd underwater
            "30Rnd_556x45_Stanag",           # 5.56mm 30rnd
            "16Rnd_9x21_Mag",                # 9mm 16rnd
            "9Rnd_45ACP_Mag",                # .45 ACP 9rnd
            "RPG32_F",                       # RPG-42 rocket
            "1Rnd_HE_Grenade_shell",         # 40mm HE grenade
            "HandGrenade",                   # M67 Hand Grenade
            "SmokeShell"                     # Smoke Grenade
        ]

        # Item classes (medical, tools, etc.)
        self.item_classes = [
            "FirstAidKit",           # First Aid Kit
            "Medikit",               # Medical Kit
            "ToolKit",               # Toolkit
            "MineDetector",          # Mine Detector
            "Binocular",             # Binoculars
            "ItemGPS",               # GPS
            "ItemMap",               # Map
            "ItemCompass",           # Compass
            "ItemWatch",             # Watch
            "ItemRadio",             # Radio
            "NVGoggles",             # Night Vision Goggles
            "Rangefinder",           # Rangefinder
            "Laserdesignator",       # Laser Designator
            "B_UavTerminal",         # UAV Terminal
            "muzzle_snds_H",         # 6.5mm Suppressor
            "optic_Arco",            # ARCO Optic
            "acc_flashlight",        # Flashlight
            "V_PlateCarrier1_rgr",   # Carrier Rig
            "H_HelmetB",             # Combat Helmet
            "U_B_CombatUniform_mcam" # Combat Fatigues
        ]

        self.found_buildings = []

    def find_buildings(self, center_position, radius=500):
        """Find all garage/building objects within radius of center position"""
        # In SQF: nearestObjects [center_position, self.garage_classes, radius]
        # For demo, we'll simulate finding some buildings
        self.found_buildings = [
            {"position": [center_position[0] + 50, center_position[1] + 25, 0], "class": "Land_Garage_V1_F"},
            {"position": [center_position[0] - 30, center_position[1] + 40, 0], "class": "Land_Garage_V2_F"},
            {"position": [center_position[0] + 80, center_position[1] - 15, 0], "class": "Land_i_Garage_V1_F"}
        ]
        return self.found_buildings

    def generate_loot_for_building(self, building):
        """Generate random loot for a specific building"""
        loot = []

        # Always add 2 guns
        for _ in range(2):
            weapon = random.choice(self.weapon_classes)
            magazine = random.choice(self.magazine_classes)
            loot.append({"type": "weapon", "class": weapon, "magazine": magazine})

        # Add 3 rifles (additional weapons)
        for _ in range(3):
            weapon = random.choice(self.weapon_classes)
            magazine = random.choice(self.magazine_classes)
            loot.append({"type": "rifle", "class": weapon, "magazine": magazine})

        # Add ammo (5-10 magazines)
        ammo_count = random.randint(5, 10)
        for _ in range(ammo_count):
            magazine = random.choice(self.magazine_classes)
            loot.append({"type": "magazine", "class": magazine})

        # Add random items (3-8 items)
        item_count = random.randint(3, 8)
        for _ in range(item_count):
            item = random.choice(self.item_classes)
            loot.append({"type": "item", "class": item})

        return loot

    def populate_building(self, building, loot):
        """Place loot items in a building at random positions"""
        building_pos = building["position"]

        for item in loot:
            # Generate random position within building
            offset_x = random.uniform(-3, 3)
            offset_y = random.uniform(-3, 3)
            item_pos = [building_pos[0] + offset_x, building_pos[1] + offset_y, building_pos[2] + 0.1]

            # Create the item based on type
            if item["type"] == "weapon":
                # Create weapon with magazine
                weapon_holder = f"weapon_holder_{random.randint(1000, 9999)}"
                # In SQF: weapon_holder = "GroundWeaponHolder" createVehicle item_pos;
                # weapon_holder addWeaponCargoGlobal [item["class"], 1];
                # weapon_holder addMagazineCargoGlobal [item["magazine"], random.randint(1, 3)];
            elif item["type"] == "magazine":
                # Create magazine box
                mag_box = f"magazine_box_{random.randint(1000, 9999)}"
                # In SQF: mag_box = "Box_NATO_Ammo_F" createVehicle item_pos;
                # mag_box addMagazineCargoGlobal [item["class"], random.randint(2, 5)];
            elif item["type"] == "item":
                # Create item box
                item_box = f"item_box_{random.randint(1000, 9999)}"
                # In SQF: item_box = "Box_NATO_Uniforms_F" createVehicle item_pos;
                # item_box addItemCargoGlobal [item["class"], 1];

            print(f"Placed {item['type']}: {item['class']} at {item_pos}")

    def initialize_loot_system(self, mission_center=[0, 0, 0], search_radius=500):
        """Main initialization function"""
        print("Initializing Loot Population System...")

        # Find buildings
        buildings = self.find_buildings(mission_center, search_radius)
        print(f"Found {len(buildings)} buildings to populate with loot")

        # Populate each building
        for building in buildings:
            print(f"Populating building: {building['class']} at {building['position']}")
            loot = self.generate_loot_for_building(building)
            print(f"Generated {len(loot)} loot items")
            self.populate_building(building, loot)
            print("---")

        print("Loot population system initialized successfully!")

    def get_loot_statistics(self):
        """Return statistics about generated loot"""
        total_buildings = len(self.found_buildings)
        return {
            "buildings_populated": total_buildings,
            "buildings_found": total_buildings
        }


# Demo usage
loot_system = LootSystem()
loot_system.initialize_loot_system([1000, 2000, 0], 750)

stats = loot_system.get_loot_statistics()
print(f"Loot System Stats: {stats}")