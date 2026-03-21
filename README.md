# Rarma

Rarma is a crossplatform framework for [Bohemia Interactive](https://www.bistudio.com/)'s [Armed Assault](http://arma3.com/) version 3 written in ruby.

It offers a [transcompiler](http://en.wikipedia.org/wiki/Source-to-source_compiler) for source-to-source conversion from ruby to [SQF](https://community.bistudio.com/wiki/ArmA:_Introduction_to_Scripting) code, thus support for object oriented scripting and many more.

Its main purpose is to create an developer friendly environment, that blah blah blah.

## Supported Systems

Tested:
  - Windows 8.1 (With [RubyInstaller for Windows](http://rubyinstaller.org/) and [Git for Windows](https://msysgit.github.io/))
  - Linux

## Installation



## Development Environment

Rarma provides you an easy method to setup all the tools you need to develope ArmA code in a comfortable way. It will install steamCMD, ArmA 3 Dedicated Server files and CPBO.

### Requirements

#### Windows

You need to install [RubyInstaller for Windows](http://rubyinstaller.org/) and [Git for Windows](https://msysgit.github.io/). We'll use the ```Git Bash``` as our command line.

#### Linux

You need to install the following libraries to make steamCMD and cpbo work.

##### Debian/Ubuntu

```
sudo apt-get install lib32gcc1 libboost-all-dev
```

##### Other Distributions

Check yourself. (TODO)

### Create the environment

Before you can create the environment, you have to create a ```development.yml``` inside the ```config``` directory. For this you can simply copy the existing [development.yml.example](config/development.yml.example). You then have to set your steamid in ```development.yml``` as we're using steam to install the ArmA 3 Dedicated Server files.

After editing ```development.yml```, run

```
$ rake environment
```

and let the magic happen.

You should see a message telling you that "*Rarma development environment successfully installed.*", hopefully.

## Usage

TODO: Write usage instructions here

## Development

After checking out the repo, run `bin/setup` to install dependencies. Then, run `bin/console` for an interactive prompt that will allow you to experiment.

To install this gem onto your local machine, run `bundle exec rake install`. To release a new version, update the version number in `version.rb`, and then run `bundle exec rake release` to create a git tag for the version, push git commits and tags, and push the `.gem` file to [rubygems.org](https://rubygems.org).

## Contributing

1. Fork it ( https://github.com/[my-github-username]/rarma/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
