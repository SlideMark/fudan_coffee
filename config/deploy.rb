# config valid only for Capistrano 3.1
lock '>=3.2.1'

set :application, 'fudan_coffee'
set :repo_url, 'git@github.com:SlideMark/fudan_coffee.git'
ask :branch, proc { `git rev-parse --abbrev-ref HEAD`.chomp }
set :deploy_to, '/home/fudan_coffee/deploy'
set :ssh_options, {
  keys: %w(~/.ssh/id_rsa),
  forward_agent: false,
}

USAGE = '''
## 部署
cap [目标机器组] deploy
'''

namespace :deploy do

  task :start do
    on roles(:api) do |host|
       execute "source /home/fudan_coffee/env/bin/activate && supervisorctl start coffee"
    end
  end

  task :stop do
    on roles(:api) do |host|
       execute "source /home/fudan_coffee/env/bin/activate && supervisorctl stop coffee"
    end
  end

  task :restart do
    on roles(:api) do |host|
       execute "source /home/fudan_coffee/env/bin/activate && supervisorctl restart coffee"
    end
  end

  task :reread do
    on roles(:api) do |host|
      execute "source /home/fudan_coffee/env/bin/activate && supervisorctl reread"
    end
  end

  task :status do
    on roles(:api) do |host|
      execute "source /home/fudan_coffee/env/bin/activate && supervisorctl status"
    end
  end

  task :revision do
    on roles(:api) do |host|
       execute "cat #{current_path}/REVISION"
    end
  end

  task :migration do
    on roles(:db) do |host|
       execute "source /home/fudan_coffee/env/bin/activate && cd #{release_path} && python script/migration.py"
    end
  end

  task :install_package do
    on roles(:api, :hub, :worker) do |host|
      execute "source /home/fudan_coffee/env/bin/activate && && pip install -r doc/requirements.txt"
    end
  end

  after :publishing, :install_package
  after :publishing, :migration
  after :publishing, :restart

end
