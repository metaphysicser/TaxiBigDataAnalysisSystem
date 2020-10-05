# -*- coding: utf-8 -*-
"""
Created on Wes Aug 12 19:20: 2020
@author: 张平路
"""


import pandas as pd
import numpy as np
import csv
from business_calendar import Calendar


fr1 = pd.read_csv('data/Session2_trainData/flow.csv', encoding='cp936')

fr2 = pd.read_csv('data/Session2_trainData/money.csv', encoding='cp936')

fr3  = pd.read_csv('data/Session2_trainData/avaiblity.csv',encoding='cp936')

X_train_csv = open('X_train.csv','w',newline='')
writer1 = csv.writer(X_train_csv)
writer1.writerow(('月份','日期','工作日','流量'))

y_train_csv = open('y_train.csv','w',newline='')
writer2 = csv.writer(y_train_csv)
writer2.writerow(('收入','利用率'))
for i in range(1,8):
    cal = Calendar()
    date = '2017-02-'+str(i)
    judge_workday = cal.isworkday(date)
    if judge_workday ==True:
        judge_workday = 1
    else:
        judge_workday =0
    district = ['从化区', '南沙区', '增城区', '天河区', '海珠区', '番禺区', '白云区', '花都区', '荔湾区', '越秀区', '黄浦区']

    for j in district:
        writer1.writerow((2,i,judge_workday,fr1.loc[i-1][j]))
        writer2.writerow((fr2.loc[i-1][j],fr3.loc[i-1][j]))

X_train_csv.close()
y_train_csv.close()
