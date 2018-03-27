import os
import sys


"""
	Clones and builds the pegasus repo if needed
"""
def setup_pegasus(branch):
	# build paths
	path_jiboV2 = os.path.expanduser('~/jibo/jiboV2')
	path_pegasus = os.path.expanduser(path_jiboV2 + '/pegasus')

	# commands
	clone = 'git clone https://github.com/jiboV2/pegasus.git'
	checkout = 'git checkout ' + branch
	pull = 'git pull origin ' + branch 
	docker = './scripts/docker-init.sh'

	# check if user already has pegasus
	if not os.path.isdir(path_pegasus):
		print("Setting up pegasus directories...")
		os.makedirs(path_jiboV2)
		os.chdir(path_jiboV2)
		os.system(clone)
	else:
		print("Pegasus found!")

	# build pegasus
	os.chdir(path_pegasus)
	os.system(checkout)
	os.system(pull)
	os.system(docker)


"""
	Clones and builds the SDK/monorepo if needed
"""
def setup_sdk(branch):
	# build paths
	path_sdk = os.path.expanduser('~/jibo/sdk')
	path_cli = os.path.expanduser(path_sdk + '/sdk/packages/jibo-cli')

	# commands
	clone = 'git clone git@github.jibo.com:sdk/sdk.git'
	checkout = 'git checkout ' + branch
	pull = 'git pull origin ' + branch
	bootstrap = 'yarn bootstrap'
	build = 'yarn run build:skills'
	unlink = 'yarn unlink'
	link = 'yarn link'

	if not os.path.isdir(path_sdk):
		print("Setting up sdk directories...")
		os.makedirs(path_sdk)
		os.chdir(path_sdk)
		os.system(clone)
	else:
		print("SDK found!")

	# build monorepo
	os.chdir(path_sdk + '/sdk')
	os.system(checkout)
	os.system(pull)
	os.system(bootstrap)
	os.system(build)
	os.chdir(path_cli)
	os.system(unlink)
	os.system(link)


def main():
	pegasus_branch = input("Enter branch for Pegasus repo: ") or 'master'
	sdk_branch = input("Enter branch for SDK monorepo: ") or 'pegasus'

	setup_pegasus(pegasus_branch)
	setup_sdk(sdk_branch)

if __name__ == "__main__":
	main()