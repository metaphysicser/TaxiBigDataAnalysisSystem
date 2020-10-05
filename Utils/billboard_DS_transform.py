# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     billboard_DS_transform
   Description :
   Author :       Giyn
   date：          2020/8/19 13:46:37
-------------------------------------------------
   Change Activity:
                   2020/8/19 13:46:37
-------------------------------------------------
"""
__author__ = 'Giyn'

import re
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # log information settings

with open('../data/billboard_data/adPositions.json') as file:
    billboard_positions_list_string = file.read()

billboard_positions_list = re.findall('\[\d{3}.\d{5,25}, \d{2}.\d{5,25}, \d{0,10}.0\]', billboard_positions_list_string)

billboard_positions_dict_list = []

temp = []
for i in billboard_positions_list:
    lng = float(re.findall('\d{3}.\d{5,25}', i)[0])
    lat = float(re.findall('\d{2}.\d{5,25}', i)[1])
    effect = float(re.findall('\d{0,10}.0\]', i)[0].strip(']'))
    if effect <= 70:
        continue
    if (effect > 70) & (effect <= 100):
        each_point_dict = {'lnglat': [lng, lat], 'level': 2}
    elif (effect > 100) & (effect <= 350):
        each_point_dict = {'lnglat': [lng, lat], 'level': 3}
    elif (effect > 350) & (effect <= 1000):
        each_point_dict = {'lnglat': [lng, lat], 'level': 4}
    else:
        each_point_dict = {'lnglat': [lng, lat], 'level': 5}
    billboard_positions_dict_list.append(each_point_dict)

with open('../data/billboard_data/billboard_dict_form.txt', 'w') as f:
    f.write(str(billboard_positions_dict_list))
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
