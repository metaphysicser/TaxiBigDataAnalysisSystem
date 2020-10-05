import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.font_manager import FontProperties

myfont = FontProperties(fname = r'C:\Windows\Fonts\simhei.ttf',size = 14)

sns.set(font = myfont.get_name())

from Utils.GPSDataQuery import getGPSData
from Utils.judge_areas import JudgeAreas
from AdsCheckOut.adsDistribution import adsDistribution
from Utils.CoordinateConverter import wgs84_to_gcj02

pos = []

for i in range(1, 8) :

    pos.extend(getGPSData(i, np.random.randint(1000000), 20000, [0, 1000]))

pos = np.array(pos)

pos = wgs84_to_gcj02(pos)

pos = pos[JudgeAreas().judge_area('Guangzhou', array = pos[:, :2])]

ads = adsDistribution()

adPosition = ads.adsCheckOut(pos[:, :2])

plt.figure(figsize=(20, 20))

for i in JudgeAreas.districts :

    temp = pos[JudgeAreas().judge_area(i[0], array=pos[:, :2])]

    plt.scatter(temp[:, 0], temp[:, 1], alpha=0.2, label = i[1] + '区')

plt.scatter(adPosition[:, 0], adPosition[:, 1], alpha=0.2, c = "#ac0000", s = adPosition[:, 2])

plt.legend()

plt.show()

f = open("adPositions.json", "w")

f.write(str(json.dumps([list(i) for i in adPosition])))

f.close()
