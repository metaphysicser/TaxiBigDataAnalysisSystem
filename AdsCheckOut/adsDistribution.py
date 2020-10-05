import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.font_manager import FontProperties

myfont = FontProperties(fname = r'C:\Windows\Fonts\simhei.ttf',size = 14)



sns.set(font = myfont.get_name())

from sklearn.cluster import DBSCAN

class adsDistribution(object) :

    def __init__(self) :

        pass

    def adsCheckOut(self, pos, eps = 0.0005, msp = 30) :

        '''To check out all the ads position
        None
        :param pos: The positions of taxis we got in shape of [[Long. , Lat.], ..., [Long. , Lat.]]
        :type pos: list
        :param eps: Argument eps for DBSCAN.
        :type eps: int
        :param msp: Argument min_samples for DBSCAN.
        :type msp: int
        :returns: All the ads positions in shape of [[Long. , Lat., size], ..., [Long. , Lat., size]]
        :rtype: str
        '''

        pos = np.array(pos)

        res = []

        dbcs = DBSCAN(eps = eps, min_samples = msp)

        classes = dbcs.fit_predict(pos[:, :2])

        for i in set(classes) :

            if(i != -1) :
                temp = pos[classes == i]

                res.append([temp[:, 0].mean(), temp[:, 1].mean(), len(temp)])

        return np.array(res)
