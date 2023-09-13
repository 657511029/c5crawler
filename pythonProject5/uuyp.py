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


fileName = '../jewelry5.xls'
C5Headers = {
    'User-Agent': UserAgent().random,
}
proxies = {
            'http': 'http://{}'.format('8.129.28.247:8888'),
            'https': 'https://{}'.format('8.129.28.247:8888'),
}
def xr_formExcel(fileName):
    df = pd.read_excel(fileName,sheet_name= 'sheet1')
    listx = df['C5饰品id'].tolist()
    listx = [str(i) for i in listx]
    return listx
def getC5Price(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
    urlPathEnd = '&delivery=&page=1&limit=10'
    for jewelry in jewelryList:
        url = urlPathStart + jewelry + urlPathEnd
        response = requests.get(url, headers=C5Headers,proxies=proxies)
        jsonStr = json.loads(response.text)
        items = jsonStr['data']['list']
        if (len(items) != 0):
            item = items[0]
            name = item['itemName']
            price = item['cnyPrice']
            statTrak = 'StatTrak'  # 去除暗金
            if (statTrak in name):
                continue
            souvenir = '纪念品'
            if (souvenir in name):
                continue
            misicBox = '花脸'
            if (misicBox in name):
                continue
            out = '★'
            if (out in name):
                continue
            out1 = '伽玛多普勒'
            if (out1 in name):
                continue
            print(name + ": " + price)

jewelryList = xr_formExcel(fileName)
jewelryList = list(dict.fromkeys(jewelryList))
print(len(jewelryList))
getC5Price(jewelryList)
# igxePriceList = getIgxeJewelryList(nameList)
# print(len(igxePriceList))
# for i in range(0, len(nameList)):
#     print(nameList[i] + ': ' + igxePriceList[i])