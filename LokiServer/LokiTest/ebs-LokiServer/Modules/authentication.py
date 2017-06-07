import boto3
import json
from flask import request, Response
from Helpers.decimalencoder import DecimalEncoder
from boto3.dynamodb.conditions import Key, Attr
from functools import wraps
import logging

logging.basicConfig(filename='/opt/python/log/auth.log', level=logging.DEBUG)


def check_auth(username, password):
	dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
	table = dynamodb.Table('users')
	response = table.get_item(Key={'userId': username})
	logging.debug("username "+username)
	logging.debug("password "+ password)
	if 'Item' in response:
		item = json.dumps(response['Item'], cls=DecimalEncoder)
		userJson = json.loads(item)
		return userJson['password'] == password
	else:
		return False;


def authenticate():
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		logging.debug("auth "+ str(auth))
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated