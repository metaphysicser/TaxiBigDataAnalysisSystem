#-*-coding:UTF8-*-
"""
created on Sun Agu 16 13:04 2020
@author:zpl
"""
from sklearn import tree,model_selection
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd
import json
from business_calendar import Calendar

X = []#dependent variable
y =pd.read_csv('money.csv',encoding='cp936')
y1 = pd.read_csv('avaiblity.csv',encoding='cp936')

fr = open('flow_data/flow_data_in_districts_1.txt')
content = fr.read()
dict = eval(content)

district  =['baiyun', 'conghua', 'haizhu', 'huadu', 'huangpu', 'liwan', 'nansha', 'panyu', 'tianhe', 'yuexiu', 'zengcheng']
#record history
for i in range(1,8):
    file = 'data/flow_data_in_districts/flow_data_in_districts_'+str(i)+'.txt'
    fr = open('data/flow_data_in_districts/flow_data_in_districts_1.txt')
    content = fr.read()
    dict = eval(content)

     #judge whether is workday
    date = '2017-2-' + str(i)
    cal = Calendar()
    judge_workday = cal.isworkday(date)
    if judge_workday == True:
        judge_workday = 1
    else:
        judge_workday = 0
    dict_total= {}
    #transform  into json
    file_name = 'MoneyAndAvty_district_' + str(i) + '.json'
    with open(file_name, 'w') as json_file:
        for dist in district:
            print(dist)
            temp = [2, i, judge_workday, dict[dist]]

            X.append(temp)
            dict_ = {'district': dist, 'money': y.loc[i - 1][dist], 'avaiblity': y1.loc[i - 1][dist]}
            json_str = json.dumps(dict_)
            json_file.write(json_str)

X = np.array(X)
y =np.array(pd.read_csv('data/Session2_trainData/y_train.csv',encoding='cp936').loc[:]['收入'])
y1 = np.array(pd.read_csv('data/Session2_trainData/y_train.csv',encoding='cp936').loc[:]['利用率'])

_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,random_state=666,test_size=0.5)
X_train1,X_test1,y_train1,y_test1 = model_selection.train_test_split(X,y1,random_state=666,test_size=0.5)
#money
clf1 = tree.DecisionTreeRegressor()
clf1.fit(X,y)
#avty
clf2 = tree.DecisionTreeRegressor()
clf2.fit(X,y1)

for i in range(8,15):
    file = 'data/flow_data_in_districts/flow_data_in_districts_'+str(i)+'.txt'
    fr = open('data/flow_data_in_districts/flow_data_in_districts_1.txt')
    content = fr.read()
    dict = eval(content)


    date = '2017-2-' + str(i)
    cal = Calendar()

    judge_workday = cal.isworkday(date)
    if judge_workday == True:
        judge_workday = 1
    else:
        judge_workday = 0
    dict_ = {}
    file_name = 'MoneyAndAvty_district_' + str(i) + '.json'
    with open(file_name, 'w') as json_file:
        for dist in district:
            temp = [[2, i, judge_workday, dict[dist]]]

            money = clf1.predict(temp)[0]
            avty = clf2.predict(temp)[0]

            dict_ = {'district': dist, 'money': money, 'avaiblity':avty}
            json_str = json.dumps(dict_)
            json_file.write(json_str)