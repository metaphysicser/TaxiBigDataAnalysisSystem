from Utils.MysqlDb import sqldbs
from os import environ as env_dist

def tempalted(self, args) :

    '''基本描述
    详细描述
    :param path: The path of the file to wrap
    :type path: str
    :param field_storage: The :class:`FileStorage` instance to wrap
    :type field_storage: FileStorage
    :param temporary: Whether or not to delete the file when the File instance is destructed
    :type temporary: bool
    :returns: A buffered writable file descriptor
    :rtype: BufferedFileStorage
    '''

def getGPSData(date, offset, N, speed) :

    '''To get top N positions (in Long.&Lat.) from GPS data with an offset on the date (2.1 + date).
    None
    :param date: The offset in day from 2.1.
    :type date: int
    :param offset: Offset in the database.
    :type offset: int
    :param N: The amount of the result.
    :type N: int
    :param speed: The speed limitation in shape of [low, high]
    :type speed: list
    :returns: The result position in shape of [[Long. , Lat.], ..., [Long. , Lat.]]
    :rtype: list
    '''

    res = []

    try:

        ms = sqldbs(host=str(env_dist['QGTAXI_ADD']), password=str(env_dist['QGTAXI_PWD']), user=str(env_dist['QGTAXI_ID']),
                port=int(env_dist['QGTAXI_PORT']))

        ms.executeSql("use taxilog;")

        des = ms.executeSql("select * from gpsdata{0} WHERE SPEED >= {3} and SPEED <= {4} limit {1}, {2};".format(date + 1, offset, N, speed[0], speed[1]))

        for i in des :

            res.append(list(i[3:6]))

        ms.close()

    except:

        pass

    return res

def getGPSDataByLicensePlate(date, LicensePlate) :

    '''To get top N positions (in Long.&Lat.) from GPS data with an offset on the date (2.1 + date).
    None
    :param date: The offset in day from 2.1.
    :type date: int
    :param offset: Offset in the database.
    :type offset: int
    :param N: The amount of the result.
    :type N: int
    :returns: The result position
    :rtype: list [[Long. , Lat.], ..., [Long. , Lat.]]
    '''

    res = []

    try:

        ms = sqldbs(host=str(env_dist['QGTAXI_ADD']), password=str(env_dist['QGTAXI_PWD']), user=str(env_dist['QGTAXI_ID']),
                port=int(env_dist['QGTAXI_PORT']))

        ms.executeSql("use taxilog;")

        cmd = "select * from gpsdata{0} where ".format(date)

        for i in range(0, len(LicensePlate)) :

            if(i) :
                cmd += "or "

            cmd += "LICENSEPLATENO = '{0}'".format(LicensePlate[i])

        print(cmd)

        des = ms.executeSql(cmd + ";")

        for i in des :

            res.append(list(i))

        ms.close()

    except:

        pass

    return res
