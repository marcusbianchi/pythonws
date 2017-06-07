import pandas as pd
import numpy as np 
import pylab as P
import csv as csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def featureSelection(file_path):
	df = pd.read_csv(file_path,header=0)

	df['Gender']=df['Sex'].map({'female':0,'male':1}).astype(int)

	df['EmbarkedLoc']=df['Embarked'].map({'C':0,'Q':1,'S':2},'ignore')

	df['EmbarkedLoc'].fillna(np.random.randint(0,3),inplace = True)

	for i in range(1,4):
		df[df['Fare'].isnull()] = df[df['Fare'].notnull() & df['Pclass']==i]['Fare'].mean()


	median_ages = np.zeros((2,3))

	for i in range(0,2):
		for j in range(0,3):	
			median_ages[i,j] = df[(df['Gender']==i) & (df['Pclass']==j+1)]['Age'].dropna().median();

	df['AgeFill'] = df['Age']

	for i in range(0,2):
		for j in range(0,3):
			df.loc[(df.Age.isnull()) & (df.Gender==i) & (df.Pclass == j+1),'AgeFill'] = median_ages[i,j]

	df['AgeIsNull'] = pd.isnull(df.Age).astype(int)

	df['FamilySize'] = df['SibSp'] + df['Parch']

	df['Age*Class'] = df.AgeFill * df.Pclass

	df = df.drop(['PassengerId','Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1) 

	df = df.drop(['Age'], axis=1)

	df = df.dropna()

	return df

#----------------------Get Train Data from Dataset --------------------------------------------
df_train = featureSelection('./data/train.csv')

train_data = df_train.values

#----------------------Get Test Data from Dataset --------------------------------------------

df_test = featureSelection('./data/test.csv')

test_data = df_test.values

#---------------------Score Random Forest ----------------------------------------------------

X_train,X_test,y_train,y_test = train_test_split(train_data[0:,1:],train_data[0:,0])

forest = RandomForestClassifier(n_estimators = 10000,max_features=None,min_samples_split=5)

forest.fit(X_train,y_train)

print(forest.score(X_train,y_train))

print(forest.score(X_test,y_test))

#-----------------Predict Result Forest--------------------------------------------------------

forest = forest.fit(train_data[0:,1:],train_data[0:,0])

output = forest.predict(test_data).astype(int)

df_test = pd.read_csv('./data/test.csv',header=0)

with open('./data/forest.csv','w', newline='') as forestmodel_csv:
	forestmodel_csv_object = csv.writer(forestmodel_csv)
	forestmodel_csv_object.writerow(['PassengerId','Survived'])
	forestmodel_csv_object.writerows(zip(df_test['PassengerId'],output))

print('Done')



#-----------------SVM Test--------------------------------------------------------------------

# from sklearn.svm import SVC

# svm = SVC(kernel='rbf',C=50, gamma=0.1)

# svm.fit(X_train,y_train)

# print(svm.score(X_train,y_train))

# print(svm.score(X_test,y_test))


