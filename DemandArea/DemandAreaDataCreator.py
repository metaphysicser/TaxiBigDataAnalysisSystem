import pandas as pd
import numpy as np
from matplotlib.path import Path
from sklearn.cluster import DBSCAN
from CoordinateConverter import wgs84_to_gcj02
import json


def load_data(day, area):
    """
    读取并处理数据
    :param day: 哪一天
    :param area: 边界
    :return: 上车下车数据
    """
    data = pd.read_csv("operate_data/operate_his" + str(day) + ".csv")
    location = pd.read_csv("GuangzhouAdministrativeDistrict/" + area + ".txt", header=None)
    location = location.values.reshape(location.values.shape[1] // 2, 2)
    # 使用matplotlib中的path判断是否在区域内
    path = Path(location, closed=True)
    target_data = data[['GET_ON_LONGITUDE', 'GET_ON_LATITUDE', 'GET_OFF_LONGITUDE', 'GET_OFF_LATITUDE']].values
    data_filter = path.contains_points(target_data[:, :2])
    # 选出在区域内的所有数据
    target_data = target_data[data_filter == True]
    # 清除重复数据
    return np.unique(target_data, axis=0)


def cluster_frequency_area(all_location):
    """
    使用DBSCAN算法获取载客热点区
    :param all_location: 上车坐标
    :return: 标签
    """
    clu = DBSCAN(min_samples=20, eps=0.000425)
    return clu.fit_predict(all_location)


def frequent_area_to_json(list1, day):
    """
    载客热点数据保存为json
    :param list1: 上车数据
    :param day: 哪一天
    :return:
    """
    res = []
    for i in list1:
        d = {
            "lnglat": list(i)
        }
        res.append(d)
    with open("DemandAreaData/Passenger hot spots/day" + str(day) + ".json", 'w') as f:
        json.dump(res, f)


def circle_to_json(list1, day):
    """
        需求区域圆数据保存为json
        :param list1: 上车数据
        :param day: 哪一天
        :return:
        """
    res = []
    for i in list1:
        d = {
            "lnglat": list(i[0]),
            "mag": i[1]
        }
        res.append(d)
    with open("DemandAreaData/Demand area/day" + str(day) + '_circle.json', 'w') as f:
        json.dump(res, f)


def select_data(location, label, n):
    """
    选择SSE最大的n个簇
    :param location: 所有坐标点
    :param label: 标签
    :param n: 多少个簇
    :return: m*5的数组
    """
    def count_sse(x):
        circle = x.mean(0)
        sse = np.sqrt(np.sum(np.square(x - circle)))
        sse = np.sum(sse)
        return sse

    unique = np.unique(label)
    res = np.empty((len(unique,)))
    for i in range(len(unique)):
        X = location[label == unique[i]]
        res[i] = count_sse(X[:, :2])
    idx = np.argsort(-res)[:n]
    combine = []
    count = 1
    for i in idx:
        x_res = location[label == unique[i]]
        cxk = np.hstack((x_res, np.full((len(x_res), 1), count)))
        combine.append(cxk)
        count += 1
    return np.vstack(combine)

def get_clu(location_data):
    """
    计算圆心以及获得簇
    :param location_data: 上下车数据以及标签
    :return: 圆与簇的数据
    """
    def single_clu(single_data):
        circle = single_data.mean(0)
        r = np.max(np.sqrt(np.sum(np.square(single_data - circle))))
        return circle, r*0.95
    res0 = []
    res1 = []
    for i in np.unique(location_data[:, -1]):
        a = location_data[location_data[:, -1] == i]
        a_on = a[:, :2]
        a_off = a[:, 2:4]
        circle, r = single_clu(a_on)
        res0.append((circle, r))
        d = {
            "circle": circle,
            "off_clu": a_off
        }
        res1.append(d)
    return res0, res1


def judge_clu(x_off, center_d):
    """
    判断下车点处于哪个需求区
    :param x_off: 下车坐标
    :param center_d: 需求区范围
    :return: 属于需求区的圆心
    """
    res_d = np.inf
    res_circle = None
    for i in center_d:
        dist = np.linalg.norm(x_off - i[0])
        if dist < i[1] and dist < res_d:
            res_d = dist
            res_circle = i[0]
    return res_circle


def get_res(center_d, clu_d, n, day):
    """
    判断并保存为json文件
    :param center_d: 需求区所有点
    :param clu_d: 需求区范围
    :param n: 前n个主要坐标
    :param day: 哪一天
    :return:
    """
    result_main = []
    result_other = []
    count0 = 1
    for d in clu_d:
        count1 = 1
        collector = {}
        circle_point = str(d["circle"][0]) + "," + str(d["circle"][1])
        for each_point in d["off_clu"]:
            # res = {
            #     "name": str(count0) + "-" + str(count1),
            #     "line": [str(d["circle"][0]) + "," + str(d["circle"][1])]
            # }

            a = judge_clu(each_point, center_d)
            if a is None:
                add = str(each_point[0]) + "," + str(each_point[1])
                # res["line"].append(add)
                # collector.append(add)
                # res["other"].append({"lnglat": list(each_point)})
            else:
                add = str(a[0]) + "," + str(a[1])
                if add == circle_point:
                    continue
                # res["line"].append(add)
                # collector.append(add)
            if add not in collector:
                collector[add] = 1
            else:
                collector[add] += 1
                # res["line"].append(add)
                # result.append(res)
                # count1 += 1
        keys = list(collector.keys())
        values = np.array(list(collector.values()))
        idx_main = np.argsort(-values)[:n]
        for i in idx_main:
            res_m = {
                "name": str(count0) + "-" + str(count1),
                "line": [circle_point, keys[i]]
            }
            res_o = {
                "name": str(count0) + "-" + str(count1),
                "line": [circle_point, keys[-i-1]]
            }
            result_main.append(res_m)
            result_other.append(res_o)
            count1 += 1
        count0 += 1
    with open("DemandAreaData/Flow direction/main/day" + str(day) + ".json", "w") as f:
        json.dump(result_main, f)
    with open("DemandAreaData/Flow direction/other/day" + str(day) + ".json", "w") as f:
        json.dump(result_other, f)


if __name__ == '__main__':
    for i in range(1, 60):
        area = "Guangzhou"
        text_data = load_data(i, area)
        off = wgs84_to_gcj02(text_data[:, 2:4])
        text_data = np.hstack((wgs84_to_gcj02(text_data[:, :2]), off))
        y = cluster_frequency_area(text_data[:, :2])
        idx = np.argwhere(y == -1)
        text_data = np.delete(text_data, idx, axis=0)
        y = np.delete(y, idx)
        text_data = select_data(text_data, y, 44)
        frequent_area_to_json(text_data[:, :2], i)
        circle_data, clu_data = get_clu(text_data)
        circle_to_json(circle_data, i)
        get_res(circle_data, clu_data, 8, i)
        print("day %d successful" %i)