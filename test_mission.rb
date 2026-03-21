#!/usr/bin/env ruby

# Test Rarma project - Simple mission example
class MyMission
  def initialize
    @players = []
    @mission_name = "Test Mission"
  end

  def add_player(name)
    @players << name
  end

  def start_mission
    puts "Starting mission: #{@mission_name}"
    @players.each do |player|
      puts "Player: #{player}"
    end
  end

  def check_condition
    if @players.size > 0
      return true
    else
      return false
    end
  end
end

mission = MyMission.new
mission.add_player("Player1")
mission.start_mission

if mission.check_condition
  puts "Mission ready!"
end