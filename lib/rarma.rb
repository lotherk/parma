require "logger"
require "colored"
require "rarma/version"
require "rarma/logger"

module Rarma

  def self.gem_root
    @gem_root ||= Gem::Specification.find_by_name("rarma").gem_dir
  end

  def self.logger(output=STDOUT)
    unless @logger
      @logger = Rarma::Logger.new(output)
      @logger.level = Logger::INFO
    end
    @logger
  end

  def self.root
    Gem::Specification.find_by_name("rarma").gem_dir
  end
end
