import numpy as np


def wgs84_to_gcj02(array):
    """
    WGS84 to GCJ02
    Args:
        lng: longitude of WGS84
        lat: latitude of WGS84
    Returns:
        res: GCJ02 array
    """
    def converter(lng, lat):
        pi = 3.1415926535897932384626  # π
        a = 6378245.0  # 长半轴
        ee = 0.00669342162296594323  # 扁率
        def transformlat(lng, lat):
            ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
                  0.1 * lng * lat + 0.2 * np.sqrt(np.fabs(lng))
            ret += (20.0 * np.sin(6.0 * lng * pi) + 20.0 *
                    np.sin(2.0 * lng * pi)) * 2.0 / 3.0
            ret += (20.0 * np.sin(lat * pi) + 40.0 *
                    np.sin(lat / 3.0 * pi)) * 2.0 / 3.0
            ret += (160.0 * np.sin(lat / 12.0 * pi) + 320 *
                    np.sin(lat * pi / 30.0)) * 2.0 / 3.0
            return ret

        def transformlng(lng, lat):
            ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
                  0.1 * lng * lat + 0.1 * np.sqrt(np.fabs(lng))
            ret += (20.0 * np.sin(6.0 * lng * pi) + 20.0 *
                    np.sin(2.0 * lng * pi)) * 2.0 / 3.0
            ret += (20.0 * np.sin(lng * pi) + 40.0 *
                    np.sin(lng / 3.0 * pi)) * 2.0 / 3.0
            ret += (150.0 * np.sin(lng / 12.0 * pi) + 300.0 *
                    np.sin(lng / 30.0 * pi)) * 2.0 / 3.0
            return ret

        dlat = transformlat(lng - 105.0, lat - 35.0)
        dlng = transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * pi
        magic = np.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = np.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
        dlng = (dlng * 180.0) / (a / sqrtmagic * np.cos(radlat) * pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return mglng, mglat

    res = np.empty(array.shape)
    for i in range(res.shape[0]):
        res[i][0], res[i][1] = converter(array[i][0], array[i][1])
    return res
