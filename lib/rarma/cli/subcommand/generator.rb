require 'stringio'
class Rarma::CLI::Subcommand::Generator
  attr_reader :description
  def initialize
    @description = "Generate a mission"
  end
  def main
    opts = Trollop::options do
      usage = <<-USAGE
Usage: rarma generate [options] src dst
USAGE
      banner usage
      opt :output, "Destination folder", :type => String
      opt :output_strip, "Strip leading n directories from destination folder", :default => 0
      opt :include, "Include file/folder into destination root and sub folders", :multi => true, :type => String
    end
    src = ARGV.shift
    src ||= "."
    dst = ARGV.shift
    dst ||= "./generated"
    Rarma.logger.debug "Building filetree for #{src}..."
    files = {}
    skippers = ["mission.rb", "description.rb", "init.rb", "parameters.rb"]
    Dir["#{src}/**/*.rb"].sort.each do |f|
      filename = f.gsub(/^#{src}\//, '')
      next if skippers.include?(filename)
      spl = f.split(".")
      type = :eval
      if spl.count > 2
        if spl[-2].downcase == 'sqf'
          type = :compile
        end
      end
      files[type] ||= []
      files[type] << f
    end
    Rarma.logger.debug "Got:\n#{files}"

    files[:eval].flatten.each do |file|
      stdout = StringIO.new
      $stdout = stdout
      load file
      $stdout = STDOUT
      stdout.rewind
      Rarma.logger.debug "output for #{file}:\n#{stdout.read}"
    end if files[:eval]
    skippers.each do |f|
      Rarma.logger.debug "Checking for #{f}"
      if File.exist?("#{src}/#{f}")
        Rarma.logger.debug "Loading #{f}"
        stdout = StringIO.new
        $stdout = stdout
        load f
        $stdout = STDOUT
        stdout.rewind
        Rarma.logger.debug "output for #{f}:\n#{stdout.read}"
      end
    end
  end
end
