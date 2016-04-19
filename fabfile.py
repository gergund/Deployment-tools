from fabric.api import *
from fabric.contrib.files import *

env.hosts = [
    'web01',
]

# Set the username
env.user   = "jenkins"

#VARIABLES#
repo = 'git@github.corp.magento.com:magento2/magento2ce.git'
base_path = '/var/www/deploy/'
#env.sudo_user = 'jenkins'
git_tag = '2.0.4'
###########

def uptime():
	"""	Shows server uptime """
	run("uptime")

def init_shared():
	shared_path = base_path + 'shared/'
	media_path = base_path + 'shared/'  +'media/'
	var_path = base_path + 'shared/' + 'var/'
	env_path = base_path + 'shared/' + 'env/'
	if not exists(shared_path, use_sudo=True):
		sudo('mkdir -p ' + shared_path)
	if not exists(media_path, use_sudo=True):
		sudo('mkdir -p ' + media_path)
		sudo('chmod 770 ' + media_path)
		sudo('chown apache:apache ' + media_path)
	if not exists(var_path, use_sudo=True):
		sudo('mkdir -p ' + var_path)
		sudo('chmod 770 ' + var_path)
                sudo('chown apache:apache ' + var_path)
	if not exists(env_path, use_sudo=True):
                sudo('mkdir -p ' + env_path)
		sudo('chmod 770 ' + env_path)
                sudo('chown apache:apache ' + env_path)

def deploy():
	timestamp = run('date +%s')
	versions_path = base_path + 'versions/' + timestamp + '/'
	release_path = base_path  + 'releases/' + git_tag + '/'
	current_path =  base_path + 'current'
	sudo('mkdir -p ' + versions_path)
	sudo('cp -r ' + release_path + '/* ' + versions_path)
	with cd(versions_path):
		sudo('rm -Rf ' + versions_path + 'media')
		sudo('ln -s ../../shared/media')
		sudo('rm -Rf ' + versions_path + 'var')
		sudo('ln -s ../../shared/var')
		sudo('cd app/etc/ && ln -s ../../../shared/env/env.php')
	with cd(base_path):
		sudo('rm -Rf ' + current_path)
		sudo('ln -s ' + versions_path + ' ' + current_path)
	sudo('service php-fpm reload')
        sudo('service nginx reload')

def update(path):
	with cd(path):
		sudo('git checkout tags/' + git_tag + ' -b ' + git_tag, warn_only=True)
		sudo('git branch -a | grep ' + git_tag, warn_only=True)
		sudo('git status | grep nothing', warn_only=True)
	deploy()

def install():
	init_shared()
	path = base_path  + 'releases/' + git_tag + '/'
	if exists(path, use_sudo=True):
		update(path)
	else:
		sudo('mkdir -p ' + path)
		with cd(path):
			sudo('git clone ' + repo + ' .')
			update(path)

def rollback(version):
	current_path =  base_path + 'current'
	if (version == 'latest'):
		latest = sudo('cd ' +  base_path + 'versions/ && ls -la | tail -fn 2 | head -1 | awk \'{print $9}\' ')
		back_path = base_path + 'versions/' + latest
	else:
		back_path = base_path + 'versions/' + version
	if exists(back_path, use_sudo=True):
		sudo('rm -Rf ' + current_path)
		sudo('ln -s ' + back_path + ' ' + current_path)

def clean(amount):
	versions_path = base_path + 'versions/'
	amount = int(amount)
	versions_amount = int(sudo('cd ' + versions_path + ' && ls -l | wc -l'))
	count = int(versions_amount) - int(amount)
	if ( count > 1 ):
		for i in range(1, count):
			if ( (versions_amount - amount) > 1 ):
				to_rm = sudo('cd ' + versions_path + ' && ls -la | head -4 | tail -fn 1 | awk \'{print $9}\' ')
				sudo('rm -Rf ' + versions_path + '/' + to_rm)
