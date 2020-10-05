# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     total_districts_flow
   Description :
   Author :       Giyn
   date：          2020/8/17 1:04:59
-------------------------------------------------
   Change Activity:
                   2020/8/17 1:04:59
-------------------------------------------------
"""
__author__ = 'Giyn'

import logging
import json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # log information settings

district_names = ['baiyun', 'conghua', 'haizhu', 'huadu', 'huangpu', 'liwan',
                  'nansha', 'panyu', 'tianhe', 'yuexiu', 'zengcheng']

with open('../data/districts_flow_weight.txt') as file:
    flow_weight = file.read().replace("\'", "\"")
    flow_weight_dict = json.loads(flow_weight)

for day in range(1, 15):
    districts_flow_path = '../data/flow_data_in_districts/flow_data_in_districts_{}.txt'.format(str(day))
    with open(districts_flow_path, 'r') as f:
        districts_flow = f.read().replace("\'", "\"")
        districts_flow_dict = json.loads(districts_flow)

    for each_district in district_names:
        districts_flow_dict[each_district] += 100000 * flow_weight_dict[each_district]
        districts_flow_dict[each_district] = int(districts_flow_dict[each_district])
    save_path = '../data/total_districts_flow/total_districts_flow_{}.txt'.format(str(day))

    with open(save_path, 'w') as file:
        file.write(str(districts_flow_dict))
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
