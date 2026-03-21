require 'rarma'
require 'trollop'

module Rarma::CLI
  def self.options
    @options
  end
  def self.main
    subs = []
    Rarma::CLI::Subcommand.subcommands.each { |subcmd| subs << subcmd.to_s.downcase }
    p = Trollop::Parser.new do
      version Rarma::VERSION
      banner <<EOB
rarma #{Rarma::VERSION}

Usage
  rarma [global options] <subcommand> [subcommand options]

Available subcommands:
EOB
      Rarma::CLI::Subcommand.subcommands.each do |subcmd|
        subcmd = subcmd.downcase
        len = 16
        diff = len - subcmd.length
        inst = Rarma::CLI::Subcommand[subcmd]
        desc = Rarma::CLI::Subcommand[subcmd].description rescue nil
        banner "  %s%#{diff}s - %s" % [subcmd, "", desc]
      end
      banner ""
      banner "Global options:"
      opt :debug, "Enable debug messages", :default => false, :short => '-d'
      stop_on subs
    end
    @options = Trollop::with_standard_exception_handling p do
      raise Trollop::HelpNeeded if ARGV.empty?
      p.parse
    end

    Rarma.logger.level = Logger::DEBUG if @options[:debug]

    subcmd = ARGV.shift

    begin
      Rarma::CLI::Subcommand[subcmd].main
    rescue RuntimeError => e
      unless @options[:debug]
        puts "Error: #{e.message}"
        exit 1
      else
        raise
      end
    rescue
      raise
    end

  end
end

require 'rarma/cli/subcommand'
