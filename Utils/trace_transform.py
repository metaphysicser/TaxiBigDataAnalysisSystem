# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     trace_transform
   Description :
   Author :       Giyn
   date：          2020/8/16 16:30:40
-------------------------------------------------
   Change Activity:
                   2020/8/16 16:30:40
-------------------------------------------------
"""
__author__ = 'Giyn'

import os
import json
import logging
import numpy as np
from Utils.CoordinateConverter import wgs84_to_gcj02


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # log information settings


def trace_transform_frontend():
    for day in range(1, 15):
        trace_data_path = '../data/raw_exceptionCarsTrace_Frontend/day{}Pre/'.format(str(day))
        file_name_list = os.listdir(trace_data_path)

        logging.info('Start to work!')

        for each_file_name in file_name_list:
            each_file_path = trace_data_path + each_file_name
            with open(each_file_path, 'r', encoding='utf-8') as file:
                raw_unusual_car_info = file.read()

            unusual_car_list = json.loads(raw_unusual_car_info)
            unusual_car_dict = unusual_car_list[0]
            unusual_car_trace_list = unusual_car_dict['lnglat']
            dealed_unusual_car_trace_list = wgs84_to_gcj02(np.array(unusual_car_trace_list)).tolist()
            assert isinstance(dealed_unusual_car_trace_list, object)
            unusual_car_list[0]['lnglat'] = dealed_unusual_car_trace_list

            logging.info('Successfully deal the trace of a unusual taxi!')
            save_path = '../data/exceptionalCarsTrace_Frontend/day{}Pre/{}'.format(str(day), each_file_name)
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(str(unusual_car_list))
            logging.info('Successfully save data!')


def trace_transform_android():
    for day in range(1, 15):
        trace_data_path = '../data/raw_exceptionCarsTrace_Android/day{}/'.format(str(day))
        file_name_list = os.listdir(trace_data_path)

        logging.info('Start to work!')

        for each_file_name in file_name_list:
            each_file_path = trace_data_path + each_file_name
            with open(each_file_path, 'r', encoding='utf-8') as file:
                raw_unusual_car_trace = file.read()

            unusual_car_trace_list = json.loads(raw_unusual_car_trace)
            for i in range(len((unusual_car_trace_list))):
                dealed_points_array = wgs84_to_gcj02(np.array([[unusual_car_trace_list[i]['lng'], unusual_car_trace_list[i]['lat']]]))
                unusual_car_trace_list[i]['lng'] = dealed_points_array[0][0]
                unusual_car_trace_list[i]['lat'] = dealed_points_array[0][1]

            logging.info('Successfully deal the trace of a unusual taxi!')

            save_path = '../data/exceptionalCarsTrace_Android/day{}/{}'.format(str(day), each_file_name)
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(str(unusual_car_trace_list))
            logging.info('Successfully save data!')


if __name__ == "__main__":
    trace_transform_frontend()
    trace_transform_android()


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
