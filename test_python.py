# Test Python script for rarma transpilation
class TestMission:
    def __init__(self):
        self.name = "Python Demo Mission"
        self.players = []

    def add_player(self, player_name):
        self.players.append(player_name)
        print(f"Added player: {player_name}")

    def start_mission(self):
        print(f"Starting mission: {self.name}")
        print(f"Total players: {len(self.players)}")

    def has_players(self):
        return len(self.players) > 0


# Create and run mission
mission = TestMission()
mission.add_player("Alice")
mission.add_player("Bob")

if mission.has_players():
    mission.start_mission()
    print("Mission completed!")
else:
    print("No players found!")