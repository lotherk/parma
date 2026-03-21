# Simple test script for rarma compilation
class TestMission
  def initialize
    @name = "Demo Mission"
    @players = []
  end

  def add_player(player_name)
    @players << player_name
    puts "Added player: #{player_name}"
  end

  def start
    puts "Starting mission: #{@name}"
    puts "Total players: #{@players.size}"
  end
end

# Create and run mission
mission = TestMission.new
mission.add_player("Alice")
mission.add_player("Bob")
mission.start