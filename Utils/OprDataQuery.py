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

def getOprData(date) :

    '''To get all data from operate data with an offset on the date (2.1 + date).

    None

    :param date: The offset in day from 2.1.
    :type date: int
    :returns: The result position in shape of [data1, ..., dataN]
    :rtype: list
    '''

    res = []

    try:

        ms = sqldbs(host=str(env_dist['QGTAXI_ADD']), password=str(env_dist['QGTAXI_PWD']), user=str(env_dist['QGTAXI_ID']),
                port=int(env_dist['QGTAXI_PORT']))

        ms.executeSql("use operate_his;")

        des = ms.executeSql("select * from operate_his{0};".format(date + 1))

        for i in des :

            res.append(list(i))

        ms.close()

    except:

        pass

    return res
