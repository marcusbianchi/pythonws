# coding: utf-8

import threading
from MachineLearningModule import machine_learn
from flask import Flask,request

class machineLearnThread (threading.Thread):
	def __init__(self,loss,n_estimators,max_depth,max_features,
		learning_rate,min_samples_split,min_samples_leaf,subsample):
		self.loss = loss
		self.n_estimators=n_estimators
		self.max_depth = max_depth
		self.max_features =  max_features
		self.learning_rate = learning_rate
		self.min_samples_split = min_samples_split
		self.min_samples_leaf = min_samples_leaf
		self.subsample=subsample
		threading.Thread.__init__(self)
	def run(self):
		machine_learn.learn(self.loss,self.n_estimators,self.max_depth,self.max_features,
			self.learning_rate,self.min_samples_split,self.min_samples_leaf,self.subsample)

app = Flask(__name__)


@app.route("/machinelearn",methods=["GET"])
def machinelearn():
	loss = 'ls'
	n_estimators=200
	max_depth = 8
	max_features =  'sqrt' 
	learning_rate = 0.05
	min_samples_split = 500
	min_samples_leaf = 50
	subsample=0.8
	thread1 = machineLearnThread(loss,n_estimators,max_depth,max_features,
    	learning_rate,min_samples_split,min_samples_leaf,subsample)
	thread1.start()
	return 'Learning!!'



@app.route("/predict",methods=["PUT"])
def predict():
	if request.is_json:
		predict_params = request.json
		print(len(predict_params['current_positions']))
		if(len(predict_params['current_positions'])==56):
			recomended_position = machine_learn.find_position(predict_params['current_positions'],predict_params['item_type'],10);
			return str(recomended_position),200
		else:
			return 'The Size of the Recomended Positions must be 56',400
	else:
		return 'The Body MUST BE A JSON',400
	

app.run(debug=True, use_reloader=True)