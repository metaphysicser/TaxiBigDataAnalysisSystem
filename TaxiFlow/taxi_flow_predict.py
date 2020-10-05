# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     taxi_flow_predict
   Description :
   Author :       Giyn
   date：          2020/8/13 16:26:34
-------------------------------------------------
   Change Activity:
                   2020/8/14 14:02:46
-------------------------------------------------
"""
__author__ = 'Giyn'


import logging
import math
import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from Utils.CoordinateConverter import wgs84_to_gcj02
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # log information settings

raw_data_path = '../data/operate_his/operate_his1.csv'
operate_his = pd.read_csv(raw_data_path, low_memory=False)

operate_his_on_points = operate_his.loc[:, ['EMPTY_MILE', 'LOAD_MILE', 'OPERATE_MONEY',
                                            'GET_ON_LONGITUDE', 'GET_ON_LATITUDE']]
operate_his_off_points = operate_his.loc[:, ['EMPTY_MILE', 'LOAD_MILE', 'OPERATE_MONEY',
                                             'GET_OFF_LONGITUDE', 'GET_OFF_LATITUDE']]

operate_his_on_points = operate_his_on_points[
    ~operate_his_on_points['GET_ON_LONGITUDE'].isin([0])]  # remove rows with longitude 0
operate_his_on_points = operate_his_on_points[
    ~operate_his_on_points['GET_ON_LATITUDE'].isin([0])]  # remove rows with latitude 0

operate_his_off_points = operate_his_off_points[
    ~operate_his_off_points['GET_OFF_LONGITUDE'].isin([0])]  # remove rows with longitude 0
operate_his_off_points = operate_his_off_points[
    ~operate_his_off_points['GET_OFF_LATITUDE'].isin([0])]  # remove rows with latitude 0

get_on_points = operate_his_on_points[0:70000].iloc[:, [3, 4]].values
get_off_points = operate_his_off_points[0:70000].iloc[:, [3, 4]].values

assert isinstance(operate_his_on_points[0:70000].iloc[:, [0, 1, 2]].values, object)
assert isinstance(operate_his_off_points[0:70000].iloc[:, [0, 1, 2]].values, object)

on_points_features = operate_his_on_points[0:70000].iloc[:, [0, 1, 2]].values
off_points_features = operate_his_off_points[0:70000].iloc[:, [0, 1, 2]].values

logging.info('Start to analyse and count!')

on_flow_data = []
# calculate the data volume of getting on and off the bus through [Get_On Point]
for i in range(len(get_on_points)):
    lng_on = round(get_on_points[i][0], 3)  # decrease the accuracy of longitude of [get_on point]
    lat_on = round(get_on_points[i][1], 3)  # decrease the accuracy of latitude of [get_on point]
    flow_on = operate_his.loc[
                  (operate_his['GET_ON_LONGITUDE'] >= (lng_on - 0.003)) &
                  (operate_his['GET_ON_LONGITUDE'] <= (lng_on + 0.003)) &
                  (operate_his['GET_ON_LATITUDE'] >= (lat_on - 0.003)) &
                  (operate_his['GET_ON_LATITUDE'] <= (lat_on + 0.003))].shape[0] + operate_his.loc[
                  (operate_his['GET_OFF_LONGITUDE'] >= (lng_on - 0.003)) &
                  (operate_his['GET_OFF_LONGITUDE'] <= (lng_on + 0.003)) &
                  (operate_his['GET_OFF_LATITUDE'] >= (lat_on - 0.003)) &
                  (operate_his['GET_OFF_LATITUDE'] <= (lat_on + 0.003))].shape[0]
    on_flow_data.append(flow_on)
logging.info('Successfully count the flow of get_on points!')

off_flow_data = []
# calculate the data volume of getting on and off the bus through [Get_Off Point]
for j in range(len(get_off_points)):
    lng_off = round(get_off_points[j][0], 3)  # decrease the accuracy of longitude of [get_on point]
    lat_off = round(get_off_points[j][1], 3)  # decrease the accuracy of latitude of [get_on point]
    flow_off = operate_his.loc[
                  (operate_his['GET_ON_LONGITUDE'] >= (lng_off - 0.003)) &
                  (operate_his['GET_ON_LONGITUDE'] <= (lng_off + 0.003)) &
                  (operate_his['GET_ON_LATITUDE'] >= (lat_off - 0.003)) &
                  (operate_his['GET_ON_LATITUDE'] <= (lat_off + 0.003))].shape[0] + operate_his.loc[
                  (operate_his['GET_OFF_LONGITUDE'] >= (lng_off - 0.003)) &
                  (operate_his['GET_OFF_LONGITUDE'] <= (lng_off + 0.003)) &
                  (operate_his['GET_OFF_LATITUDE'] >= (lat_off - 0.003)) &
                  (operate_his['GET_OFF_LATITUDE'] <= (lat_off + 0.003))].shape[0]
    off_flow_data.append(flow_off)
logging.info('Successfully count the flow of get_off points!')

on_points_trans = np.hstack((on_points_features, (wgs84_to_gcj02(get_on_points))))  # lat and lng conversion
on_points_flow = np.hstack((on_points_trans, np.array([on_flow_data]).reshape(70000, 1)))  # add flow column
off_points_trans = np.hstack((off_points_features, (wgs84_to_gcj02(get_off_points))))  # lat and lng conversion
off_points_flow = np.hstack((off_points_trans, np.array([off_flow_data]).reshape(70000, 1)))  # add flow column

all_points_flow = np.vstack((on_points_flow, off_points_flow))
logging.info('Successfully generate final data!')

np.random.seed(412)
X, y = np.split(all_points_flow, [5], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=412)
y_train = np.ravel(y_train)


"""The following is the RandomForestRegressor"""
forest = RandomForestRegressor(n_estimators=1000, criterion='mse', random_state=412, n_jobs=-1)
forest.fit(X_train, y_train)
logging.info('Successfully fit the model!')

# y_predict_RFG = forest.predict(X_test)
#
# MSE_of_RFG = mean_squared_error(y_test, y_predict_RFG)
# MAE_of_RFG = mean_absolute_error(y_test, y_predict_RFG)
# R_Square_of_RFG = r2_score(y_test, y_predict_RFG)

# print('RMSE of RFG: ' + str(math.sqrt(MSE_of_RFG)))
# print('MSE of RFG: ' + str(MSE_of_RFG))
# print('MAE of RFG: ' + str(MAE_of_RFG))
# print('R_Square of RFG: ' + str(R_Square_of_RFG))

for predicted_day in range(8, 15):
    logging.info('Start to predict taxi flow of one day!')
    raw_be_predicted_data_path = '../data/operate_his/operate_his{}.csv'.format(str(predicted_day))
    raw_be_predicted_data = pd.read_csv(raw_be_predicted_data_path)
    on_points_df = raw_be_predicted_data.iloc[:, [0, 1, 2, 3, 4]]
    off_points_df = raw_be_predicted_data.iloc[:, [0, 1, 2, 5, 6]]

    on_points_df = on_points_df[~on_points_df['GET_ON_LONGITUDE'].isin([0])]  # remove rows with longitude 0
    on_points_df = on_points_df[~on_points_df['GET_ON_LATITUDE'].isin([0])]  # remove rows with latitude 0
    off_points_df = off_points_df[~off_points_df['GET_OFF_LONGITUDE'].isin([0])]  # remove rows with longitude 0
    off_points_df = off_points_df[~off_points_df['GET_OFF_LATITUDE'].isin([0])]  # remove rows with latitude 0

    get_on_points_predicted = on_points_df[0:50000].iloc[:, [3, 4]].values
    get_off_points_predicted = off_points_df[0:50000].iloc[:, [3, 4]].values

    on_points_predicted_features = on_points_df[0:50000].iloc[:, [0, 1, 2]].values
    off_points_predicted_features = on_points_df[0:50000].iloc[:, [0, 1, 2]].values

    # lat and lng conversion
    on_points_dealed_data = np.hstack((on_points_predicted_features, (wgs84_to_gcj02(get_on_points_predicted))))
    # lat and lng conversion
    off_points_dealed_data = np.hstack((off_points_predicted_features, (wgs84_to_gcj02(get_off_points_predicted))))

    on_points_data = on_points_dealed_data[0:50000]
    off_points_data = off_points_dealed_data[0:50000]

    all_points_data = np.vstack((on_points_data, off_points_data))

    raw_result = forest.predict(all_points_data)
    predicted_flow = raw_result.reshape(100000, 1)

    predicted_points = np.split(all_points_data, [3], axis=1)[1]

    predicted_data = np.hstack((predicted_points, predicted_flow))

    predicted_data_list = []
    for each in predicted_data:
        each_data = {'lng': each[0], 'lat': each[1], 'count': each[2]}
        predicted_data_list.append(each_data)

    save_path = '../data/flow_data_predicted/flow_data_predicted_{}.txt'.format(str(predicted_day))
    with open(save_path, 'w') as file:
        file.write(str(predicted_data_list))
    logging.info('Successfully save data!')


"""The following is the GradientBoostingRegressor"""
# gbdt = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,
#                                  max_depth=1, random_state=0, loss='ls')
# gbdt.fit(X_train, y_train)
# logging.info('Successfully fit the model!')
#
# y_predict_GBDT = gbdt.predict(X_test)
#
# MSE_of_GBDT = mean_squared_error(y_test, y_predict_GBDT)
# MAE_of_GBDT = mean_absolute_error(y_test, y_predict_GBDT)
# R_Square_of_GBDT = r2_score(y_test, y_predict_GBDT)
#
# print('RMSE of GBDT: ' + str(math.sqrt(MSE_of_GBDT)))
# print('MSE of GBDT: ' + str(MSE_of_GBDT))
# print('MAE of GBDT: ' + str(MAE_of_GBDT))
# print('R_Square of GBDT: ' + str(R_Square_of_GBDT))


"""The following is the XGBoost"""
# XGB = xgb.XGBRegressor(seed=412)
#
# XGB.fit(X_train, y_train, verbose=True)
#
# y_predict_XGB = XGB.predict(X_test)
#
# MSE_of_XGB = mean_squared_error(y_test, y_predict_XGB)
# MAE_of_XGB = mean_absolute_error(y_test, y_predict_XGB)
# R_Square_of_XGB = r2_score(y_test, y_predict_XGB)
#
# print('RMSE of XGB: ' + str(math.sqrt(MSE_of_XGB)))
# print('MSE of XGB: ' + str(MSE_of_XGB))
# print('MAE of XGB: ' + str(MAE_of_XGB))
# print('R_Square of XGB: ' + str(R_Square_of_XGB))


"""The following is the lightgbm"""
# LGB = lgb.LGBMRegressor(objective='regression', max_depth=5, num_leaves=25, learning_rate=0.007, n_estimators=1000,
#                         min_child_samples=80, subsample=0.8, colsample_bytree=1, reg_alpha=0, reg_lambda=0,
#                         random_state=np.random.randint(10e6))
#
# LGB.fit(X_train, y_train, verbose=False)
#
# y_predict_LGB = LGB.predict(X_test)
#
# MSE_of_LGB = mean_squared_error(y_test, y_predict_LGB)
# MAE_of_LGB = mean_absolute_error(y_test, y_predict_LGB)
# R_Square_of_LGB = r2_score(y_test, y_predict_LGB)
#
# print('RMSE of LGB: ' + str(math.sqrt(MSE_of_LGB)))
# print('MSE of LGB: ' + str(MSE_of_LGB))
# print('MAE of LGB: ' + str(MAE_of_LGB))
# print('R_Square of LGB: ' + str(R_Square_of_LGB))


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
