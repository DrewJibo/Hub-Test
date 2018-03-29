import os, sys
import boto3

sys.path.append('./')
from TestUtils.utils import *


"""
	Create connection to AWS/ec2 services
"""
def connect():
	# Get credentials for AWS
	cred_path = check_credentials()
	credentials = load_json(cred_path)
	access_key = credentials['accessKeyId']
	secret_key = credentials['secretAccessKey']
	region = credentials['region']

	if access_key is None or secret_key is None:
		print("\nNo access key is available.\n")
		sys.exit()

	# connect to aws
	conn = boto3.resource('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
	return conn


"""
	Makes a request using the AWS SDK (boto3).
	This does not require a signature, it is automatically signed.
"""
def send_request():
	conn = connect()
	

if __name__ == "__main__":
	send_request()