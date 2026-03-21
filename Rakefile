require "bundler/gem_tasks"
require "rarma"
if ENV['DEBUG']
  Rarma.logger.level = Logger::DEBUG
end
require "rarma/rake"
require "rubocop/rake_task"

RuboCop::RakeTask.new

require "./tasks/buildenv.rb"
require "./tasks/server.rb"
