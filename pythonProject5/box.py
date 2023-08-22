import re
import json
import requests
from urllib.parse import quote
import xlsxwriter as xw
import os
C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; noticeList=%5B%22174%22%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1692172574,1692232776,1692342532,1692579256; NC5_newC5login=1; PHPSESSID=k0fjhp52p33799n9190nohilah; NC5_uid=1000034675; _csrf=f541e85145f3e481df5fc48fa59eb5acc9692219bbbee695d2ba127d3d6ee22fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22y3NfbUJBxrDDE3T-6qn5bT_k-fFuPWqz%22%3B%7D; NC5_crossAccessToken=undefined; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1692596042'
}
lowPrice = 10
highPrice = 2000
def getAllBoxID():
    urlPathStart = 'https://www.c5game.com/playground/case'
    try:
        url = urlPathStart
        response = requests.get(url, headers=C5Headers)
        if response.status_code == 200:
            boxIDList = []
            html = response.text
            id_pattern = '<a href="(.*?)" class="case-zone-group pointer relative"'
            boxUrlStr = json.dumps(re.findall(id_pattern, html)).encode('unicode-escape').decode('unicode-escape')
            boxUrlStr = boxUrlStr.strip('[')
            boxUrlStr = boxUrlStr.strip(']')
            boxUrlList = boxUrlStr.split(',')
            for item in boxUrlList:
                item = item.strip()
                item = item.strip('\"/playground/case/')
                item = item[0:3]
                boxIDList.append(item)
            boxIDList = list(dict.fromkeys(boxIDList))
            print(len(boxIDList))
            return boxIDList
        else:
            print('响应码错误: ' + response.status_code)

    except:
        print('爬取失败')

def getJewelryList(boxIDList):
    try:
        urlStart = 'https://www.c5game.com/napi/trade/c5-games/blind-box/v1/case-detail?case_id='
        jewelryList = []
        for boxID in boxIDList:
            url = urlStart + boxID
            response = requests.get(url, headers=C5Headers)
            if response.status_code == 200:
                jsonStr = json.loads(response.text)
                itemsList = jsonStr['data']['items']
                for items in itemsList:
                    items = itemsList[items]
                    for item in items:
                        itemName = item['name']
                        statTrak = 'StatTrak'  # 去除暗金
                        if (statTrak in itemName):
                            continue
                        souvenir = '纪念品'
                        if (souvenir in itemName):
                            continue
                        itemID = item['item_id']
                        jewelryList.append(itemID)
        print(len(jewelryList))
        return jewelryList
    except:
        print('爬取失败')

def getC5Price(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
    urlPathEnd = '&delivery=2&page=1&limit=10'
    try:
        data = []
        for jewelry in jewelryList:
            url = urlPathStart + jewelry + urlPathEnd
            response = requests.get(url, headers=C5Headers)
            jsonStr = json.loads(response.text)
            items = jsonStr['data']['list']
            if(len(items) != 0):
                item = items[0]
                name = item['itemName']
                price = item['cnyPrice']
                statTrak = 'StatTrak'   #去除暗金
                if(statTrak in name):
                    continue
                souvenir = '纪念品'
                if(souvenir in name):
                    continue
                if(float(price) < 10):
                    continue
                if(float(price) > 2000):
                    continue
                print(name + ": " + price)
                dic = {}
                dic['name'] = name
                dic['price'] = price
                data.append(dic)
        return data
    except:
        print('爬取失败')

#根据检索关键词列表获取价格列表（名称：价格）
def getC5AllPrice(nameList):
    urlPathStart = 'https://www.c5game.com/csgo?marketKeyword='
    try:
        jewelryList = []
        for name in nameList:
            url = urlPathStart + quote(name)
            response = requests.get(url, headers=C5Headers)
            if response.status_code == 200:
                html = response.text
                id_pattern = '<a href="/csgo' + '(.*?)/sell" target="_blank" class="mb20"'
                data_id = json.dumps(re.findall(id_pattern, html)).encode('unicode-escape').decode('unicode-escape')
                data_id = data_id.strip('[')
                data_id = data_id.strip(']')
                itemIDList = data_id.split(',')
                for item in itemIDList:
                    item = item.strip()
                    item = item.strip('\"')
                    item_id = item[1:].split('/')[0]
                    jewelryList.append(item_id)
        return jewelryList
    except:
        print('爬取失败')

boxIDList = getAllBoxID()
jewelryList = getJewelryList(boxIDList)
data = getC5Price(jewelryList)
print(len(data))