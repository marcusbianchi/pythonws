import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

df_init = pd.DataFrame();

positions = np.random.choice([0,1,2,3,4],size=56,p=[0.8,0.05,0.05,0.05,0.05])

positionnames = ['Position '+str(x) for x in range(56)]
max_lines = 100000
while(True):
	
	opentime = random.uniform(0, 30)
	time = np.arange(0,opentime,1.0)
	pos_measurements = np.tile(positions,(len(time),1))



	changedpos = random.randint(0,55)
	if(positions[changedpos]!=0):
		positions[changedpos] = np.random.choice([0,1,2,3,4],size=1,p=[0.8,0.05,0.05,0.05,0.05])
	else:
		positions[changedpos] = random.randint(1,5)

	df = pd.DataFrame(data = pos_measurements, columns = positionnames)

	df['timesincelastopen'] = time

	if(changedpos<=14):
		df['deltatemp1'] = random.uniform(1,2)*np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp2'] = random.uniform(0, 0.5) * np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp3'] = random.uniform(0,0.25)* np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp4'] = random.uniform(0, 0.1) * np.sin(time*0.1)*np.exp(-time+2)
	elif(changedpos>15 and changedpos<=29):
		df['deltatemp1'] = random.uniform(0, 1) * np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp2'] = random.uniform(1,2)*np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp3'] = random.uniform(0,0.5) * np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp4'] = random.uniform(0,0.2) * np.sin(time*0.1)*np.exp(-time+2)
	elif(changedpos>30 and changedpos<=44):
		df['deltatemp1'] = random.uniform(0,1) * np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp2'] = random.uniform(0, 0.5) *np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp3'] = random.uniform(1,2)*np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp4'] = random.uniform(0,0.2) * np.sin(time*0.1)*np.exp(-time+2)
	else:
		df['deltatemp1'] = random.uniform(0,0.2) * np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp2'] = random.uniform(0,0.5) *np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp3'] = random.uniform(0,1) * np.sin(time*0.1)*np.exp(-time+2)
		df['deltatemp4'] = random.uniform(1,2)* np.sin(time*0.1)*np.exp(-time+2)
	df_init= df_init.append(df)	
	print(str(len(df_init['deltatemp4'])/max_lines*100)+"%")


	if(len(df_init['deltatemp4'])>=max_lines):
		break;

df_init['index'] = np.arange(0,len(df_init['timesincelastopen']))

df_init.set_index('index',inplace=True)

if(len(df_init.index)>max_lines):
	df_init.drop(df_init.index[max_lines:],inplace=True)


print(df_init.info())

df_init.to_csv('.\data\data.csv', sep=',',mode='w+',float_format='%.2f')

# df_init['deltatemp1'].plot()
# df_init['deltatemp2'].plot()
# df_init['deltatemp3'].plot()
# df_init['deltatemp4'].plot()

# plt.show()



