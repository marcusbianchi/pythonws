import boto3
import json
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from Helpers.validationfilters import validate_json, validate_schema
from Helpers.decimalencoder import DecimalEncoder
from Modules.authentication import requires_auth

class User(Resource):
	@requires_auth
	def get(self, userid):
		dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
		table = dynamodb.Table('users')
		response = table.get_item(Key={'userId': userid})
		item = json.dumps(response['Item'], cls=DecimalEncoder)
		return json.loads(item)
	
	@validate_json
	@validate_schema('user-schema')
	@requires_auth
	def put(self, userid):
		dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
		table = dynamodb.Table('users')
		response = table.get_item(Key={'userId': userid})
		if 'Item' in response:
			table.delete_item(Key={'userId': userid})
			req_json = request.get_json()
			req_json['userId'] = userid
			result = table.put_item(
				Item=req_json
			)
			return req_json,201
		else:
			return "Item not found",404
	
	@validate_json
	@validate_schema('user-schema')
	@requires_auth
	def delete(self, userid):
		dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
		table = dynamodb.Table('users')
		response = table.get_item(Key={'userId':userid})
		if 'Item' in response:
			table.delete_item(Key={'userId': userid})			
			return '',204
		else:
			return "Item not found",404
