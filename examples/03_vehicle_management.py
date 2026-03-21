# Example 3: Vehicle Management System
# Demonstrates vehicle spawning, management, and maintenance

import random

class VehicleSystem:
    def __init__(self):
        self.vehicles = []
        self.vehicle_types = {
            "car": ["C_Offroad_01_F", "B_MRAP_01_F", "O_MRAP_02_F"],
            "truck": ["C_Van_01_transport_F", "B_Truck_01_transport_F", "O_Truck_02_transport_F"],
            "tank": ["B_MBT_01_cannon_F", "O_MBT_02_cannon_F"],
            "helicopter": ["B_Heli_Light_01_F", "O_Heli_Light_02_F"],
            "plane": ["B_Plane_CAS_01_F", "O_Plane_CAS_02_F"]
        }
        self.fuel_stations = []
        self.repair_stations = []

    def spawn_vehicle(self, position, vehicle_type="car", side="CIV"):
        """Spawn a vehicle at the given position"""
        if vehicle_type not in self.vehicle_types:
            vehicle_type = "car"

        class_name = random.choice(self.vehicle_types[vehicle_type])

        vehicle = {
            "id": f"vehicle_{len(self.vehicles)}",
            "class": class_name,
            "position": position,
            "type": vehicle_type,
            "side": side,
            "fuel": 1.0,
            "damage": 0.0,
            "crew": [],
            "cargo": [],
            "locked": False
        }

        self.vehicles.append(vehicle)
        return vehicle

    def assign_crew(self, vehicle_id, crew_members):
        """Assign crew to a vehicle"""
        for vehicle in self.vehicles:
            if vehicle["id"] == vehicle_id:
                vehicle["crew"] = crew_members
                # In SQF: {_x moveInAny vehicle_object} forEach crew_members
                break

    def load_cargo(self, vehicle_id, items):
        """Load items into vehicle cargo"""
        for vehicle in self.vehicles:
            if vehicle["id"] == vehicle_id:
                vehicle["cargo"].extend(items)
                # In SQF: {vehicle_object addItemCargoGlobal _x} forEach items
                break

    def set_vehicle_lock(self, vehicle_id, locked=True):
        """Lock or unlock a vehicle"""
        for vehicle in self.vehicles:
            if vehicle["id"] == vehicle_id:
                vehicle["locked"] = locked
                # In SQF: vehicle_object lock (if locked then 2 else 0)
                break

    def refuel_vehicle(self, vehicle_id, fuel_amount=1.0):
        """Refuel a vehicle"""
        for vehicle in self.vehicles:
            if vehicle["id"] == vehicle_id:
                vehicle["fuel"] = min(1.0, vehicle["fuel"] + fuel_amount)
                # In SQF: vehicle_object setFuel vehicle["fuel"]
                break

    def repair_vehicle(self, vehicle_id, repair_amount=1.0):
        """Repair a vehicle"""
        for vehicle in self.vehicles:
            if vehicle["id"] == vehicle_id:
                vehicle["damage"] = max(0.0, vehicle["damage"] - repair_amount)
                # In SQF: vehicle_object setDamage vehicle["damage"]
                break

    def add_fuel_station(self, position, radius=10):
        """Add a fuel station location"""
        station = {
            "position": position,
            "radius": radius,
            "type": "fuel"
        }
        self.fuel_stations.append(station)

    def add_repair_station(self, position, radius=10):
        """Add a repair station location"""
        station = {
            "position": position,
            "radius": radius,
            "type": "repair"
        }
        self.repair_stations.append(station)

    def find_nearest_service(self, vehicle_position, service_type):
        """Find nearest fuel or repair station"""
        stations = self.fuel_stations if service_type == "fuel" else self.repair_stations

        if not stations:
            return None

        nearest = min(stations,
                     key=lambda s: ((s["position"][0] - vehicle_position[0]) ** 2 +
                                   (s["position"][1] - vehicle_position[1]) ** 2) ** 0.5)
        return nearest

    def get_vehicle_status(self, vehicle_id):
        """Get detailed status of a vehicle"""
        for vehicle in self.vehicles:
            if vehicle["id"] == vehicle_id:
                return {
                    "id": vehicle["id"],
                    "class": vehicle["class"],
                    "fuel": vehicle["fuel"],
                    "damage": vehicle["damage"],
                    "crew_count": len(vehicle["crew"]),
                    "cargo_count": len(vehicle["cargo"]),
                    "locked": vehicle["locked"]
                }
        return None

    def get_fleet_statistics(self):
        """Get statistics about the entire vehicle fleet"""
        total_vehicles = len(self.vehicles)
        operational = len([v for v in self.vehicles if v["damage"] < 0.5 and v["fuel"] > 0.1])
        damaged = len([v for v in self.vehicles if v["damage"] >= 0.5])
        out_of_fuel = len([v for v in self.vehicles if v["fuel"] <= 0.1])

        return {
            "total_vehicles": total_vehicles,
            "operational": operational,
            "damaged": damaged,
            "out_of_fuel": out_of_fuel,
            "service_stations": len(self.fuel_stations) + len(self.repair_stations)
        }


# Demo usage
vehicle_system = VehicleSystem()

# Add service stations
vehicle_system.add_fuel_station([500, 500, 0])
vehicle_system.add_repair_station([600, 600, 0])

# Spawn various vehicles
car = vehicle_system.spawn_vehicle([1000, 2000, 0], "car", "WEST")
truck = vehicle_system.spawn_vehicle([1100, 2100, 0], "truck", "EAST")
tank = vehicle_system.spawn_vehicle([1200, 2200, 0], "tank", "WEST")

# Simulate usage
vehicle_system.load_cargo(truck["id"], ["FirstAidKit", "ToolKit", "30Rnd_65x39_caseless_mag"])
vehicle_system.refuel_vehicle(car["id"], 0.8)
vehicle_system.repair_vehicle(tank["id"], 0.2)

print(f"Spawned {len(vehicle_system.vehicles)} vehicles")
stats = vehicle_system.get_fleet_statistics()
print(f"Fleet Statistics: {stats}")

# Find nearest fuel station for the car
nearest_fuel = vehicle_system.find_nearest_service(car["position"], "fuel")
if nearest_fuel:
    print(f"Nearest fuel station to car: {nearest_fuel['position']}")