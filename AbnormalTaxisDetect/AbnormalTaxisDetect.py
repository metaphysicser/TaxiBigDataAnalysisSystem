import datetime
import numpy as np
import json

from Utils.OprDataQuery import *
from Utils.DataLoader import *

def abnormalTaxisDetect(date) :

    '''To get all data from operate data with an offset on the date (2.1 + date).

    None

    :param date: The offset in day from 2.1.
    :type date: int
    :returns: The result plateno in shape of [plateno1, ..., platenoN]
    :rtype: list
    '''

    oprData = np.array(getOprData(date))

    interval = []

    print(len(oprData))

    repeated, unique = divideRepeatTaxis(oprData)

    for i in range(len(unique)):
        begin = datetime.datetime.strptime(unique[i][7], "%Y-%m-%d %H:%M:%S")

        end = datetime.datetime.strptime(unique[i][8], "%Y-%m-%d %H:%M:%S")

        interval.append((end - begin).total_seconds())

    interval = np.array(interval)

    print((interval >= 60 * 60 * 10).sum())

    return unique[interval >= 60 * 60 * 10], repeated

def divideRepeatTaxis(oprData) :

    plateNo = set(oprData[:, 2])

    print(plateNo)

    reserve = [0] * len(oprData)

    for i in plateNo:

        temp = oprData[oprData[:, 2] == str(i)]

        if(len(temp) > 1) :

            for j in range(0, len(temp)) :

                if((temp[:, 7] == temp[j][7]).sum() > 1 or
                        (temp[:, 8] == temp[j][8]).sum() > 1) :

                    reserve = reserve + (oprData[:, 7] == temp[j][7]) + (oprData[:, 8] == temp[j][8])

                    break

    reserve = reserve > 0

    return oprData[reserve], oprData[reserve == False]

if __name__ == '__main__':

    for date in range(0, 14) :

        data0, data1 = abnormalTaxisDetect(date)

        exception = []

        plate0 = set(data0[:, 2])

        plate1 = set(data1[:, 2])

        for i in plate0 :

            exception.append({'plate' : i, 'type' : 'timeExceed'})

        for i in plate1 :

            exception.append({'plate' : i, 'type' : 'repeatedOrder'})

        print(exception)

        print(str(json.dumps(exception)))

        f = open("exceptionalCars{0}.json".format(date + 1), "w")

        f.write(str(json.dumps(exception)))

        f.close()
