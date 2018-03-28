import os, sys
import boto3
from TestUtils.utils import *

"""
"""
def boto_request(access_key, secret_key):
		
	config_path = check_aws_config()
	aws_data = load_json(config_path)
	region = aws_data['region']

	s3 = boto3.resource('s3')
	for bucket in s3.buckets.all():
		print(bucket.name)


"""
	Makes a request using the AWS SDK (boto3).
	This does not require a signature, it is automatically signed.
"""
def send_request():
	cred_path = check_credentials()

	# Get credentials for AWS token
	credentials = load_json(dst_path)
	access_key = credentials['accessKeyId']
	secret_key = credentials['secretAccessKey']

	if access_key is None or secret_key is None:
		print("\nNo access key is available.\n")
		sys.exit()

	boto_request(access_key, secret_key)


if __name__ == "__main__":
	send_request()