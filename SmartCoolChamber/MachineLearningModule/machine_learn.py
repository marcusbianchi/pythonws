# coding: utf-8

import pandas as pd
import numpy as np 
import pylab as P
import shelve
from sklearn.model_selection import train_test_split
from datetime import datetime
from sklearn.ensemble  import GradientBoostingRegressor
import shelve

def learn(loss,n_estimators,max_depth,max_features,learning_rate,min_samples_split,min_samples_leaf,subsample):
	#-----------------------------load Data----------------------------------------------
	df = pd.read_csv('./data/data.csv',header=0)
	data = df.values
	gb = []
	gb_train_score=[]
	gb_test_score=[]
	splited_data_values_array =[]
	loss = loss
	n_estimators=n_estimators
	max_depth = max_depth
	max_features =  max_features 
	learning_rate = learning_rate
	min_samples_split = min_samples_split
	min_samples_leaf = min_samples_leaf
	subsample=subsample

	for i in range(4):
		#-----------------------------Split Value---------------------------------------------- 
		temps = data[0:,58:].copy()
		temps = np.delete(temps,i,1)
		
		concact_data = np.concatenate((data[0:,1:58],temps), 1)
		print(concact_data.shape)
		print(concact_data)
		X_train,X_test,y_train,y_test = train_test_split(data[0:,1:58],data[0:,58+i].ravel())
		splited_data_values = {}		
		splited_data_values['X_train'] = X_train
		splited_data_values['X_test'] = X_test
		splited_data_values['y_train'] = y_train
		splited_data_values['y_test'] = y_test
		splited_data_values_array.append(splited_data_values)

		#-----------------------GradientBoostingRegressor------------------------------------
		gb.append(GradientBoostingRegressor(presort = True,loss=loss,n_estimators =n_estimators,
		max_depth=max_depth,max_features=max_features,min_samples_split=min_samples_split,
		learning_rate=learning_rate,min_samples_leaf=min_samples_leaf,subsample=subsample,verbose=True).fit(X_train,y_train))
		print(gb[i].score(X_train,y_train))
		print(gb[i].score(X_test,y_test))
		gb_train_score.append(gb[i].score(X_train,y_train))
		gb_test_score.append(gb[i].score(X_test,y_test))

	d = shelve.open('./longmemory/learning')
	if('gb' in d):
		gb_old = d['gb']
		for i in range(4):
			splited_data_values = splited_data_values_array[i]			
			gb_old_score = gb_old[i].score(splited_data_values['X_test'],splited_data_values['y_test'])			
			print(str(i)+' Old '+str(gb_old_score))
			print(str(i)+' New '+str(gb_test_score[i]))
			if(gb_test_score[i]>gb_old_score and gb_test_score[i]<=1):
				gb[i] = gb[i]
			else:
				gb[i] = gb_old[i]
				gb_test_score[i] = gb_old_score
	d['gb'] = gb
	d.close()
	return gb_test_score

def predict(current_positions,position,item_type,opentime):
	current_positions[position] = item_type
	time = np.arange(0,opentime,0.5)
	pos_measurements = np.tile(current_positions,(len(time),1))
	time= time.reshape((len(time), 1))
	X = np.concatenate((pos_measurements,time), 1)
	d = shelve.open('./longmemory/learning')
	scores = []
	for gb in d['gb']:
		sum = np.sum(gb.predict(X))
		scores.append(sum)
	d.close()	
	return np.sum(scores)

def find_position(current_positions,item_type,opentime):
	available_options = [i for x,i in zip(current_positions,range(len(current_positions))) if x==0]
	scores = list(map(lambda x:predict(current_positions,x,item_type,opentime), available_options))
	result = dict(zip(available_options,scores))
	print(result)
	return max(result, key=result.get)
# loss = 'ls'
# n_estimators=200
# max_depth = 10
# max_features =  'sqrt' 
# learning_rate = 0.05
# min_samples_split = 500
# min_samples_leaf = 50
# subsample=0.8
# learn(loss,n_estimators,max_depth,max_features,learning_rate,min_samples_split,min_samples_leaf,subsample)

