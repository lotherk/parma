class Rarma::Rake::Task::Buildenv::Linux
  include Rarma::Rake::Task::Buildenv

  def install_steam
    unless File.directory? config['steamdir']
      super
      puts "Extracting steamCMD to #{config['steamdir']}".colorize(:bold)
      FileUtils.mkdir_p(config['steamdir'])
      Rake.sh "tar xzf #{@steamcmd_file} -C #{config['steamdir']}"
    else
      puts "#{config['steamdir']} already exists, remove if you want to reinstall.".colorize(:yellow)
      puts ""
    end
  end

  def install_arma
    puts "Installing/Updating arma3 to #{config['armadir']}".colorize(:bold)
    Rake.sh "./#{config['steamdir']}/steamcmd.sh +login #{config['steamid']} +force_install_dir #{config['armadir']} +app_update 233780 +exit"
    puts ""
  end

  def install_cpbo
    unless File.exist? config['cpbodir']
      puts "Cloning https://github.com/iAnomaly/cpbo to #{config['cpbodir']}"
      Rake.sh "git clone https://github.com/iAnomaly/cpbo #{config['cpbodir']}"
      puts "Compiling cpbo"
      Rake.sh "cd #{config['cpbodir']}; make"
    else
      puts "#{config['cpbodir'] } already exists, remove if you want to to reinstall".colorize(:yellow)
    end
    puts ""
  end

end
