# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     taxi_flow_weight
   Description :
   Author :       Giyn
   date：          2020/8/15 16:57:13
-------------------------------------------------
   Change Activity:
                   2020/8/15 16:57:13
-------------------------------------------------
"""
__author__ = 'Giyn'

import pandas as pd
import numpy as np
import logging
from Utils.CoordinateConverter import wgs84_to_gcj02
from Utils import judge_areas


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # log information settings

judge = judge_areas.JudgeAreas()
district_names = ['baiyun', 'conghua', 'haizhu', 'huadu', 'huangpu', 'liwan',
                  'nansha', 'panyu', 'tianhe', 'yuexiu', 'zengcheng']

weight = {"baiyun": 0, "conghua": 0, "haizhu": 0, "huadu": 0, "huangpu": 0, "liwan": 0,
          "nansha": 0, "panyu": 0, "tianhe": 0, "yuexiu": 0, "zengcheng": 0}

raw_data_path = '../data/operate_his/operate_his1.csv'
operate_his = pd.read_csv(raw_data_path, low_memory=False)
column = ['GET_ON_LONGITUDE', 'GET_ON_LATITUDE', 'GET_OFF_LONGITUDE', 'GET_OFF_LATITUDE']
operate_his = operate_his.loc[0:6000, column]

operate_his_on_points = operate_his.loc[:, ['GET_ON_LONGITUDE', 'GET_ON_LATITUDE']]
operate_his_off_points = operate_his.loc[:, ['GET_OFF_LONGITUDE', 'GET_OFF_LATITUDE']]
operate_his_on_points = operate_his_on_points[
    ~operate_his_on_points['GET_ON_LONGITUDE'].isin([0])]  # remove rows with longitude 0
operate_his_on_points = operate_his_on_points[
    ~operate_his_on_points['GET_ON_LATITUDE'].isin([0])]  # remove rows with latitude 0
operate_his_off_points = operate_his_off_points[
    ~operate_his_off_points['GET_OFF_LONGITUDE'].isin([0])]  # remove rows with longitude 0
operate_his_off_points = operate_his_off_points[
    ~operate_his_off_points['GET_OFF_LATITUDE'].isin([0])]  # remove rows with latitude 0

operate_his_on_points = operate_his_on_points[0:5000]
operate_his_off_points = operate_his_off_points[0:5000]

assert isinstance(operate_his_on_points.values, object)
get_on_points = operate_his_on_points.values
assert isinstance(operate_his_off_points.values, object)
get_off_points = operate_his_off_points.values

logging.info('Start to count the flow weight of all the districts!')
for i in range(len(get_on_points)):
    for each_name in district_names:
        if judge.judge_area(each_name, array=wgs84_to_gcj02(np.array([get_on_points[i]])))[0] == True:
            weight[each_name] += 1
logging.info('Successfully count the flow of get_on points!')

for j in range(len(get_off_points)):
    for each_name in district_names:
        if judge.judge_area(each_name, array=wgs84_to_gcj02(np.array([get_on_points[j]])))[0] == True:
            weight[each_name] += 1
logging.info('Successfully count the flow of get_off points!')


for k in district_names:
    weight[k] = weight[k] / 10000

save_path = '../data/districts_flow_weight.txt'
with open(save_path, 'w') as file:
    file.write(str(weight))

logging.info('Successfully save weight data!')


################################################################################################################
#                               ___                         ___                                     ___        #
#                              /\__\                       /\  \         _____                     /\  \       #
#    ____         _____       /:/ _/_         ___          \:\  \       /::\  \       ___         /::\  \      #
#   / __ \       / ___ \     /:/ /\  \       /\__\          \:\  \     /:/\:\  \     /\__\       /:/\:\  \     #
#  / /  \ \     / /   \_)   /:/ /::\  \     /:/  /      ___  \:\  \   /:/  \:\__\   /:/__/      /:/  \:\  \    #
# ( (    ) )   ( (  ____   /:/_/:/\:\__\   /:/__/      /\  \  \:\__\ /:/__/ \:|__| /::\  \     /:/__/ \:\__\   #
# ( (  /\) )   ( ( (__  )  \:\/:/ /:/  /  /::\  \      \:\  \ /:/  / \:\  \ /:/  / \/\:\  \__  \:\  \ /:/  /   #
#  \ \_\ \/     \ \__/ /    \::/ /:/  /  /:/\:\  \      \:\  /:/  /   \:\  /:/  /   ~~\:\/\__\  \:\  /:/  /    #
#   \___\ \_     \____/      \/_/:/  /   \/__\:\  \      \:\/:/  /     \:\/:/  /       \::/  /   \:\/:/  /     #
#        \__)                  /:/  /         \:\__\      \::/  /       \::/  /        /:/  /     \::/  /      #
#                              \/__/           \/__/       \/__/         \/__/         \/__/       \/__/       #
#                                                                                                              #
################################################################################################################

##########################################################################
#      ___           ___           ___           ___           ___       #
#     /\  \         /\  \         /\  \         /\  \         /\  \      #
#     \:\  \       /::\  \       /::\  \       /::\  \       /::\  \     #
#      \:\  \     /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/\ \  \    #
#      /::\  \   /::\~\:\__\   /:/  \:\__\   /::\~\:\  \   _\:\~\ \  \   #
#     /:/\:\__\ /:/\:\ \:|__| /:/__/ \:|__| /:/\:\ \:\__\ /\ \:\ \ \__\  #
#    /:/  \/__/ \:\~\:\/:/  / \:\  \ /:/  / \/__\:\/:/  / \:\ \:\ \/__/  #
#   /:/  /       \:\ \::/  /   \:\  /:/  /       \::/  /   \:\ \:\__\    #
#   \/__/         \:\/:/  /     \:\/:/  /        /:/  /     \:\/:/  /    #
#                  \::/__/       \::/__/        /:/  /       \::/  /     #
#                   ~~            ~~            \/__/         \/__/      #
#                                                                        #
##########################################################################
