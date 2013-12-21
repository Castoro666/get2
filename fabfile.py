from fabric.api import *
from fabric.contrib.files import *
from fabric.colors import *
import fabtools

env.shell = "/bin/bash -c -l"
env.hosts = ['django@luccalug.it',]

def runserver():
	with prefix("source ~/.bashrc"):
		with prefix("workon venv-get"):
			local("python manage.py runserver")

def deploy(name):
	if exists("~/%s" % name):
		print(red("Error: Directory gia esistente!"))
	else:
		run("mkdir ~/%s" % name)
		with cd("~/%s" % name):
			fabtools.require.git.working_copy("https://github.com/luk156/get2.git")
			password = create_database(name)
			with cd("get2"):
				configure(name,password)
			with fabtools.python.virtualenv('../stable-env'):
				run("python get2/manage.py collectstatic")
				run("python get2/manage.py syncdb")
				run("python get2/manage.py migrate")
		fabtools.require.service.restarted('apache2')


def configure(name, password):
	run ("cp get2/settings.py.sample get2/settings.py")
	sed("get2/settings.py", "_database_", name)
	sed("get2/settings.py", "_user_", name)
	sed("get2/settings.py", "_titolo_", name)
	sed("get2/settings.py", "_password_", password)

def create_database(name):
	with settings(mysql_user='root', mysql_password='Franchini03'):
		password = prompt('Inserisci la password del nuovo database: ')
		fabtools.require.mysql.user(name, password)
		fabtools.require.mysql.database(name, owner=name)
		return password

def update(name):
	with cd("~/%s/" % name):
		fabtools.require.git.working_copy("https://github.com/luk156/get2.git")
		with fabtools.python.virtualenv('../stable-env'):
			run("python get2/manage.py collectstatic")
	fabtools.require.service.restarted('apache2')