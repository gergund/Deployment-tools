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
	if not exists(var_path, use_sudo=True):
		sudo('mkdir -p ' + var_path)
	if not exists(env_path, use_sudo=True):
                sudo('mkdir -p ' + env_path)

def deploy():
	timestamp = run('date +%s')
	versions_path = base_path + 'versions/' + timestamp + '/'
	release_path = base_path  + 'releases/' + git_tag + '/'
	current_path =  base_path + 'current'
	sudo('mkdir -p ' + versions_path)
	sudo('cp -r ' + release_path + '/* ' + versions_path)
	with cd(base_path):
		sudo('rm -Rf ' + current_path)
		sudo('ln -s ' + versions_path + ' ' + current_path)

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