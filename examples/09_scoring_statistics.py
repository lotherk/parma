# Example 9: Mission Scoring and Statistics
# Demonstrates scoring systems, statistics tracking, and performance metrics

class ScoringSystem:
    def __init__(self):
        self.player_scores = {}
        self.team_scores = {}
        self.mission_stats = {
            "start_time": 0,
            "end_time": 0,
            "total_kills": 0,
            "objectives_completed": 0,
            "players_participated": 0
        }
        self.score_multipliers = {
            "kill_infantry": 10,
            "kill_vehicle": 50,
            "kill_aircraft": 100,
            "objective_complete": 200,
            "revive_teammate": 25,
            "heal_teammate": 15,
            "repair_vehicle": 30,
            "resupply_ammo": 20
        }

    def initialize_player(self, player_id, player_name):
        """Initialize scoring for a player"""
        self.player_scores[player_id] = {
            "name": player_name,
            "total_score": 0,
            "kills": {"infantry": 0, "vehicle": 0, "aircraft": 0},
            "objectives": 0,
            "support": {"revives": 0, "heals": 0, "repairs": 0, "resupplies": 0},
            "penalties": 0,
            "playtime": 0
        }

    def award_points(self, player_id, action_type, multiplier=1):
        """Award points for an action"""
        if player_id not in self.player_scores:
            return False

        if action_type not in self.score_multipliers:
            return False

        points = self.score_multipliers[action_type] * multiplier
        self.player_scores[player_id]["total_score"] += points

        # Track specific stats
        if action_type.startswith("kill_"):
            unit_type = action_type.split("_")[1]
            if unit_type in self.player_scores[player_id]["kills"]:
                self.player_scores[player_id]["kills"][unit_type] += 1
        elif action_type == "objective_complete":
            self.player_scores[player_id]["objectives"] += 1
        elif action_type in ["revive_teammate", "heal_teammate", "repair_vehicle", "resupply_ammo"]:
            support_type = action_type.split("_")[1] + "s"
            if support_type in self.player_scores[player_id]["support"]:
                self.player_scores[player_id]["support"][support_type] += 1

        return True

    def apply_penalty(self, player_id, points, reason="unknown"):
        """Apply penalty points"""
        if player_id in self.player_scores:
            self.player_scores[player_id]["penalties"] += points
            self.player_scores[player_id]["total_score"] -= points
            return True
        return False

    def update_playtime(self, player_id, minutes):
        """Update player's playtime"""
        if player_id in self.player_scores:
            self.player_scores[player_id]["playtime"] += minutes
            return True
        return False

    def calculate_team_scores(self):
        """Calculate scores for teams"""
        team_totals = {}
        for player_id, stats in self.player_scores.items():
            # Assume team based on player ID prefix (simplified)
            team = player_id.split("_")[0] if "_" in player_id else "solo"
            if team not in team_totals:
                team_totals[team] = 0
            team_totals[team] += stats["total_score"]

        self.team_scores = team_totals
        return team_totals

    def get_player_rankings(self, sort_by="total_score"):
        """Get player rankings"""
        players = list(self.player_scores.values())

        if sort_by == "total_score":
            players.sort(key=lambda x: x["total_score"], reverse=True)
        elif sort_by == "kills":
            players.sort(key=lambda x: sum(x["kills"].values()), reverse=True)
        elif sort_by == "objectives":
            players.sort(key=lambda x: x["objectives"], reverse=True)

        return players[:10]  # Top 10

    def get_mission_summary(self):
        """Get complete mission summary"""
        total_players = len(self.player_scores)
        total_score = sum(p["total_score"] for p in self.player_scores.values())
        avg_score = total_score / total_players if total_players > 0 else 0

        kill_stats = {
            "infantry": sum(p["kills"]["infantry"] for p in self.player_scores.values()),
            "vehicle": sum(p["kills"]["vehicle"] for p in self.player_scores.values()),
            "aircraft": sum(p["kills"]["aircraft"] for p in self.player_scores.values())
        }

        return {
            "total_players": total_players,
            "total_score": total_score,
            "average_score": avg_score,
            "total_kills": sum(kill_stats.values()),
            "kill_breakdown": kill_stats,
            "top_players": self.get_player_rankings()[:3]
        }

    def export_scores(self, filename="mission_scores.txt"):
        """Export scores to file"""
        # In SQF: copyToClipboard or similar
        content = "Mission Scores:\n"
        for player_id, stats in self.player_scores.items():
            content += f"{stats['name']}: {stats['total_score']} points\n"
        return content


# Demo usage
scoring = ScoringSystem()

# Initialize players
scoring.initialize_player("west_alpha", "Alpha Leader")
scoring.initialize_player("west_bravo", "Bravo Soldier")
scoring.initialize_player("east_sniper", "Enemy Sniper")

# Award points for various actions
scoring.award_points("west_alpha", "kill_infantry", 3)  # 3 infantry kills
scoring.award_points("west_alpha", "objective_complete")  # Complete objective
scoring.award_points("west_bravo", "revive_teammate")     # Revive teammate
scoring.award_points("east_sniper", "kill_vehicle")       # Destroy vehicle

# Update playtime
scoring.update_playtime("west_alpha", 45)  # 45 minutes played

# Calculate team scores
team_scores = scoring.calculate_team_scores()

# Get mission summary
summary = scoring.get_mission_summary()

print("Mission Summary:")
print(f"Total Players: {summary['total_players']}")
print(f"Total Score: {summary['total_score']}")
print(f"Average Score: {summary['average_score']:.1f}")
print(f"Total Kills: {summary['total_kills']}")

# Show top players
rankings = scoring.get_player_rankings()
for i, player in enumerate(rankings[:3], 1):
    print(f"{i}. {player['name']}: {player['total_score']} points")