import re
import json
import sys
import time
from urllib.parse import quote

import pandas as pd
import requests
import xlsxwriter as xw
import os

from bs4 import BeautifulSoup

lowPrice = 10
highPrice = 2000
fileName = '../jewelry5.xls'
C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; NC5_uid=1000189316; aliyungf_tc=a609d9540c8fa6321d5d7d286c9c200a03f0462c8e28eb7d284cdbc7bb35efa5; alicfw=1032882838%7C2016287211%7C1328233530%7C1328232805; alicfw_gfver=v1.200309.1; NC5_crossAccessToken=undefined; noticeList=%5B%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1694142048,1694396720,1694482744,1694573477; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1694576615'
}
igxeHeaders = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
}
session = requests.Session()
loginUrl = "https://api.youpin898.com/api/user/Auth/PwdSignIn"

loginHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54',
    'Referer': 'https://www.youpin898.com/'
}
loginData = {
    'UserName': '',
    'UserPwd': '',
    'Code': '',
    'SessionId': ''
}
# session对象登录，记录登录的状态
html = session.post(url=loginUrl, headers=loginHeaders, json=loginData)
token = json.loads(html.text)['Data']['Token']
# session对象的登录的状态去请求
uuHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Authorization': 'Bearer ' + token
}

def xw_toExcel(jewelryList):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['C5饰品id']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(jewelryList)):
        insertData = [jewelryList[j]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    worksheet1.set_column('A:A',20)
    workbook.close()  # 关闭表
def xr_formExcel(fileName):
    df = pd.read_excel(fileName,sheet_name= 'sheet1')
    listx = df['C5饰品id'].tolist()
    listx = [str(i) for i in listx]
    return listx
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
                        misicBox = '花脸'
                        if (misicBox in itemName):
                            continue
                        out = '★'
                        if(out in itemName):
                            continue
                        itemID = item['item_id']
                        jewelryList.append(itemID)
        jewelryList = list(dict.fromkeys(jewelryList))
        return jewelryList
    except:
        print('爬取失败')

def getC5Price(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
    urlPathEnd = '&delivery=&page=1&limit=10'
    try:
        dataList = []
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
                misicBox = '花脸'
                if (misicBox in name):
                    continue
                out = '★'
                if (out in name):
                    continue
                out1 = '伽玛多普勒'
                if (out1 in name):
                    continue
                if(float(price) < lowPrice):
                    continue
                if(float(price) > highPrice):
                    continue
                print(name + ": " + price)
                dic = {}
                dic['name'] = name
                dic['jewelry'] = jewelry
                dic['price'] = price
                dataList.append(dic)
        return dataList
    except:
        print('爬取失败')
def getC5BuyPrice(dataList):
    map = {}
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/purchase/v2/list?itemId='
    urlPathEnd = '&delivery=&styleId=&page=1&limit=10'
    for data in dataList:
        jewelry = data['jewelry']
        url = urlPathStart + jewelry + urlPathEnd
        response = requests.get(url, headers=C5Headers)
        jsonStr = json.loads(response.text)
        items = jsonStr['data']['list']
        if(len(items) != 0):
            item = items[0]
            name = item['itemName']
            price = item['cnyPrice']
            map[name] = price
    return map

def getIgxePrice(dataList):
    urlStart = 'https://www.igxe.cn/market/csgo?keyword='
    map = {}
    # urls = []
    # for data in dataList:
    #     name = data['name']
    #     jewelryName = quote(name)
    #     url = urlStart + jewelryName
    #     urls.append(url)
    # req_list = (grequests.get(u,timeout=3) for u in urls)
    # for res in grequests.imap(req_list, size=size):
    for data in dataList:
        name = data['name']
        jewelryName = quote(name)
        url = urlStart + jewelryName
        html = requests.get(url,headers=igxeHeaders)
        soup = BeautifulSoup(html.text, "html.parser")
        data_list = soup.find_all(class_="list list")
        assert len(data_list) == 1, "unmatched data list"
        candidates = [
            a for a in data_list[0].find_all("a") if a.find(class_="name").text == name
        ]
        if len(candidates) == 1:
            priceStr = candidates[0].find(class_="price").text
            price = float(priceStr[1:])
            map[name] = price
    return map
# def getUUJewelryList(dataList):
#     uuUrl = 'https://api.youpin898.com/api/homepage/search/match'
#     jewelryList = []
#     uuDatas = []
#     for data in dataList:
#         name = data['name']
#         uuData = {
#             'keyWords': name,
#             'listType': '10'
#         }
#         uuDatas.append(uuData)
#     req_list = (grequests.post(uuUrl, headers=uuHeaders, json=uuData,timeout=3) for uuData in uuDatas)
#     i = -1
#     for res in grequests.imap(req_list, size=2):
#         i = i + 1
#         itemName = dataList[i]['name']
#         price = dataList[i]['price']
#         jsonStr = json.loads(res.content)
#         items = jsonStr['Data']['dataList']
#         for item in items:
#             jewelryID = item['templateId']
#             jewelryName = item['commodityName']
#             if(jewelryName != itemName):
#                 continue
#             map = {}
#             map['name'] = jewelryName
#             map['price'] = price
#             map['jewelryID'] = jewelryID
#             jewelryList.append(map)
#         time.sleep(0.1)
#     return jewelryList
#
# def getUUBuyPrice(jewelryList):
#     uuUrl = 'https://api.youpin898.com/api/youpin/commodity/purchase/find'
#     uuDatas = []
#     for jewelry in jewelryList:
#         jewelryID = jewelry['jewelryID']
#         uuData = {
#             'pageIndex': 1,
#             'pageSize': 50,
#             'templateId': jewelryID
#         }
#         uuDatas.append(uuData)
#     req_list = (grequests.post(uuUrl, headers=uuHeaders, json=uuData, timeout=3) for uuData in uuDatas)
#     i = -1
#     for res in grequests.imap(req_list, size=5):
#         i = i + 1
#         jsonStr = json.loads(res.content)
#         price = 100.00
#         priceList = jsonStr['data']['response']
#         if(len(priceList) != 0):
#             price = priceList[0]['unitPrice']
#         if (float(jewelryList[i]['price']) < price/100.00):
#             print(jewelryList[i]['name'] + ': ' + jewelryList[i]['price'] + '  ' + str(price/100.00))
#         time.sleep(0.1)
def compareC5(dataList,map):
    for data in dataList:
        name = data['name']
        sellPrice = data['price']
        buyPrice = 0.00
        if(name in map.keys()):
            buyPrice = map[name]
        if (float(sellPrice) < buyPrice):
            print(name + ': ' + str(sellPrice) + '  ' + str(buyPrice))

def compareIgxe(dataList,map):
    for data in dataList:
        name = data['name']
        UUBuyPrice = data['price']
        if((name not in map.keys()) or (map[name] == 0.00)):
            continue
        igxePrice = map[name]
        if (UUBuyPrice > igxePrice):
            print(name + ': ' + str(igxePrice) + '  ' + str(UUBuyPrice))
def getUUJewelryList(dataList):
    uuUrl = 'https://api.youpin898.com/api/homepage/search/match'
    jewelryList = []
    for data in dataList:
        price = data['price']
        name = data['name']
        uuData = {
            'keyWords': name,
            'listType': '10'
        }
        html = session.post(uuUrl, headers=uuHeaders, json=uuData)
        jsonStr = json.loads(html.text)
        items = jsonStr['Data']['dataList']
        for item in items:
            jewelryID = item['templateId']
            jewelryName = item['commodityName']
            if(jewelryName != name):
                continue
            # statTrak = 'StatTrak'  # 去除暗金
            # if (statTrak in jewelryName):
            #     continue
            # souvenir = '纪念品'
            # if (souvenir in jewelryName):
            #     continue
            # key = '钥匙'
            # if (key in jewelryName):
            #     continue
            map = {}
            map['name'] = name
            map['price'] = price
            map['jewelryID'] = jewelryID
            jewelryList.append(map)
        time.sleep(0.1)
    return jewelryList


def getUUBuyPrice(jewelryList):
    UUList = []
    uuUrl = 'https://api.youpin898.com/api/youpin/commodity/purchase/find'
    for jewelry in jewelryList:
        name = jewelry['name']
        jewelryID = jewelry['jewelryID']
        uuData = {
            'pageIndex': 1,
            'pageSize': 50,
            'templateId': jewelryID
        }
        html = session.post(uuUrl, headers=uuHeaders, json=uuData)
        jsonStr = json.loads(html.text)
        price = 100.00
        priceList = jsonStr['data']['response']
        if(len(priceList) != 0):
            price = priceList[0]['unitPrice']
            map = {}
            map['name'] = name
            map['price'] = price/100.00
            UUList.append(map)
        if (float(jewelry['price']) < price/100.00):
            print(name + ': ' + jewelry['price'] + '  ' + str(price/100.00))
        time.sleep(0.1)
    return UUList
def start():
    T1 = time.time()
    if os.path.exists(fileName):
        print('读取文件')
        jewelryList = xr_formExcel(fileName)
        print(len(jewelryList))
        jewelryList = list(dict.fromkeys(jewelryList))
        os.remove(fileName)
        xw_toExcel(jewelryList)
        print('更新旧文件')
    else:
        boxIDList = getAllBoxID()
        jewelryList = getJewelryList(boxIDList)

    print(len(jewelryList))
    dataList = getC5Price(jewelryList)
    print(len(dataList))
    # print('与c5求购相比(c5在售:c5求购)')
    # C5Map = getC5BuyPrice(dataList)
    # compareC5(dataList, C5Map)
    print('与uu求购相比(c5在售:uu求购)')
    uuJewelryList = getUUJewelryList(dataList)
    print(len(uuJewelryList))
    UUList = getUUBuyPrice(uuJewelryList)
    print('与igxe在售相比(igxe在售:uu求购)')
    igxeMap = getIgxePrice(dataList)
    print(len(igxeMap))
    compareIgxe(UUList, igxeMap)
    T2 = time.time()
    print('程序运行时间:%s分钟' % ((T2 - T1)/60))
start()