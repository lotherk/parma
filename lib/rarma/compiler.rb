require 'ruby_parser'
require 'securerandom'
require 'rarma/compiler/assembly'
require 'rarma/compiler/processor'
require 'rarma/util/tidy'

RARMA_COMPILER_KEYWORDS=[:require]

module Rarma::Compiler
  def self.opts
    @opts
  end
  def self.compile file, opts={}
    @opts = opts
    # parse code
    Assembly.load_file file
    Assembly.build
    Assembly.debug_dump
  end

  def self.load_file file
    Rarma.logger.debug "Loading #{file}"
    opts[:include].each do |path|
      Rarma.logger.debug "  searching #{path}"
      filename = File.join(path, '/', "#{file}.rb")
      Rarma.logger.debug "     checking #{filename}"
      if File.exist? filename
        Assembly.load_file filename
        return true
      end
    end
    raise RuntimeError, "could not find file #{file} in include path"
  end


end
require 'rarma/compiler/scope.rb'
