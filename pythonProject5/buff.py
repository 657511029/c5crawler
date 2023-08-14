import re
import json
import requests
from urllib.parse import quote
import time
import xlsxwriter as xw
import os
buffHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': '_ntes_nnid=a81ea4b883a087c51b7d8b9f7ce5c913,1690947339047; _ntes_nuid=a81ea4b883a087c51b7d8b9f7ce5c913; Device-Id=3ABe7sqJnoICsII0jmdm; timing_user_id=time_AJGrS6MTiv; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=mQB73GXqn5Rr1RCTx6rstVxK.YvXL2IJPJroImpZXKsjhziQhoRng7uR5aCArW7KHI0bkA6BBGotGJK0lK9pzlFUA75leAI.xCQ5uxv.f6ZGbvtnYONFKLkyvwkL7nfMvxiQsABT127QibC4PdnB0.4iLTwarL5DHNr9zHKPgPwEmp4n58tDIHwOrEkmrvPikPUZZlY4ov3skEmJaxMm4MiB14Yxe9fLIHiPohmHh2Mju; S_INFO=1691974203|0|0&60##|13162147622; P_INFO=13162147622|1691974203|1|netease_buff|00&99|null&null&null#shh&null#10#0|&0|null|13162147622; remember_me=U1102355461|2CftSTVqcxaY6rfX15EhBTdQMKiHLTUy; session=1-x8dFhs2WEYbz2qaXEKhtFPHUX1sKWmeipkyqodeo8kvr2038039389; csrf_token=ImUxMDc5OWU5Y2M4ZDM1ZmFmZTM4YTljZDQ4YTliYTllMTM2NDQ2NzUi.F7sYDw.NHcIDetLiYjyeWrU5MdjcSTwRHw'
}
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
            'AWP | 冥界之河 (久经沙场)',
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

def getBuffAllPrice(nameList):
    urlPathStart = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search='
    urlPathEnd = '&use_suggestion=0&_=1691975943061'
    try:
        count = 0
        for name in nameList:
            name = quote(name).replace('%20', '+')
            name = name.replace('%28', '(')
            name = name.replace('%29', ')')
            url = urlPathStart + name + urlPathEnd
            response = requests.get(url, headers=buffHeaders)
            if response.status_code == 200:
                jsonStr = json.loads(response.text)
                itemList = jsonStr['data']['items']
                for item in itemList:
                    itemName = item['name']
                    itemSellPirce = item['sell_min_price']
                    itemBuyPrice = item['buy_max_price']
                    statTrak = 'StatTrak'  # 去除暗金
                    if (statTrak in itemName):
                        continue
                    souvenir = '纪念品'
                    if (souvenir in itemName):
                        continue
                    print(itemName + ': ' + itemSellPirce + '   ' + itemBuyPrice)
                    count += 1
            time.sleep(1)
        print(count)
    except:
        print('爬取失败')
getBuffAllPrice(nameList)