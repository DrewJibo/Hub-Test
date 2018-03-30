import os, sys
import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

sys.path.append('./')
from TestUtils.utils import *


"""
	Tries to make a signed request to Elastic Search
"""
def es_request():
	cred_path = check_credentials()
	cred_json = load_json(cred_path)
	ACCESS_KEY = cred_json['accessKeyId']
	SECRET_KEY = cred_json['secretAccessKey']
	REGION = 'us-east-1'
	SERVICE = 'es'
	DOMAIN = 'stg-entrypoint'

	if ACCESS_KEY is None or SECRET_KEY is None:
		print("\nCredentials are invalid.\n")
		sys.exit()

	session = boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
	credentials = session.get_credentials()

	es_host = '{}.{}.{}.amazonaws.com'.format(DOMAIN, REGION, SERVICE)
	aws_auth = AWSRequestsAuth(
		aws_access_key=credentials.access_key,
		aws_secret_access_key=credentials.secret_key,
		aws_token=credentials.token,
		aws_host=es_host,
		aws_region=session.region_name,
		aws_service=SERVICE
	)

	# use the requests connection_class and pass in the custom auth class
	es = Elasticsearch(
		hosts=[{'host': es_host, 'port': 443}],
		http_auth=aws_auth,
		use_ssl=True,
		verify_certs=True,
		connection_class=RequestsHttpConnection
	)

	print(es.info())


def main():
	es_request()


if __name__ == "__main__":
	main()