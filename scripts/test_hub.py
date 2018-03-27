import paramiko
import json
import requests
import os, sys
import base64, datetime, hashlib, hmac


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
	Reads and returns contents of JSON file
"""
def load_json(path):
	with open(path, 'r') as file:
		data = json.load(file)
	return data


"""
"""
def sign(key, msg):
	return hmac.new(key, msg.encode('utf-8'), hashlib.sha256.digest())


"""
"""
def get_signature_key(key, date_stamp, region_name, service_name):
	k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
	k_region = sign(k_date, region_name)
	k_service = sign(k_region, service_name)
	k_signing = sign(k_service, 'aws4_request')
	return k_signing


"""
	Combines the AWS elements to build a cononical request
"""
def build_req(elements):
	req = ''
	for elem in elements:
		req += '{}\n'.format(elem)

	return req


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

	if not os.path.exists(dst_path):
		print("\nGrabbing AWS credentials from robot...")
		copy_credentials_file(robot_name, username, password, src_path, dst_path)
		print("Done.\n")

	# Get credentials for AWS token
	json_data = load_json(dst_path)
	region = json_data['region']
	endpoint = 'https://{}.jibo.com'.format(region)
	access_key = json_data['accessKeyId']
	secret_key = json_data['secretAccessKey']

	method = 'GET'
	service = 'ec2'
	host = 'ec2.amazonaws.com'
	region = 'us-east-1'
	aws_endpoint = 'https://ec2.amazonaws.com'
	request_parameters = ''

	if access_key is None or secret_key is None:
		print("\nNo access key is available.\n")
		sys.exit()

	# Create a date for headers and the credential string
	time = datetime.datetime.utcnow()
	amz_date = time.strftime('%Y%m%d%dT%H%M%SZ')	# date with time
	date_stamp = time.strftime('%Y%m%d')			# date w/o time, used in credential scope

	aws_elements = list()
	canonical_uri = '/'														# create canonical URI (from domain to query), use '/' if no path
	canonical_query = request_parameters									# must be sorted by name
	canonical_headers = 'host:{}\nx-amz-date:{}\n'.format(host, amz_date)	# must be trimmed, lowercase, sorted in code point (low to high)
	signed_headers = 'host;x-amz-date'										# lists headers in canonical_headers list, delimited with ; in alpha order
	payload_hash = hashlib.sha256('').hexdigest()							# hash of the request body content, GET payload is empty string

	canonical_request = build_req(aws_elements)								# combine elements to make cononical request

if __name__ == "__main__":
	create_token()