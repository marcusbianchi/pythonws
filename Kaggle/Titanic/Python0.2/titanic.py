import pandas as pd
import numpy as np 
import pylab as P

df = pd.read_csv('./data/train.csv',header=0)

df['Gender']=df['Sex'].map({'female':0,'male':1}).astype(int)

df['EmbarkedLoc']=df['Embarked'].map({'C':0,'Q':1,'S':2},'ignore')

df['EmbarkedLoc'].fillna(np.random.randint(0,3),inplace = True)


median_ages = np.zeros((2,3))

for i in range(0,2):
	for j in range(0,3):	
		median_ages[i,j] = df[(df['Gender']==i) & (df['Pclass']==j+1)]['Age'].dropna().median();

df['AgeFill'] = df['Age']

for i in range(0,2):
	for j in range(0,3):
		df.loc[(df.Age.isnull()) & (df.Gendr==i) & (df.Pclass == j+1),'AgeFill'] = median_ages[i,j]

df['AgeIsNull'] = pd.isnull(df.Age).astype(int)

print(df.describe())

df['FamilySize'] = df['SibSp'] + df['Parch']

df['Age*Class'] = df.AgeFill * df.Pclass

df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1) 

df = df.drop(['Age'], axis=1)

train_data = df.values

