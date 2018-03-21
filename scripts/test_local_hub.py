import os
import sys
import json
import jsc #convert from js


def get_creds(file):
	


def create_token(credential_path):
	# read credentials from file
	with open(credential_path, 'r') as file:
		json_data = json.load(file)

	region = json_data['region']
	endpoint = 'https://{}.jibo.com'.format(region)
	creds = get_creds(credential_path)

	account = {
				'credentials': creds,
				'region': region,
				'endpoint': endpoint
			}

	token = jsc.Account(account).createAccessToken()



if __name__ == "__main__":
	create_token()