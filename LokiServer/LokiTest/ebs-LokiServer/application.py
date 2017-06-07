import json
import os
from flask import Flask,current_app
from flask_restful import  Api
from Modules.datacapture import Datacapture
from Modules.thinglist import ThingList
from Modules.thing import Thing
from Modules.userlist import UserList
from Modules.user import User
from Modules.measurementeventlist import MeasurementEventList


application  = Flask(__name__)
api = Api(application)

with application .app_context():
	path = './Schemas'
	files = os.listdir(path);
	for file in files:
		f = open(path+'//'+file,'r')
		filecontent = f.read()
		f.close()
		fullfilename = os.path.splitext(path+'\\'+file)[0]
		filename = os.path.basename(fullfilename)
		current_app.config[filename] = json.loads(filecontent)

api.add_resource(Datacapture, '/datacapture/')
api.add_resource(ThingList, '/things/')
api.add_resource(Thing, '/things/<thingid>')
api.add_resource(UserList, '/users/')
api.add_resource(User, '/users/<userid>')
api.add_resource(MeasurementEventList, '/measurementevent/')

if __name__ == '__main__':
	application .run(debug=True,threaded=True)