# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'rarma/version'

Gem::Specification.new do |spec|
  spec.name          = "rarma"
  spec.version       = Rarma::VERSION
  spec.authors       = ["Konrad Lother"]
  spec.email         = ["konrad@corpex.de"]
  spec.summary       = %q{ArmA Ruby Framework}
  spec.description   = %q{ArmA Ruby Framework}
  spec.homepage      = "https://github.com/lotherk/rarma"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 2.7"

  spec.files         = `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }
#  spec.bindir        = "exe"
  spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
  spec.require_paths = ["lib"]

  spec.add_development_dependency "bundler", "~> 2.0"
  spec.add_development_dependency "rake", "~> 13.0"
  spec.add_development_dependency "rspec", "~> 3.12"
  spec.add_development_dependency "rubocop", "~> 1.57"
  spec.add_dependency "sexp_processor", "~> 4.16"
  spec.add_dependency "ruby_parser", "~> 3.20"
  spec.add_dependency "colorize", "~> 0.8"
end
