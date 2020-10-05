# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 14:20 2020
@author: 张平路
"""


import pandas as pd
import numpy as np
from business_calendar import Calendar
from matplotlib.path import Path
import csv



def judge_district(nparray):
    """judge the point belonging to which district

    the function will use the path model with the data of boundary to judge
    which district the point in

    Args:
        nparry:a nparry involves longitude and lagitude which shape is (n,2)
    Returns:
        res:the disrict that the point really in

    """
    district = ['从化区','南沙区','增城区','天河区','海珠区','番禺区','白云区','花都区','荔湾区','越秀区','黄浦区']

    res = []
    boundry = []
    for i in range(len(district)):
        file = 'data/DistrictBoundaryInChinese/' + str(district[i]) + '.txt'
        fr = open(file)
        data = fr.readline().split(',')
        for j in data:
            j = float(j)
        data = np.array(data)
        b = data.reshape(len(data) // 2, 2)#transform shape into (n,2)
        boundry.append(b)

    for m in range(len(nparray)):
        for i in range(len(district)):
            flag = 0
            path = Path(boundry[i], closed=True)#use the path model


            #print([nparry[0,0],nparry[0,1])
            if path.contains_points([[float(nparray[m,0]),float(nparray[m,1])]]) == [ True]:
                flag = 1
                res.append(district[i])
                print('第'+str(m)+'个数据检查完成')
                break
        if flag == 0:
            res.append(district[0])
            print('第' + str(m) + '个数据检查完成')

    return res



def saveAvaiblityAndMoney():
    """create two csvtable storing avaiblity and money

    select data randomly to reduce processing time.Iterate the data and judge the district blonging to.comput the
    avarge and save in the csv table

    Args:None
    Returns:None

    """
    #create the avaiblity csv table
    csv_file = open('avaiblity.csv','w',newline='')
    writer = csv.writer(csv_file)
    writer.writerow(('日期','从化区','南沙区','增城区','天河区','海珠区','番禺区','白云区','花都区','荔湾区','越秀区','黄浦区'))
    #create the money csv money
    csv_file2 = open('money.csv', 'w', newline='')
    writer2 = csv.writer(csv_file2)
    writer2.writerow(('日期', '从化区', '南沙区', '增城区', '天河区', '海珠区', '番禺区', '白云区', '花都区', '荔湾区', '越秀区', '黄浦区'))

    for i in range(1,8):
        data = pd.DataFrame(np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]).reshape(1,11),
                            columns=['从化区', '南沙区', '增城区', '天河区', '海珠区', '番禺区', '白云区', '花都区', '荔湾区', '越秀区', '黄浦区'])

        count = pd.DataFrame(np.zeros((1, 11)),
                            columns=['从化区', '南沙区', '增城区', '天河区', '海珠区', '番禺区', '白云区', '花都区', '荔湾区', '越秀区', '黄浦区'])
        money = pd.DataFrame(np.zeros((1, 11)),
                             columns=['从化区', '南沙区', '增城区', '天河区', '海珠区', '番禺区', '白云区', '花都区', '荔湾区', '越秀区', '黄浦区'])
        file = 'data/operate/operate_his'+str(i)+'.csv'
        operate = pd.read_csv(file)
        #select 20000 data in each table randomly
        operate = operate.sample(n = 20000,random_state=123,axis=0)
        longitude = operate['GET_ON_LONGITUDE']
        latitude = operate['GET_ON_LATITUDE']
        load_mile = operate['LOAD_MILE']

        empty_mile = operate['EMPTY_MILE']
        operate_money = operate['OPERATE_MONEY']
        longitude_ = longitude[:,np.newaxis]
        latitude_ = latitude[:,np.newaxis]

        c = np.hstack((longitude_,latitude_))
        judge = judge_district(c)
        judge = np.array(judge)



        for j in range(len(load_mile)):
            print('第'+str(i)+'个文件的第'+str(j)+'次计算')

            if load_mile.iat[j] + empty_mile.iat[j] == 0.0:#avoid nan in final result
                empty_mile.iat[j] = 1

            avty = load_mile.iat[j]/(load_mile.iat[j]+empty_mile.iat[j])
            data[judge[j]] += avty
            money[judge[j]] += operate_money[j]/100
            count[judge[j]] +=1


        data = np.array(data)
        count = np.array(count)
        count[count==0] =1
        money = np.array(money)

        data = data/count
        data = data[0]
        money = money/count
        money = money[0]
        writer.writerow(('2017-2-' + str(i), data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
                         data[8], data[9], data[10]))
        writer2.writerow(('2017-2-' + str(i),money[0],money[1],money[2],money[3],money[4],money[5],money[6],money[7],money[8],money[9],money[10],))


    csv_file.close()
    csv_file2.close()



