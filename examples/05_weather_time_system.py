# Example 5: Weather and Time Management
# Demonstrates dynamic weather changes and time progression

class WeatherSystem:
    def __init__(self):
        self.current_weather = {
            "overcast": 0.5,
            "rain": 0.0,
            "fog": 0.0,
            "wind_speed": 5.0,
            "wind_direction": 180
        }
        self.time_acceleration = 1.0
        self.day_night_cycle = True

    def set_weather(self, overcast=None, rain=None, fog=None, wind_speed=None, wind_direction=None):
        """Set weather parameters"""
        if overcast is not None:
            self.current_weather["overcast"] = max(0.0, min(1.0, overcast))
        if rain is not None:
            self.current_weather["rain"] = max(0.0, min(1.0, rain))
        if fog is not None:
            self.current_weather["fog"] = max(0.0, min(1.0, fog))
        if wind_speed is not None:
            self.current_weather["wind_speed"] = max(0.0, wind_speed)
        if wind_direction is not None:
            self.current_weather["wind_direction"] = wind_direction % 360

        # In SQF: 0 setOvercast overcast; 0 setRain rain; etc.

    def start_weather_transition(self, target_weather, duration=300):
        """Gradually change weather over time"""
        # Calculate steps for smooth transition
        steps = duration // 10  # Update every 10 seconds
        transition = {}

        for key in target_weather:
            if key in self.current_weather:
                current = self.current_weather[key]
                target = target_weather[key]
                step_size = (target - current) / steps
                transition[key] = {
                    "current": current,
                    "target": target,
                    "step": step_size,
                    "remaining_steps": steps
                }

        self.weather_transition = transition
        return transition

    def update_weather_transition(self):
        """Update weather transition (call every few seconds)"""
        if not hasattr(self, 'weather_transition') or not self.weather_transition:
            return False

        completed = True
        for key, trans in self.weather_transition.items():
            if trans["remaining_steps"] > 0:
                completed = False
                trans["current"] += trans["step"]
                trans["remaining_steps"] -= 1
                self.current_weather[key] = trans["current"]

        if completed:
            delattr(self, 'weather_transition')
            return True

        return False

    def set_time_acceleration(self, acceleration):
        """Set time acceleration multiplier"""
        self.time_acceleration = max(0.1, min(120.0, acceleration))
        # In SQF: setTimeMultiplier acceleration

    def set_day_time(self, hour, minute=0):
        """Set specific time of day"""
        # In SQF: setDate [year, month, day, hour, minute]
        self.target_time = {"hour": hour, "minute": minute}

    def skip_time(self, hours):
        """Skip forward in time"""
        # In SQF: skipTime hours
        self.time_skip = hours

    def toggle_day_night_cycle(self, enabled=True):
        """Enable or disable automatic day/night cycle"""
        self.day_night_cycle = enabled

    def get_weather_description(self):
        """Get human-readable weather description"""
        weather = self.current_weather

        if weather["rain"] > 0.7:
            condition = "Heavy Rain"
        elif weather["rain"] > 0.3:
            condition = "Light Rain"
        elif weather["overcast"] > 0.8:
            condition = "Overcast"
        elif weather["overcast"] > 0.5:
            condition = "Cloudy"
        elif weather["fog"] > 0.5:
            condition = "Foggy"
        else:
            condition = "Clear"

        wind_desc = f"Wind: {weather['wind_speed']} m/s from {weather['wind_direction']}°"

        return f"{condition}, {wind_desc}"

    def simulate_weather_event(self, event_type):
        """Trigger special weather events"""
        events = {
            "storm": {"overcast": 1.0, "rain": 0.8, "wind_speed": 15.0},
            "sandstorm": {"overcast": 0.9, "fog": 0.7, "wind_speed": 20.0},
            "clear": {"overcast": 0.0, "rain": 0.0, "fog": 0.0, "wind_speed": 2.0},
            "sunny": {"overcast": 0.2, "rain": 0.0, "fog": 0.0, "wind_speed": 3.0}
        }

        if event_type in events:
            self.start_weather_transition(events[event_type], 180)  # 3 minutes
            return True
        return False


class TimeSystem:
    def __init__(self):
        self.mission_start_time = 12 * 3600  # Start at noon (12:00)
        self.current_time = self.mission_start_time
        self.time_multiplier = 1.0

    def advance_time(self, seconds):
        """Advance mission time"""
        self.current_time += seconds * self.time_multiplier

    def get_time_string(self):
        """Get current time as HH:MM format"""
        total_seconds = int(self.current_time)
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds // 60) % 60
        return "02d"

    def is_daytime(self):
        """Check if it's currently daytime"""
        hours = (self.current_time // 3600) % 24
        return 6 <= hours <= 18  # 6 AM to 6 PM

    def time_until_dark(self):
        """Get seconds until nightfall"""
        hours = (self.current_time // 3600) % 24
        if hours >= 18:
            return (30 - hours) * 3600  # Next day
        else:
            return (18 - hours) * 3600


# Demo usage
weather = WeatherSystem()
time_sys = TimeSystem()

print("Initial weather:", weather.get_weather_description())
print("Initial time:", time_sys.get_time_string())

# Start a storm
weather.simulate_weather_event("storm")
print("Starting storm transition...")

# Simulate time passing and weather updating
for i in range(18):  # 18 updates = 3 minutes at 10-second intervals
    weather.update_weather_transition()
    time_sys.advance_time(10)

print("After storm:", weather.get_weather_description())
print("Time after storm:", time_sys.get_time_string())
print("Is daytime?", time_sys.is_daytime())