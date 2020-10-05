# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     districts_taxi_flow
   Description :
   Author :       Giyn
   date：          2020/8/14 19:38:17
-------------------------------------------------
   Change Activity:
                   2020/8/14 19:38:17
-------------------------------------------------
"""
__author__ = 'Giyn'

import pandas as pd
import numpy as np
import logging
import multiprocessing
from Utils import judge_areas
from Utils.CoordinateConverter import wgs84_to_gcj02


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # log information settings

district_names = ['baiyun', 'conghua', 'haizhu', 'huadu', 'huangpu', 'liwan',
                  'nansha', 'panyu', 'tianhe', 'yuexiu', 'zengcheng']

judge = judge_areas.JudgeAreas()


def processing(each_data):
    raw_data_path = '../data/operate_his/operate_his{}.csv'.format(str(each_data))
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

    flow = {'baiyun': 0, 'conghua': 0, 'haizhu': 0, 'huadu': 0, 'huangpu': 0, 'liwan': 0,
            'nansha': 0, 'panyu': 0, 'tianhe': 0, 'yuexiu': 0, 'zengcheng': 0}

    logging.info('Start to count the flow of one district!')
    # Calculate the data volume of getting on and off the bus through [Get_On Point]
    for i in range(len(get_on_points)):
        lng_on = round(get_on_points[i][0], 3)  # Decrease the accuracy of longitude of [get_on point]
        lat_on = round(get_on_points[i][1], 3)  # Decrease the accuracy of latitude of [get_on point]
        """
        The amount of data when getting on the taxi and passing through the [get_on point] + 
        the amount of data when getting off the taxi and passing through the [get_on point]
        """
        for each_name in district_names:
            if judge.judge_area(each_name, array=wgs84_to_gcj02(np.array([get_on_points[i]])))[0] == True:
                flow_on = operate_his.loc[
                              (operate_his['GET_ON_LONGITUDE'] >= (lng_on - 0.003)) &
                              (operate_his['GET_ON_LONGITUDE'] <= (lng_on + 0.003)) &
                              (operate_his['GET_ON_LATITUDE'] >= (lat_on - 0.003)) &
                              (operate_his['GET_ON_LATITUDE'] <= (lat_on + 0.003))].shape[0] + operate_his.loc[
                              (operate_his['GET_OFF_LONGITUDE'] >= (lng_on - 0.003)) &
                              (operate_his['GET_OFF_LONGITUDE'] <= (lng_on + 0.003)) &
                              (operate_his['GET_OFF_LATITUDE'] >= (lat_on - 0.003)) &
                              (operate_his['GET_OFF_LATITUDE'] <= (lat_on + 0.003))].shape[0]
                flow[each_name] += flow_on
    logging.info('Successfully count the flow of get_on points!')

    # Calculate the data volume of getting on and off the bus through [Get_Off Point]
    for j in range(len(get_off_points)):
        lng_off = round(get_off_points[j][0], 3)  # Decrease the accuracy of longitude of [get_off point]
        lat_off = round(get_off_points[j][1], 3)  # Decrease the accuracy of latitude of [get_off point]
        """
        The amount of data when getting on the taxi and passing through the [get_off point] + 
        the amount of data when getting off the taxi and passing through the [get_off point]
        """
        for each_name in district_names:
            if judge.judge_area(each_name, array=wgs84_to_gcj02(np.array([get_off_points[j]])))[0] == True:
                flow_off = operate_his.loc[
                               (operate_his['GET_ON_LONGITUDE'] >= (lng_off - 0.003)) &
                               (operate_his['GET_ON_LONGITUDE'] <= (lng_off + 0.003)) &
                               (operate_his['GET_ON_LATITUDE'] >= (lat_off - 0.003)) &
                               (operate_his['GET_ON_LATITUDE'] <= (lat_off + 0.003))].shape[0] + operate_his.loc[
                               (operate_his['GET_OFF_LONGITUDE'] >= (lng_off - 0.003)) &
                               (operate_his['GET_OFF_LONGITUDE'] <= (lng_off + 0.003)) &
                               (operate_his['GET_OFF_LATITUDE'] >= (lat_off - 0.003)) &
                               (operate_his['GET_OFF_LATITUDE'] <= (lat_off + 0.003))].shape[0]
                flow[each_name] += flow_off
    logging.info('Successfully count the flow of get_off points!')

    save_path = '../data/flow_data_in_districts/flow_data_in_districts_{}.txt'.format(str(each_data))
    with open(save_path, 'w') as file:
        file.write(str(flow))
    logging.info('Successfully save data!')


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    index = range(1, 15)
    pool.map(processing, index)


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
