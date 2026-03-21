class Rarma::Rake::Task::Buildenv::Windows
  include Rarma::Rake::Task::Buildenv

  def install_steam
    super
    unless File.exist?config['steamdir']
      FileUtils.mkdir_p(config['steamdir'])
      Rake.sh "unzip #{@steamcmd_file} -d #{config['steamdir']}"
    else
      puts "#{config['steamdir']} alrealdy exists, remove to reinstall".colorize(:yellow)
    end
  end

  def install_arma
    puts "Installing/Updating arma3 in #{config['armadir']}"
    FileUtils.mkdir_p(config['armadir'])
    Rake.sh "#{config['steamdir']}/steamcmd.exe +login #{config['steamid']} +force_install_dir #{config['armadir'].gsub('/', '\\')} +app_update 233780 +exit"
  end

  def install_cpbo
  end

end
