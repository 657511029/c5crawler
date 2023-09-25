import re
import json
import time
import pandas as pd
import requests
from urllib.parse import quote
import xlsxwriter as xw
import os

from fake_useragent import UserAgent

lowPrice = 10
highPrice = 300
fileName = '../jewelry3.xls'
C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.5162 SLBChan/105',
    'Cookie': 'aliyungf_tc=973ec8d0de2e40404ce0f1d2dc14bdb5699941578837a76c922e3d083aa02f74; alicfw=2842237974%7C2044019511%7C1328233706%7C1328232806; alicfw_gfver=v1.200309.1; NC5_crossAccessToken=undefined; NC5_deviceId=169413670065317710; NC5_version_id=new_web_grey; noticeList=%5B%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1694136705; _bl_uid=3zl6emUm93Ox3z94L5jv1C624z42; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1694136740'
}
csqaqHeaders = {
    'User-Agent': UserAgent().random,
    # 'Cookie': 'Hm_lvt_15af8706a9ce32d18f868b867df3203f=1694654085; Hm_lpvt_15af8706a9ce32d18f868b867df3203f=1694654085'
}

jewelryList = []
nameList = []
def xr_nameFormExcel(fileName):
    df = pd.read_excel(fileName,sheet_name= 'sheet1')
    listx = df['饰品名称'].tolist()
    listx = [str(i) for i in listx]
    return listx
def xr_C5idFormExcel(fileName):
    df = pd.read_excel(fileName,sheet_name= 'sheet1')
    listx = df['C5饰品id'].tolist()
    listx = [str(i) for i in listx]
    return listx
def xw_toExcel(fileName,dataList,buffAndUUMap):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['饰品名称', 'C5饰品id','C5自发/buff','C5自发/uu求购','buff在售/uu求购','steam/buff','c5自发价格','buff最低售价','buff最高求购','uu最低售价','uu最高求购']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(dataList)):
        name = dataList[j]['name']
        C5Price = float(dataList[j]['price'])
        C5ID = dataList[j]['itemID']
        if(name not in buffAndUUMap.keys()):
            continue
        buffAndUUPrice = buffAndUUMap[name]
        buffSellPrice = buffAndUUPrice['buffSellPrice']
        buffBuyPrice = buffAndUUPrice['buffBuyPrice']
        steamPrice = buffAndUUPrice['steamPrice']
        uuSellPrice = buffAndUUPrice['uuSellPrice']
        uuBuyPrice = buffAndUUPrice['uuBuyPrice']
        if(buffSellPrice == 0.00):
            print('该饰品buff在售为0:  ' + name)
            continue
        if (uuBuyPrice == 0.00):
            print('该饰品uu求购为0:  ' + name)
            continue
        buffProfit =  (0.99 * C5Price/buffSellPrice - 1) * 100
        steamProfit = buffSellPrice/(steamPrice * 0.86)
        uuBuyProfit =  (0.99 * C5Price/uuBuyPrice - 1) * 100
        buffUU = (buffBuyPrice / uuBuyPrice - 1) * 100
        insertData = [name,C5ID,buffProfit,uuBuyProfit,buffUU,steamProfit,C5Price,buffSellPrice,buffBuyPrice,uuSellPrice,uuBuyPrice]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    worksheet1.set_column('A:A',50)
    worksheet1.set_column('B:K',20)
    workbook.close()  # 关闭表

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
                        misicBox = '花脸'
                        if (misicBox in itemName):
                            continue
                        itemID = item['item_id']
                        jewelryList.append(itemID)
        jewelryList = list(dict.fromkeys(jewelryList))
        print(len(jewelryList))
        return jewelryList
    except:
        print('爬取失败')

def getC5Price(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
    urlPathEnd = '&delivery=2&page=1&limit=10'
    dataList = []
    for jewelry in jewelryList:
        url = urlPathStart + jewelry + urlPathEnd
        response = requests.get(url, headers=C5Headers)
        jsonStr = json.loads(response.text)
        items = jsonStr['data']['list']
        if (len(items) != 0):
            item = items[0]
            name = item['itemName']
            price = item['cnyPrice']
            if (float(price) < lowPrice):
                continue
            if (float(price) > highPrice):
                continue
            dic = {}
            dic['name'] = name
            dic['price'] = price
            dic['itemID'] = jewelry
            dataList.append(dic)
    return dataList
def getCsqaqIDList(nameList):
    urlPathStart = 'https://csqaq.com/proxies/api/v1/detail?result='
    csqaqIDList = []
    for name in nameList:
        jewelryName = quote(name).replace('%7C', '|')
        jewelryName = jewelryName.replace('%28', '(')
        jewelryName = jewelryName.replace('%29', ')')
        url = urlPathStart + jewelryName
        response = requests.get(url, headers=csqaqHeaders)
        if response.status_code == 200:
            jsonStr = json.loads(response.text)
            itemList = jsonStr['data']
            point = 0
            for item in itemList:
                itemName = item['value']
                itemId = item['id']
                if (name != itemName):
                    continue
                point = 1
                map = {}
                map['name'] = name
                map['id'] = itemId
                csqaqIDList.append(map)
            if (point == 0):
                map = {}
                map['name'] = name
                map['id'] = '0'
                csqaqIDList.append(map)
        else:
            print("响应码错误" + str(response.status_code))
    return csqaqIDList
def getBuffAndUUPriceList(csqaqIDList):
    urlPathStart = 'https://csqaq.com/proxies/api/v1/info/good?id='
    buffAndUUMap = {}
    for csqaqID in csqaqIDList:
        itemID = csqaqID['id']
        itemName = csqaqID['name']
        if(itemID == '0'):
            print('名称找不到    ' + itemName)
            continue
        url = urlPathStart + itemID
        response = requests.get(url, headers=csqaqHeaders)
        if response.status_code == 200:
            jsonStr = json.loads(response.text)
            itemInfo = jsonStr['data']['goods_info']
            buffSellPrice = itemInfo['buff_sell_price']
            buffBuyPrice = itemInfo['buff_buy_price']
            steamPrice = itemInfo['steam_sell_price']
            uuSellPrice = itemInfo['yyyp_sell_price']
            uuBuyPrice = itemInfo['yyyp_buy_price']
            map = {}
            map['buffSellPrice'] = buffSellPrice
            map['buffBuyPrice'] = buffBuyPrice
            map['steamPrice'] = steamPrice
            map['uuSellPrice'] = uuSellPrice
            map['uuBuyPrice'] = uuBuyPrice
            print('获取数据成功:   ' + itemName)
            buffAndUUMap[itemName] = map
        else:
            print("响应码错误" + str(response.status_code) + '  ' + csqaqID['name'])
        time.sleep(2)
    return buffAndUUMap
def start():
    T1 = time.time()
    if os.path.exists(fileName):
        jewelryList = xr_C5idFormExcel(fileName)
        jewelryList = list(dict.fromkeys(jewelryList))
        nameList = xr_nameFormExcel(fileName)
        nameList = list(dict.fromkeys(nameList))
        os.remove(fileName)
        print('删除旧文件')
    else:
        boxIDList = getAllBoxID()
        jewelryList = getJewelryList(boxIDList)


    dataList = getC5Price(jewelryList)
    print('成功获取c5在售数据:      ' + str(len(dataList)))
    csqaqIDList = getCsqaqIDList(nameList)
    print('成功获取csqaqID数据:    ' + str(len(csqaqIDList)))
    buffAndUUMap = getBuffAndUUPriceList(csqaqIDList)
    print('成功获取buff和uu数据:   ' + str(len(buffAndUUMap)))
    xw_toExcel(fileName,dataList,buffAndUUMap)
    print('写入成功')
    T2 = time.time()
    print('程序运行时间:%s分钟' % ((T2 - T1) / 60))
start()