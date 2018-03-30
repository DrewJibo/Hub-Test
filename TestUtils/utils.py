import os, sys
import json
import paramiko

"""
	Copies the credentials.json file locally from robot
"""
def copy_credentials_file(hostname, username, password, src_path, dst_path):
	# create ssh connection
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=hostname, username=username, password=password)

	# ftp file from robot to local path
	ftp_client = ssh_client.open_sftp()
	ftp_client.get(src_path, dst_path)
	ftp_client.close()


"""
	Creates a default config file for AWS
	(aws_config.json)
"""
def create_default_config(path):
	data = {}
	data['method'] = 'GET'
	data['service'] = 'ec2'
	data['host'] = 'devgreen-hub.jibo.com'
	data['region'] = 'stg-entrypoint'
	data['endpoint'] = 'http://ec2.devgreen-hub.com'

	with open(path, 'w+') as file:
		json.dump(data, file)


"""
	Checks for the aws_config.json file,
	creates the file and populates with default values
	if not found.
"""
def check_aws_config():
	config_path = os.path.expanduser('~/jibo/HubTest/config/aws_config.json')

	if not os.path.exists(config_path):
		print("\nCreating default AWS config...")
		create_default_config(config_path)
		print("Done.\n")

	return config_path


"""
	Checks for the credentials.json file,
	creates the file and populates with values from
	robot if not found.
"""
def check_credentials():
	login_file = os.path.expanduser('~/jibo/HubTest/config/login.json')
	login_data = load_json(login_file)

	robot_name = login_data['robot_name']
	username = login_data['username']
	password = login_data['password']
	
	src_path = '/var/jibo/credentials.json'
	dst_path = os.path.expanduser('~/jibo/HubTest/config/credentials.json')

	if not os.path.exists(dst_path):
		print("\nGrabbing AWS credentials from robot...")
		copy_credentials_file(robot_name, username, password, src_path, dst_path)
		print("Done.\n")

	return dst_path


"""
	Reads and returns contents of JSON file
"""
def load_json(path):
	with open(path, 'r') as file:
		data = json.load(file)
	return data