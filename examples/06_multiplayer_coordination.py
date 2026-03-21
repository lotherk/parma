# Example 6: Multiplayer Coordination System
# Demonstrates player coordination, team management, and communication

class MultiplayerSystem:
    def __init__(self):
        self.players = {}
        self.teams = {}
        self.objectives = []
        self.communication_channels = {}

    def add_player(self, player_id, name, side="WEST"):
        """Add a player to the system"""
        self.players[player_id] = {
            "name": name,
            "side": side,
            "position": [0, 0, 0],
            "status": "alive",
            "team": None,
            "role": "rifleman",
            "score": 0
        }

    def create_team(self, team_id, name, leader_id):
        """Create a team with a leader"""
        if leader_id not in self.players:
            return False

        self.teams[team_id] = {
            "name": name,
            "leader": leader_id,
            "members": [leader_id],
            "objectives": [],
            "communication_channel": f"team_{team_id}"
        }

        self.players[leader_id]["team"] = team_id
        return True

    def join_team(self, player_id, team_id):
        """Player joins a team"""
        if player_id not in self.players or team_id not in self.teams:
            return False

        if player_id not in self.teams[team_id]["members"]:
            self.teams[team_id]["members"].append(player_id)
            self.players[player_id]["team"] = team_id
            return True
        return False

    def assign_role(self, player_id, role):
        """Assign a role to a player"""
        valid_roles = ["rifleman", "medic", "engineer", "sniper", "leader", "machinegunner"]
        if player_id in self.players and role in valid_roles:
            self.players[player_id]["role"] = role
            return True
        return False

    def update_player_position(self, player_id, position):
        """Update player's position"""
        if player_id in self.players:
            self.players[player_id]["position"] = position
            return True
        return False

    def send_team_message(self, sender_id, team_id, message):
        """Send message to team channel"""
        if sender_id not in self.players or team_id not in self.teams:
            return False

        if sender_id not in self.teams[team_id]["members"]:
            return False

        # In SQF: [sender_id, message] call BIS_fnc_dynamicText or similar
        print(f"[Team {team_id}] {self.players[sender_id]['name']}: {message}")
        return True

    def assign_team_objective(self, team_id, objective_id, description):
        """Assign objective to a team"""
        if team_id not in self.teams:
            return False

        objective = {
            "id": objective_id,
            "description": description,
            "assigned_team": team_id,
            "status": "active",
            "progress": 0
        }

        self.objectives.append(objective)
        self.teams[team_id]["objectives"].append(objective_id)
        return True

    def complete_objective(self, objective_id):
        """Mark an objective as completed"""
        for obj in self.objectives:
            if obj["id"] == objective_id:
                obj["status"] = "completed"
                obj["progress"] = 100

                # Notify team
                team_id = obj["assigned_team"]
                if team_id in self.teams:
                    self.send_team_message("system", team_id, f"Objective completed: {obj['description']}")
                return True
        return False

    def get_team_status(self, team_id):
        """Get detailed status of a team"""
        if team_id not in self.teams:
            return None

        team = self.teams[team_id]
        members = []
        for member_id in team["members"]:
            if member_id in self.players:
                members.append({
                    "id": member_id,
                    "name": self.players[member_id]["name"],
                    "role": self.players[member_id]["role"],
                    "status": self.players[member_id]["status"]
                })

        team_objectives = []
        for obj_id in team["objectives"]:
            for obj in self.objectives:
                if obj["id"] == obj_id:
                    team_objectives.append(obj)
                    break

        return {
            "name": team["name"],
            "leader": team["leader"],
            "member_count": len(members),
            "members": members,
            "objectives": team_objectives
        }

    def get_player_statistics(self):
        """Get statistics about all players"""
        total_players = len(self.players)
        alive_players = len([p for p in self.players.values() if p["status"] == "alive"])
        total_teams = len(self.teams)

        side_counts = {}
        for player in self.players.values():
            side = player["side"]
            side_counts[side] = side_counts.get(side, 0) + 1

        return {
            "total_players": total_players,
            "alive_players": alive_players,
            "dead_players": total_players - alive_players,
            "total_teams": total_teams,
            "side_distribution": side_counts
        }


# Demo usage
mp_system = MultiplayerSystem()

# Add players
mp_system.add_player("player1", "Alpha Leader", "WEST")
mp_system.add_player("player2", "Bravo One", "WEST")
mp_system.add_player("player3", "Charlie Medic", "WEST")
mp_system.add_player("enemy1", "Opfor Sniper", "EAST")

# Create team
mp_system.create_team("alpha_team", "Alpha Squad", "player1")

# Join team
mp_system.join_team("player2", "alpha_team")
mp_system.join_team("player3", "alpha_team")

# Assign roles
mp_system.assign_role("player3", "medic")

# Assign objective
mp_system.assign_team_objective("alpha_team", "secure_zone", "Secure the marked zone")

# Send team message
mp_system.send_team_message("player1", "alpha_team", "Moving to objective")

# Update positions
mp_system.update_player_position("player1", [1000, 2000, 0])

print("Multiplayer system initialized")
stats = mp_system.get_player_statistics()
print(f"Player Statistics: {stats}")

team_status = mp_system.get_team_status("alpha_team")
if team_status:
    print(f"Team Status: {team_status['name']} has {team_status['member_count']} members")