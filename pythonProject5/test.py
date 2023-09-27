import json
import time
from urllib.parse import quote
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

nameList = ['M4A1 消音型 | 暴怒野兽 (久经沙场)',
            'M4A4 | 死寂空间 (略有磨损)',
            'AK-47 | 混沌点阵 (崭新出厂)',
            'M4A4 | 喧嚣杀戮 (久经沙场)',
            'USP | 黑色魅影 (久经沙场)',
            'M4A4 | 龙王 (略有磨损)',
            '格洛克 18 型 | 荒野反叛 (久经沙场)',
            'AK-47 | 阿努比斯军团 (略有磨损)',
            'AWP | 狮子之日 (久经沙场)',
            'AWP | 浮生如梦 (略有磨损)',
            'AK-47 | 复古浪潮 (久经沙场)',
            'M4A1 消音型 | 印花集 (久经沙场)',
            'AWP | 迷人眼 (久经沙场)',
            'AWP | 浮生如梦 (久经沙场)',
            'AWP | 冥界之河 (崭新出厂)',
            'USP 消音版 | 倒吊人 (久经沙场)',
            'AK-47 | 蓝色层压板 (久经沙场)',
            'AK-47 | 精英之作 (崭新出厂)',
            'AWP | 树蝰 (久经沙场)',
            '沙漠之鹰 | 阴谋者 (崭新出厂)',
            'M4A4 | 黑色魅影 (久经沙场)',
            'M4A4 | 活色生香 (久经沙场)',
            'M4A4 | 彼岸花 (略有磨损)',
            'M4A1 消音型 | 破碎铅秋 (久经沙场)',
            'AWP | 猫猫狗狗 (略有磨损)',
            'FN57 | 怒氓 (久经沙场)',
            '沙漠之鹰 | 机械工业 (久经沙场)',
            'MAC-10 | 霓虹骑士 (略有磨损)',
            'AK-47 | 蓝色层压板 (略有磨损)',
            'M4A1 消音型 | 氮化处理 (略有磨损)',
            '沙漠之鹰 | 机械工业 (崭新出厂)',
            '沙漠之鹰 | 机械工业 (略有磨损)',
            'AK-47 | 幻影破坏者 (略有磨损)',
            '沙漠之鹰 | 大佬龙 (久经沙场)',
            'P90 | 二西莫夫 (久经沙场)',
            'AK-47 | 幻影破坏者 (久经沙场)',
            '格洛克 18 型 | 子弹皇后 (略有磨损)',
            'MP9 | 星使 (久经沙场)',
            'AK-47 |翡翠细条纹 (久经沙场)'
            ]



C5Headers = {
    'User-Agent': UserAgent().random,
}
proxies = {
            'http': 'http://{}'.format('95.216.72.172:8088'),
            'https': 'http://{}'.format('95.216.72.172:8088'),
# 222.74.73.202:42055
# 61.216.156.222:60808
# 183.236.232.160:8080
}
def getC5Price():
    url = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId=1098192327056363520&delivery=2&page=1&limit=10'
    # url = 'https://www.baidu.com/'
    # url = 'http://httpbin.kdlapi.com/headers'
    # url = 'https://www.c5game.com/playground/case'
    # url = 'https://csqaq.com/proxies/api/v1/info/good?id=12389'
    resp = requests.get(url, proxies=proxies,headers=C5Headers)
    print(resp.text)
    if resp.status_code == 200:
        print('\033[31m可用\033[0m')
        # 可以的IP 写入文本以便后续使用
    else:
        print('不可用')

getC5Price()
# igxePriceList = getIgxeJewelryList(nameList)
# print(len(igxePriceList))
# for i in range(0, len(nameList)):
#     print(nameList[i] + ': ' + igxePriceList[i])