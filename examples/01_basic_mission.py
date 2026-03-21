# Example 1: Basic Mission Framework
# Demonstrates fundamental mission structure with objectives and win conditions

import random

class BasicMission:
    def __init__(self):
        self.mission_name = "Operation Python"
        self.objectives = []
        self.completed_objectives = []
        self.difficulty = "normal"
        self.max_time = 3600  # 1 hour in seconds
        self.start_time = 0

    def add_objective(self, objective_id, description, required=True):
        """Add a mission objective"""
        objective = {
            "id": objective_id,
            "description": description,
            "required": required,
            "completed": False,
            "progress": 0,
            "max_progress": 100
        }
        self.objectives.append(objective)

    def complete_objective(self, objective_id, progress=100):
        """Mark an objective as completed"""
        for obj in self.objectives:
            if obj["id"] == objective_id:
                obj["completed"] = True
                obj["progress"] = progress
                self.completed_objectives.append(objective_id)
                print(f"Objective completed: {obj['description']}")

    def get_mission_status(self):
        """Get current mission status"""
        completed_count = len([obj for obj in self.objectives if obj["completed"]])
        total_objectives = len(self.objectives)
        required_completed = len([obj for obj in self.objectives if obj["completed"] and obj["required"]])

        return {
            "name": self.mission_name,
            "objectives_completed": completed_count,
            "total_objectives": total_objectives,
            "required_completed": required_completed,
            "success": required_completed == len([obj for obj in self.objectives if obj["required"]])
        }

    def check_win_condition(self):
        """Check if mission win conditions are met"""
        status = self.get_mission_status()
        return status["success"]

    def initialize_mission(self):
        """Set up the mission"""
        print(f"Initializing mission: {self.mission_name}")

        # Add objectives
        self.add_objective("recon", "Conduct reconnaissance of the AO", True)
        self.add_objective("secure", "Secure the objective area", True)
        self.add_objective("extract", "Extract all friendly units", True)
        self.add_objective("bonus", "Destroy enemy communications", False)

        print(f"Added {len(self.objectives)} objectives")

    def update_mission(self, current_time):
        """Update mission state (called periodically)"""
        # Simulate some objectives completing over time
        if current_time > 300 and "recon" not in self.completed_objectives:  # 5 minutes
            self.complete_objective("recon")

        if current_time > 600 and "secure" not in self.completed_objectives:  # 10 minutes
            self.complete_objective("secure")

        if current_time > 900 and "extract" not in self.completed_objectives:  # 15 minutes
            self.complete_objective("extract")

    def end_mission(self):
        """End the mission and show results"""
        status = self.get_mission_status()
        if status["success"]:
            print(f"MISSION SUCCESS: {self.mission_name}")
            print(f"Completed {status['objectives_completed']}/{status['total_objectives']} objectives")
        else:
            print(f"MISSION FAILED: {self.mission_name}")
            print(f"Only completed {status['required_completed']} required objectives")


# Mission execution
mission = BasicMission()
mission.initialize_mission()

# Simulate mission progression
for time in range(0, 1200, 60):  # Every minute for 20 minutes
    mission.update_mission(time)

mission.end_mission()