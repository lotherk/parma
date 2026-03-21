require 'yaml'
require 'fileutils'
require 'open-uri'

module Rarma; module Rake; module Task; module Buildenv
  def install_steam
    unless File.exist? @steamcmd_file
      puts "Downloading #{@steamcmd_url}".colorize(:bold)
      File.open(@steamcmd_file, "wb") do |file|
        file << open(@steamcmd_url).read
      end
      puts "download finished".colorize(:bold)
    else
      puts "File #{@steamcmd_file} already exists.".colorize(:yellow)
    end
  end

  def install_arma
    raise "not implemented"
  end

  def install_cpbo
    raise "not implemented"
  end

  def initialize config
    @buildenv = ENV['buildenv'].lowercase rescue "development"
    @config = config
    @steamcmd_url = if RUBY_PLATFORM=~/linux/
      "http://media.steampowered.com/installer/steamcmd_linux.tar.gz"
    elsif RUBY_PLATFORM=~/mingw/
      "http://media.steampowered.com/installer/steamcmd.zip"
    end
    @steamcmd_file = File.join("buildenv", File.basename(@steamcmd_url))
  end
  def config
    @config
  end
end; end; end; end

task :buildenv do
  config = YAML.load_file(File.join('config','development.yml'))
  unless config['steamid']
    $stderr.puts "Please set your steamid in config/development.yml.".colorize(:red)
    exit 1
  end

  FileUtils.mkdir_p('buildenv')

  if RUBY_PLATFORM=~/linux/
    require './tasks/buildenv/linux.rb'
    installer = Rarma::Rake::Task::Buildenv::Linux.new config
  elsif RUBY_PLATFORM=~/mingw/
    require './tasks/buildenv/windows.rb'
    installer = Rarma::Rake::Task::Buildenv::Windows.new config
  else
    $stderr.puts "Unsupported platform #{RUBY_PLATFORM}"
    exit 1
  end

  installer.install_steam
  installer.install_arma
  installer.install_cpbo

  puts "\nRarma development buildenv successfully installed."
end
