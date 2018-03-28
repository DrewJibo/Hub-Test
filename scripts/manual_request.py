import os, sys
import requests
import base64, datetime, hashlib, hmac
from TestUtils.utils import *


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
	Sends a manually signed request using the AccessKeyId and SecretKey
	to the AWS service.
"""
def send_request(access_key, secret_key):
	cred_path = check_credentials()

	# Get credentials for AWS token
	credentials = load_json(dst_path)
	access_key = credentials['accessKeyId']
	secret_key = credentials['secretAccessKey']

	if access_key is None or secret_key is None:
		print("\nNo access key is available.\n")
		sys.exit()

	##########################
	#    AWS REQUEST INFO    #
	##########################

	config_path = check_aws_config()

	aws_data = load_json(config_path)
	method = aws_data['method']
	service = aws_data['service']
	host = aws_data['host']
	aws_region = aws_data['region']
	aws_endpoint = aws_data['endpoint']
	request_parameters = ''

	# Create a date for headers and the credential string
	time = datetime.datetime.utcnow()
	amz_date = time.strftime('%Y%m%d%dT%H%M%SZ')	# date with time
	date_stamp = time.strftime('%Y%m%d')			# date w/o time, used in credential scope

	##################################
	#    CREATE CANONICAL REQUEST    #
	##################################

	uri = '/'																# create canonical URI (from domain to query), use '/' if no path
	query = request_parameters												# must be sorted by name
	canonical_headers = 'host:{}\nx-amz-date:{}\n'.format(host, amz_date)	# must be trimmed, lowercase, sorted in code point (low to high)
	signed_headers = 'host;x-amz-date'										# lists headers in canonical_headers list, delimited with ; in alpha order
	payload_hash = hashlib.sha256('').hexdigest()							# hash of the request body content, GET payload is empty string

	# Combine elements to make request
	canonical_request = '{}\n{}\n{}\n{}\n{}\n{}'.format(method, uri, query, canonical_headers, signed_headers, payload_hash)

	###################################
	#    CREATE THE STRING TO SIGN    #
	###################################

	algorithm = 'AWS4-HMAC-SHA256'
	credential_scope = '{}/{}/{}/aws4_request'.format(date_stamp, aws_region, service)
	hashed_req = hashlib.sha256(canonical_request).hexdigest()

	# Combine elements to make string
	string_to_sign = '{}\n{}\n{}\n{}'.format(algorithm, amz_date, credential_scope, hashed_req)

	#############################
	#    CALCULATE SIGNATURE    #
	#############################

	signing_key = get_signature_key(secret_key, date_stamp, aws_region, service)
	encoded_string = string_to_sign.encode('utf-8')

	# create the signature
	signature = hmac.new(signing_key, encoded_string, hashlib.sha256).hexdigest()

	##########################
	#    ADD SIGNING INFO    #
	##########################

	authorization_header = '{} Credential={}/{}, SignedHeaders={}, Signature={}'.format(algorithm, access_key, credential_scope, signed_headers, signature)
	headers = {'x-amz-date':amz_date, 'Authorization':authorization_header}

	######################
	#    SEND REQUEST    #
	######################

	request_url = '{}?{}'.format(aws_endpoint, query)

	print('\n****** BEGIN REQUEST ******')
	print('Request URL = ' + request_url)
	response = requests.get(request_url, headers=headers)

	print('\n****** RESPONSE ******')
	print('Response code: %d\n' % response.status_code)
	print(response.text)


if __name__ == "__main__":
	send_request()