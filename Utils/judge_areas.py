# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 19:20:34 2020

@author: Giyn
"""

import pandas as pd
from matplotlib.path import Path


class JudgeAreas(object):
    """Judge if the points are within the administrative districts."""

    """
        All the districts(With Chinese translation) in Guangzhou.
    """
    districts = [['baiyun', '白云'], ['conghua', '从化'],
                 ['haizhu', '海珠'], ['huadu', '花都'],
                 ['huangpu', '黄埔'], ['liwan', '荔湾'],
                 ['nansha', '南沙'], ['panyu', '番禺'],
                 ['tianhe', '天河'], ['yuexiu', '越秀'],
                 ['zengcheng', '增城']]

    def judge_area(self, area, dataframe=None, lat=None, lon=None, array=None):
        """
        Judge if the latitude and longitude points are within the administrative district.
        Args:
            area: one of the 11 administrative districts in Guangzhou(type: string)
            dataframe: taxi_data
            lat: latitude(type: string)
            lon: longitude(type: string)
        Returns:
            is_in_area: whether in the area(type: array)
        """
        filename = '../data/DistrictsBoundary/{}.txt'.format(area)
        boundary = pd.read_csv(filename, header=None)
        boundary = boundary.values.reshape(boundary.values.shape[1] // 2, 2)

        path = Path(boundary, closed=True)

        if array is None:
            is_in_area = path.contains_points(dataframe[[lat, lon]])
        else:
            is_in_area = path.contains_points(array)

        return is_in_area


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
