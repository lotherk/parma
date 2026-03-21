require 'erb'
class Rarma::CLI::Subcommand::New
  extend Rarma::CLI::Subcommand
  attr_reader :description
  def initialize
    @description = "Create a new mission/addon from scratch"
  end
  def main
    p = Trollop::Parser.new do
      banner <<EOB
Usage
  rarma [global options] new [-a|-m] [options] name

#{@description}
EOB
      banner ""
      opt :mission, 'Create a mission', :short => 'm'
      opt :addon, 'Create an addon', :short => 'a'
    end

    @opts = Trollop::with_standard_exception_handling p do
      raise Trollop::HelpNeeded if ARGV.empty?
      p.parse
    end
    @name = ARGV.shift
    if @opts[:addon] && @opts[:mission]
      raise RuntimeError, "Can't specify both -a and -m"
    end
    if @opts[:addon]
      self.class.install_skeleton_files @name, [:addon]
    elsif @opts[:mission]
      self.class.install_skeleton_files @name, [:mission]
    else
      self.class.install_skeleton_files @name, [:mission]
    end
  end

  def self.install_skeleton_files directory, skels
    skels.each do |skel|
      Dir[File.join(Rarma.root, "share", "skeleton", skel.to_s, '**', '/', '*')].each do |e|
        puts e
      end
    end
  end
end
