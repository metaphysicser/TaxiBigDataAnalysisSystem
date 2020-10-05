# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:20 2020
@author: 张平路
"""


import pandas as pd
import numpy as np
from business_calendar import Calendar
from matplotlib.path import Path
import csv

def judge_district(longitude,latitude):
    """judge the point belonging to which district

        the function will use the path model with the data of boundary to judge
        which district the point in

        Args:
            nparry:a nparry involves longitude and lagitude which shape is (n,2)
        Returns:
            res:the disrict that the point really in

        """
    district = ['从化区','南沙区','增城区','天河区','海珠区','番禺区','白云区','花都区','荔湾区','越秀区','黄浦区']
    num = 0

    for i in range(len(district)):
        file = 'data/DistrictBoundaryInChinese/'+str(district[i])+'.txt'
        fr = open(file)
        data = fr.readline().split(',')
        for j in data:
            j = float(j)
        data = np.array(data)
        b = data.reshape(len(data) // 2, 2)
        path = Path(b, closed=True)

        if path.contains_points([[longitude,latitude]]) == [ True]:
            num = i
            break

    return district[num]

if __name__ =='__main__':
    """create two csvtable storing avaiblity and money

       select data randomly to reduce processing time.Iterate the data and judge the district blonging to.comput the
       avarge and save in the csv table

       Args:None
       Returns:None

       """
    csv_file = open('flow.csv','w',newline='')
    writer = csv.writer(csv_file)
    writer.writerow(('日期','从化区','南沙区','增城区','天河区','海珠区','番禺区','白云区','花都区','荔湾区','越秀区','黄浦区'))
    area_size = [1974.5,803,1616.47,96,102,786,796,970,62.4,33.8,90.95]


    for i in range(1,8):
        data = pd.DataFrame(np.zeros((1, 11)),
                            columns=['从化区', '南沙区', '增城区', '天河区', '海珠区', '番禺区', '白云区', '花都区', '荔湾区', '越秀区', '黄浦区'])
        file = 'data/operate/operate_his'+str(i)+'.csv'
        operate = pd.read_csv(file)
        longitude = operate['GET_ON_LONGITUDE']
        latitude = operate['GET_ON_LATITUDE']

        for j in range(len(longitude)):
            data[judge_district(longitude[j], latitude[j])] += 1
            print("完成第"+str(i)+'个文件的第'+str(j+1)+'次判断')

        data = np.array(data)
        data = data/area_size
        data = data[0]
        writer.writerow(('2017-2-'+str(i),data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))

    csv_file.close()



