# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     districts_flow_degree
   Description :
   Author :       Giyn
   date：          2020/8/17 16:42:02
-------------------------------------------------
   Change Activity:
                   2020/8/17 16:42:02
-------------------------------------------------
"""
__author__ = 'Giyn'

import json
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # log information settings

districts_size_dict = {'baiyun': 796, 'conghua': 1974.5, 'haizhu': 102, 'huadu': 970, 'huangpu': 90.95, 'liwan': 62.4,
                       'nansha': 803, 'panyu': 786, 'tianhe': 96, 'yuexiu': 33.8, 'zengcheng': 1616.47}

district_names = ['baiyun', 'conghua', 'haizhu', 'huadu', 'huangpu', 'liwan',
                  'nansha', 'panyu', 'tianhe', 'yuexiu', 'zengcheng']

districts_flow_degree = {'baiyun': 0, 'conghua': 0, 'haizhu': 0, 'huadu': 0, 'huangpu': 0, 'liwan': 0,
                         'nansha': 0, 'panyu': 0, 'tianhe': 0, 'yuexiu': 0, 'zengcheng': 0}


for day in range(1, 15):
    districts_flow_degree_list = []
    data_path = '../data/total_districts_flow/total_districts_flow_{}.txt'.format(str(day))

    with open(data_path, 'r') as file:
        districts_flow_dict = json.loads(file.read().replace('\'', '\"'))

    for each_name in district_names:
        if round(districts_flow_dict[each_name] / districts_size_dict[each_name]) == 0:
            districts_flow_degree[each_name] = '无数据'
        elif round(districts_flow_dict[each_name] / districts_size_dict[each_name]) <= 1000:
            districts_flow_degree[each_name] = '畅通'
        elif (round(districts_flow_dict[each_name] / districts_size_dict[each_name]) >= 1000) & (round(districts_flow_dict[each_name] / districts_size_dict[each_name]) <= 5000):
            districts_flow_degree[each_name] = '普通'
        else:
            districts_flow_degree[each_name] = '拥挤'

        district_and_status_dict = {'district': each_name, 'status': districts_flow_degree[each_name]}
        districts_flow_degree_list.append(district_and_status_dict)

    save_path = '../data/districts_flow_degree/districts_flow_degree_{}.txt'.format(str(day))
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(str(districts_flow_degree_list))
    logging.info('Successfully save data!')


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
