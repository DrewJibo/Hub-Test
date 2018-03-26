import os
import sys
import json
import paramiko


"""
	Copies the credentials.json file locally from robot
"""
def get_credentials(hostname, username, password, src_path, dst_path):

	# create ssh connection
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=hostname, username=username, password=password)

	# ftp file from robot to local path
	ftp_client = ssh_client.open_sftp()
	ftp_client.get(src_path, dst_path)
	ftp_client.close()


"""
	Reads and returns contents of JSON file
"""
def load_json(path):
	with open(path, 'r') as file:
		data = json.load(file)
	return data


"""
	Creates AWS session token
"""
def create_token():

	# get login info for SSH to robot
	login_file = os.path.expanduser('~/jibo/Hub-Test/config/login.json')
	login_data = load_json(login_file)
	username = login_data['username']
	password = login_data['password']
	robot_name = login_data['robot_name']

	# generate credentials.json
	src_path = '/var/jibo/credentials.json'
	dst_path = os.path.expanduser('~/jibo/Hub-Test/config/credentials.json')
	get_credentials(robot_name, username, password, src_path, dst_path)

	# Get credentials for AWS token
	json_data = load_json(dst_path)
	region = json_data['region']
	endpoint = 'https://{}.jibo.com'.format(region)
	accessKeyId = json_data['accessKeyId']
	secretAccessKey = json_data['secretAccessKey']


if __name__ == "__main__":
	create_token()