# Example 10: Advanced Mission Logic with State Machines
# Demonstrates complex mission flow using state machines and conditional logic

class MissionStateMachine:
    def __init__(self):
        self.current_state = "initialization"
        self.states = {
            "initialization": {
                "on_enter": self._enter_initialization,
                "transitions": {"start": "briefing"}
            },
            "briefing": {
                "on_enter": self._enter_briefing,
                "transitions": {"accept": "insertion", "decline": "aborted"}
            },
            "insertion": {
                "on_enter": self._enter_insertion,
                "transitions": {"landed": "recon", "abort": "extraction"}
            },
            "recon": {
                "on_enter": self._enter_recon,
                "transitions": {"target_found": "assault", "timeout": "extraction"}
            },
            "assault": {
                "on_enter": self._enter_assault,
                "transitions": {"objective_complete": "extraction", "objective_failed": "failed"}
            },
            "extraction": {
                "on_enter": self._enter_extraction,
                "transitions": {"extracted": "debriefing", "killed": "failed"}
            },
            "debriefing": {
                "on_enter": self._enter_debriefing,
                "transitions": {"complete": "completed"}
            },
            "completed": {
                "on_enter": self._enter_completed,
                "transitions": {}
            },
            "failed": {
                "on_enter": self._enter_failed,
                "transitions": {}
            },
            "aborted": {
                "on_enter": self._enter_aborted,
                "transitions": {}
            }
        }
        self.state_data = {}
        self.mission_timer = 0

    def start_mission(self):
        """Start the mission state machine"""
        self._change_state("start")

    def trigger_event(self, event):
        """Trigger a state transition event"""
        if self.current_state in self.states:
            transitions = self.states[self.current_state]["transitions"]
            if event in transitions:
                self._change_state(event)
                return True
        return False

    def update(self, delta_time):
        """Update mission state (call every frame/tick)"""
        self.mission_timer += delta_time

        # State-specific updates
        if self.current_state == "recon":
            # Check for recon timeout
            if self.mission_timer > self.state_data.get("recon_timeout", 300):
                self.trigger_event("timeout")
        elif self.current_state == "assault":
            # Check objective progress
            if self._check_objective_progress() >= 100:
                self.trigger_event("objective_complete")

    def get_current_state_info(self):
        """Get information about current state"""
        return {
            "state": self.current_state,
            "description": self._get_state_description(),
            "timer": self.mission_timer,
            "data": self.state_data
        }

    def _change_state(self, event):
        """Change to a new state"""
        old_state = self.current_state

        if event == "start":
            new_state = "initialization"
        elif old_state in self.states:
            transitions = self.states[old_state]["transitions"]
            new_state = transitions.get(event, old_state)
        else:
            return

        if new_state != old_state:
            self.current_state = new_state
            print(f"Mission state changed: {old_state} -> {new_state}")

            # Execute on_enter function
            if "on_enter" in self.states[new_state]:
                self.states[new_state]["on_enter"]()

    def _get_state_description(self):
        """Get human-readable description of current state"""
        descriptions = {
            "initialization": "Preparing mission systems...",
            "briefing": "Receiving mission briefing",
            "insertion": "Inserting into AO",
            "recon": "Conducting reconnaissance",
            "assault": "Executing assault on objective",
            "extraction": "Extracting from AO",
            "debriefing": "Mission debriefing",
            "completed": "Mission completed successfully",
            "failed": "Mission failed",
            "aborted": "Mission aborted"
        }
        return descriptions.get(self.current_state, "Unknown state")

    def _check_objective_progress(self):
        """Check progress on current objectives"""
        # Simulate objective progress
        return min(100, self.mission_timer / 10)  # Increases over time

    # State enter functions
    def _enter_initialization(self):
        print("Mission systems initializing...")
        self.state_data = {"initialized": True}

    def _enter_briefing(self):
        print("Squad leader: 'Listen up! Here's the mission...'")
        self.state_data = {"briefing_given": True}

    def _enter_insertion(self):
        print("Insertion helicopter inbound...")
        self.state_data = {"insertion_started": True}

    def _enter_recon(self):
        print("Moving to recon positions...")
        self.state_data = {"recon_timeout": self.mission_timer + 300}  # 5 minutes

    def _enter_assault(self):
        print("Assault team moving in!")
        self.state_data = {"assault_started": True}

    def _enter_extraction(self):
        print("Extraction team en route...")
        self.state_data = {"extraction_called": True}

    def _enter_debriefing(self):
        print("Welcome back, soldier. Mission debriefing:")
        success = self.current_state == "debriefing"
        print(f"Mission Status: {'SUCCESS' if success else 'FAILED'}")

    def _enter_completed(self):
        print("🎉 MISSION ACCOMPLISHED! 🎉")
        self.state_data = {"mission_success": True}

    def _enter_failed(self):
        print("💀 MISSION FAILED 💀")
        self.state_data = {"mission_success": False}

    def _enter_aborted(self):
        print("🚫 MISSION ABORTED 🚫")
        self.state_data = {"mission_aborted": True}


# Demo usage
mission = MissionStateMachine()
mission.start_mission()

print(f"Initial state: {mission.get_current_state_info()['state']}")

# Simulate mission progression
mission.trigger_event("accept")  # Accept briefing
print(f"After briefing: {mission.get_current_state_info()['state']}")

mission.trigger_event("landed")  # Land at insertion point
print(f"After insertion: {mission.get_current_state_info()['state']}")

mission.trigger_event("target_found")  # Find the target
print(f"After recon: {mission.get_current_state_info()['state']}")

# Simulate time passing during assault
for i in range(50):  # 50 updates
    mission.update(1)  # 1 second per update

print(f"Final state: {mission.get_current_state_info()['state']}")
print(f"Mission completed in {mission.mission_timer} seconds")