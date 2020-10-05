#-*-coding:UTF8-*-
"""
created on Wes Aug 13 15:39 2020
@author：张平路
"""
from sklearn.linear_model import LinearRegression,Lasso
from sklearn import tree,model_selection
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor



X =np.array(pd.read_csv('data/Session2_trainData/X_train.csv',encoding='cp936'))
y =np.array(pd.read_csv('data/Session2_trainData/y_train.csv',encoding='cp936').loc[:]['收入'])
X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,random_state=666,test_size=0.5)
#split into two parts

#Linear Regression
print('LinearRegression:')
L = LinearRegression()

print('first assess')
L.fit(X_train,y_train)
print('R_square:{}'.format(r2_score(y_test,L.predict(X_test))))
print('MSE:{}'.format(np.mean(np.mean((L.predict(X_test)-y_test)**2))/len(X_test)))
print('MAE:{}'.format(np.mean(np.mean(abs((L.predict(X_test)-y_test))))/len(X_test)))
print('second assess')
L.fit(X_test,y_test)
print('R_square:{}'.format(r2_score(y_train,L.predict(X_train))))
print('MSE:{}'.format(np.mean(np.mean((L.predict(X_train)-y_train)**2))/len(X_train)))
print('MAE:{}'.format(np.mean(np.mean(abs((L.predict(X_train)-y_train))))/len(X_train)))
print('\n')



print('CART tree')
clf = tree.DecisionTreeRegressor()
clf.fit(X_train,y_train)
print('first assess')
print('R_square:{}'.format(r2_score(y_test,clf.predict(X_test))))
print('MSE:{}'.format(np.mean(np.mean((clf.predict(X_test)-y_test)**2))/len(X_test)))
print('MAE:{}'.format(np.mean(np.mean(abs((clf.predict(X_test)-y_test))))/len(X_test)))
print('second assess')
clf.fit(X_test,y_test)
print('R_square:{}'.format(r2_score(y_train,clf.predict(X_train))))
print('MSE:{}'.format(np.mean(np.mean((clf.predict(X_train)-y_train)**2))/len(X_train)))
print('MAE:{}'.format(np.mean(np.mean(abs((clf.predict(X_train)-y_train))))/len(X_train)))

print('\n')



print('\n')
print('Lasso Regression')
reg = Lasso(alpha =0.1)
reg.fit(X_train,y_train)
print('first assess')
print('R_square:{}'.format(r2_score(y_test,reg.predict(X_test))))
print('MSE:{}'.format(np.mean(np.mean((reg.predict(X_test)-y_test)**2))/len(X_test)))
print('MAE:{}'.format(np.mean(np.mean(abs((reg.predict(X_test)-y_test))))/len(X_test)))
print('second assess')
reg.fit(X_test,y_test)
print('R_square:{}'.format(r2_score(y_train,reg.predict(X_train))))
print('MSE:{}'.format(np.mean(np.mean((reg.predict(X_train)-y_train)**2))/len(X_train)))
print('MAE:{}'.format(np.mean(np.mean(abs((reg.predict(X_train)-y_train))))/len(X_train)))
print('\n')

print("MLP")
model = MLPRegressor(hidden_layer_sizes=(10,10),random_state=10)
model.fit(X_train,y_train)
print('first assess')
print('R_square:{}'.format(r2_score(y_test,model.predict(X_test))))
print('MSE:{}'.format(np.mean(np.mean((model.predict(X_test)-y_test)**2))/len(X_test)))
print('MAE:{}'.format(np.mean(np.mean(abs((model.predict(X_test)-y_test))))/len(X_test)))
print('second assess')
model.fit(X_test,y_test)
print('R_square:{}'.format(r2_score(y_train,model.predict(X_train))))
print('MSE:{}'.format(np.mean(np.mean((model.predict(X_train)-y_train)**2))/len(X_train)))
print('MAE:{}'.format(np.mean(np.mean(abs((model.predict(X_train)-y_train))))/len(X_train)))
print('\n')

print("RandomForestRegressor")
RDF = RandomForestRegressor()
RDF.fit(X_train,y_train)
print('first assess')
print('R_square:{}'.format(r2_score(y_test,RDF.predict(X_test))))
print('MSE:{}'.format(np.mean(np.mean((RDF.predict(X_test)-y_test)**2))/len(X_test)))
print('MAE:{}'.format(np.mean(np.mean(abs((RDF.predict(X_test)-y_test))))/len(X_test)))
print('second assess')
RDF.fit(X_test,y_test)
print('R_square:{}'.format(r2_score(y_train,RDF.predict(X_train))))
print('MSE:{}'.format(np.mean(np.mean((RDF.predict(X_train)-y_train)**2))/len(X_train)))
print('MAE:{}'.format(np.mean(np.mean(abs((RDF.predict(X_train)-y_train))))/len(X_train)))
print('\n')

print("AdaboostRegressor")
ABR = AdaBoostRegressor()
ABR.fit(X_train,y_train)
print('first assess')
print('R_square:{}'.format(r2_score(y_test,ABR.predict(X_test))))
print('MSE:{}'.format(np.mean(np.mean((ABR.predict(X_test)-y_test)**2))/len(X_test)))
print('MAE:{}'.format(np.mean(np.mean(abs((ABR.predict(X_test)-y_test))))/len(X_test)))
print('second assess')
ABR.fit(X_test,y_test)
print('R_square:{}'.format(r2_score(y_train,ABR.predict(X_train))))
print('MSE:{}'.format(np.mean(np.mean((ABR.predict(X_train)-y_train)**2))/len(X_train)))
print('MAE:{}'.format(np.mean(np.mean(abs((ABR.predict(X_train)-y_train))))/len(X_train)))
print('\n')

