import requests
import json
import sys
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from Helpers.validationfilters import validate_json, validate_schema
from Modules.authentication import requires_auth

class Datacapture(Resource):
	@validate_json
	@validate_schema('datacapture-schema')
	@requires_auth
	def post(self):
		req_json = request.get_json()
		try:
			payload = {'physicalConn': req_json['dataSourceID']}
			print(payload)
			r = requests.get("http://127.0.0.1:5000/things/",payload)
			thingId = int(r.json()[0]['thingId'])
			for measure in req_json['measuredDataList']:
				payload={
					"thingId": thingId,
					"timeStampMeasured": measure['timeStampTicks'],
					"tag": measure['tag'],
					"groupID": measure['groupID'],
					"value": measure['value']
				}
				url = 'http://127.0.0.1:5000/measurementevent/'
				headers = {'content-type': 'application/json'}
				requests.post(url, data=json.dumps(payload), headers=headers)
			return req_json,201
		except :
			print(sys.exc_info())
			e = sys.exc_info()[0]
			return str(e), 400
		

