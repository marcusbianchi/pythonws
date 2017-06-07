import boto3
import json
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from Helpers.validationfilters import validate_json, validate_schema
from Helpers.decimalencoder import DecimalEncoder
from boto3.dynamodb.conditions import Key, Attr
from Modules.authentication import requires_auth

class ThingList(Resource):
	@validate_json
	@validate_schema('thing-schema')
	@requires_auth
	def post(self):
		req_json = request.get_json()
		dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
		table = dynamodb.Table('things')
		result = table.put_item(
			Item=req_json
		)
		return  req_json,201
		
	@requires_auth
	def get(self):
		physicalConn = request.args.get('physicalConn')
		dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
		table = dynamodb.Table('things')
		if(physicalConn!=None):
			response = table.scan(FilterExpression=Attr('physicalConn').eq(physicalConn))
		else:
			response = table.scan(Limit=10)
		result =[]
		for i in response['Items']:
			item = json.dumps(i, cls=DecimalEncoder)
			result.append(json.loads(item))
		return result,200
