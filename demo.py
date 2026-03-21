# Simple test script for Parma compilation
class TestMission:
    def __init__(self):
        self.name = "Demo Mission"
        self.players = []

    def add_player(self, player_name):
        self.players.append(player_name)
        print(f"Added player: {player_name}")

    def start(self):
        print(f"Starting mission: {self.name}")
        print(f"Total players: {len(self.players)}")


# Create and run mission
mission = TestMission()
mission.add_player("Alice")
mission.add_player("Bob")
mission.start()