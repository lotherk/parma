# Example 7: Event System and Triggers
# Demonstrates event-driven programming and trigger management

class EventSystem:
    def __init__(self):
        self.events = {}
        self.triggers = {}
        self.active_events = []

    def register_event(self, event_id, event_type, conditions=None, actions=None):
        """Register a new event"""
        self.events[event_id] = {
            "type": event_type,
            "conditions": conditions or [],
            "actions": actions or [],
            "enabled": True
        }

    def create_trigger(self, trigger_id, position, radius, activation_type="PRESENT", repeatable=True):
        """Create a trigger area"""
        self.triggers[trigger_id] = {
            "position": position,
            "radius": radius,
            "activation": activation_type,
            "repeatable": repeatable,
            "activated": False,
            "activation_count": 0
        }

    def add_trigger_event(self, trigger_id, event_id):
        """Link an event to a trigger"""
        if trigger_id in self.triggers and event_id in self.events:
            self.triggers[trigger_id]["event"] = event_id
            return True
        return False

    def check_trigger_activation(self, trigger_id, player_positions):
        """Check if trigger should activate based on player positions"""
        if trigger_id not in self.triggers:
            return False

        trigger = self.triggers[trigger_id]

        # Check if any player is within radius
        for player_pos in player_positions:
            distance = ((player_pos[0] - trigger["position"][0]) ** 2 +
                       (player_pos[1] - trigger["position"][1]) ** 2) ** 0.5

            if distance <= trigger["radius"]:
                if not trigger["activated"] or trigger["repeatable"]:
                    trigger["activated"] = True
                    trigger["activation_count"] += 1
                    return True

        return False

    def activate_event(self, event_id):
        """Activate an event"""
        if event_id in self.events and self.events[event_id]["enabled"]:
            event = self.events[event_id]
            self.active_events.append(event_id)

            # Execute actions (in SQF, these would be actual commands)
            for action in event["actions"]:
                print(f"Executing event action: {action}")

            return True
        return False

    def deactivate_event(self, event_id):
        """Deactivate an event"""
        if event_id in self.active_events:
            self.active_events.remove(event_id)
            return True
        return False

    def get_trigger_status(self, trigger_id):
        """Get status of a trigger"""
        if trigger_id in self.triggers:
            trigger = self.triggers[trigger_id]
            return {
                "activated": trigger["activated"],
                "activation_count": trigger["activation_count"],
                "position": trigger["position"],
                "radius": trigger["radius"]
            }
        return None

    def update_system(self, player_positions):
        """Update the event system (call periodically)"""
        activated_triggers = []

        for trigger_id, trigger in self.triggers.items():
            if self.check_trigger_activation(trigger_id, player_positions):
                activated_triggers.append(trigger_id)
                if "event" in trigger:
                    self.activate_event(trigger["event"])

        return activated_triggers


# Demo usage
event_system = EventSystem()

# Create triggers
event_system.create_trigger("ambush_zone", [1000, 2000, 0], 50, "PRESENT", True)
event_system.create_trigger("extraction_point", [1500, 1800, 0], 30, "PRESENT", False)

# Register events
event_system.register_event("ambush_triggered", "enemy_spawn",
                           actions=["spawn_enemy_patrol", "play_sound_alarm"])
event_system.register_event("extraction_available", "objective_update",
                           actions=["show_extraction_marker", "enable_fast_travel"])

# Link events to triggers
event_system.add_trigger_event("ambush_zone", "ambush_triggered")
event_system.add_trigger_event("extraction_point", "extraction_available")

# Simulate player movement
player_positions = [[900, 1950, 0], [950, 2050, 0]]  # Near ambush zone

activated = event_system.update_system(player_positions)
print(f"Activated triggers: {activated}")

# Check trigger status
status = event_system.get_trigger_status("ambush_zone")
if status:
    print(f"Ambush zone status: activated={status['activated']}, count={status['activation_count']}")

print(f"Active events: {event_system.active_events}")