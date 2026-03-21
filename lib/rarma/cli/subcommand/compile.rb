require 'rarma/compiler'
class Rarma::CLI::Subcommand::Compile
  extend Rarma::CLI::Subcommand
  attr_reader :description
  def initialize
    @description = "Transcompile ruby to sqf code"
  end
  def main
    p = Trollop::Parser.new do
      banner <<EOB
Usage
  rarma [global options] compile [options] srcfile

#{@description}
EOB
      banner ""
      opt :output, 'SQF output file', :short => 'o', :default => 'script.sqf'
      opt :include, 'Include library path', :short => 'I', :type => :strings
    end

    @opts = Trollop::with_standard_exception_handling p do
      raise Trollop::HelpNeeded if ARGV.empty?
      p.parse
    end
    @opts[:include] ||= []
    @opts[:include] << '.'
    Rarma::Compiler.compile ARGV.shift, @opts
  end
end
