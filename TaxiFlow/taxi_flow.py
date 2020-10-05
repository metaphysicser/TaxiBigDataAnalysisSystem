# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     districts_taxi_flow
   Description :
   Author :       Giyn
   date：          2020/8/11 19:20:34
-------------------------------------------------
   Change Activity:
                   2020/8/11 19:20:34
-------------------------------------------------
"""
__author__ = 'Giyn'

import pandas as pd
import numpy as np
import logging
import multiprocessing
from Utils.CoordinateConverter import wgs84_to_gcj02


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # log information settings


def processing(day):
    logging.info('Start to deal data of one day!')
    raw_data_path = '../data/operate_his/operate_his{}.csv'.format(str(day))
    operate_his = pd.read_csv(raw_data_path, low_memory=False)
    column = ['GET_ON_LONGITUDE', 'GET_ON_LATITUDE', 'GET_OFF_LONGITUDE', 'GET_OFF_LATITUDE']
    operate_his = operate_his.loc[0:60000, column]

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

    assert isinstance(operate_his_on_points.values, object)
    assert isinstance(operate_his_off_points.values, object)

    operate_his_on_points = operate_his_on_points[0:50000]
    operate_his_off_points = operate_his_off_points[0:50000]
    get_on_points = operate_his_on_points.values
    get_off_points = operate_his_off_points.values

    flow_data = []
    # Calculate the data volume of getting on and off the bus through [Get_On Point]
    for i in range(len(get_on_points)):
        lng_on = round(get_on_points[i][0], 3)  # Decrease the accuracy of longitude of [get_on point]
        lat_on = round(get_on_points[i][1], 3)  # Decrease the accuracy of latitude of [get_on point]
        """
        The amount of data when getting on the taxi and passing through the [get_on point] + 
        the amount of data when getting off the taxi and passing through the [get_on point]
        """
        flow_on = operate_his.loc[
                      (operate_his['GET_ON_LONGITUDE'] >= (lng_on - 0.003)) &
                      (operate_his['GET_ON_LONGITUDE'] <= (lng_on + 0.003)) &
                      (operate_his['GET_ON_LATITUDE'] >= (lat_on - 0.003)) &
                      (operate_his['GET_ON_LATITUDE'] <= (lat_on + 0.003))].shape[0] + operate_his.loc[
                      (operate_his['GET_OFF_LONGITUDE'] >= (lng_on - 0.003)) &
                      (operate_his['GET_OFF_LONGITUDE'] <= (lng_on + 0.003)) &
                      (operate_his['GET_OFF_LATITUDE'] >= (lat_on - 0.003)) &
                      (operate_his['GET_OFF_LATITUDE'] <= (lat_on + 0.003))].shape[0]

        each_flow = {'lng': wgs84_to_gcj02(np.array([[get_on_points[i][0], get_on_points[i][1]]]))[0][0],
                     'lat': wgs84_to_gcj02(np.array([[get_on_points[i][0], get_on_points[i][1]]]))[0][1],
                     'count': flow_on}
        flow_data.append(each_flow)
    logging.info('Successfully count the flow of get_on points!')

    # Calculate the data volume of getting on and off the bus through [Get_Off Point]
    for j in range(len(get_off_points)):
        lng_off = round(get_off_points[j][0], 3)  # Decrease the accuracy of longitude of [get_off point]
        lat_off = round(get_off_points[j][1], 3)  # Decrease the accuracy of latitude of [get_off point]
        """
        The amount of data when getting on the taxi and passing through the [get_off point] + 
        the amount of data when getting off the taxi and passing through the [get_off point]
        """
        flow_off = operate_his.loc[
                       (operate_his['GET_ON_LONGITUDE'] >= (lng_off - 0.003)) &
                       (operate_his['GET_ON_LONGITUDE'] <= (lng_off + 0.003)) &
                       (operate_his['GET_ON_LATITUDE'] >= (lat_off - 0.003)) &
                       (operate_his['GET_ON_LATITUDE'] <= (lat_off + 0.003))].shape[0] + operate_his.loc[
                       (operate_his['GET_OFF_LONGITUDE'] >= (lng_off - 0.003)) &
                       (operate_his['GET_OFF_LONGITUDE'] <= (lng_off + 0.003)) &
                       (operate_his['GET_OFF_LATITUDE'] >= (lat_off - 0.003)) &
                       (operate_his['GET_OFF_LATITUDE'] <= (lat_off + 0.003))].shape[0]
        each_flow = {'lng': wgs84_to_gcj02(np.array([[get_off_points[j][0], get_off_points[j][1]]]))[0][0],
                     'lat': wgs84_to_gcj02(np.array([[get_off_points[j][0], get_off_points[j][1]]]))[0][1],
                     'count': flow_off}
        flow_data.append(each_flow)
    logging.info('Successfully count the flow of get_off points!')

    save_path = '../data/flow_data/flow_data_{}.txt'.format(str(day))
    with open(save_path, 'w') as file:
        file.write(str(flow_data))
    logging.info('Successfully save data!')


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    index = range(1, 8)
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
