import re
import json
import sys
import time
import pandas as pd
import requests
from urllib.parse import quote
import xlsxwriter as xw
import os

C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.5162 SLBChan/105',
    'Cookie': 'aliyungf_tc=973ec8d0de2e40404ce0f1d2dc14bdb5699941578837a76c922e3d083aa02f74; alicfw=2842237974%7C2044019511%7C1328233706%7C1328232806; alicfw_gfver=v1.200309.1; NC5_crossAccessToken=undefined; NC5_deviceId=169413670065317710; NC5_version_id=new_web_grey; noticeList=%5B%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1694136705; _bl_uid=3zl6emUm93Ox3z94L5jv1C624z42; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1694136740'
}

buffHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.5162 SLBChan/105',
    'Cookie': 'Device-Id=XR36oi8s6mnFAKPgtUJk; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=QZYSXDIOMWHuuBNoSwqaPkASw2cGqUh35t1DlQ4wWvgUSnZrSDeaKRKbd05rnTH7nFZky6lkn4ESYpoRhJD9zCrH3AQH6R1s6urHkZ2PiqcPu9maM5p0vcOX9HOcRaJV9bJtEURIr.e.7D_04o3HUeTexEGJBzNwrfZOKw30d_Nl_3qcOzQJWWkPbKCf4KMq9pQHStbqVXYOYZ5Dznr.2HRJpdliicAqXNZqDSQNSsVUh; S_INFO=1694137382|0|0&60##|17346697622; P_INFO=17346697622|1694137382|1|netease_buff|00&99|shh&1693202991&netease_buff#shh&null#10#0#0|&0||17346697622; remember_me=U1102096421|CQVYiNWOeKiX7bqRPBR9VAEATucibbCu; session=1-ghfmOYCGgANyLFI389WG5VMmtVq2IbN3zgZrAB0KCf6b2038314877; csrf_token=IjY5YWFkZTYxZjAyN2ZiNWFhZDg1ZmEwMzI3MWU4ZjIxZDdhODA2Yzki.F9wNxw.z159__gSYXKtKR-bQ6D-IRSNmBc'
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
lowPrice = 10
highPrice = 300
lowSaleNumber = 300
fileName = '../jewelry3.xls'

jewelryList = []
def xw_toExcel(data,data1,uuSellPriceList,uuBuyPriceList):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['饰品名称', 'C5饰品id','C5自发/buff','C5自发/uu求购','buff在售/uu求购','steam/buff','c5自发价格','buff最低售价','buff最高求购','uu最低售价','uu最高求购']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        if((data1[j]['buffSellPrice'] == '1.00') | (uuBuyPriceList[j] == 1.00)):
            continue
        buffProfit =  (0.99 * float(data[j]['price'])/float(data1[j]['buffSellPrice']) - 1) * 100
        steamProfit = float(data1[j]['buffSellPrice'])/(float(data1[j]['steamPrice']) * 0.86)
        uuBuyProfit =  (0.99 * float(data[j]['price'])/uuBuyPriceList[j] - 1) * 100
        buffUU = (float(data1[j]['buffSellPrice']) / uuBuyPriceList[j] - 1) * 100
        insertData = [data[j]["name"],data[j]['itemID'],buffProfit,uuBuyProfit,buffUU,steamProfit,data[j]["price"],data1[j]["buffSellPrice"],data1[j]["buffBuyPrice"],uuSellPriceList[j],uuBuyPriceList[j]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    worksheet1.set_column('A:A',50)
    worksheet1.set_column('B:K',20)
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
            print(name + ": " + price)
            dic = {}
            dic['name'] = name
            dic['price'] = price
            dic['itemID'] = jewelry
            dataList.append(dic)
    return dataList

def getBuffAllPrice(dataList):
    urlPathStart = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search='
    urlPathEnd = '&use_suggestion=0&_=1691975943061'
    try:
        data1 = []
        for data in dataList:
            name = data['name']
            name = quote(name).replace('%20', '+')
            name = name.replace('%28', '(')
            name = name.replace('%29', ')')
            url = urlPathStart + name + urlPathEnd
            response = requests.get(url, headers=buffHeaders)
            if response.status_code == 200:
                jsonStr = json.loads(response.text)
                itemList = jsonStr['data']['items']
                point = 0
                for item in itemList:
                    itemName = item['name']
                    itemSellPirce = item['sell_min_price']
                    itemBuyPrice = item['buy_max_price']
                    itemSteamPrice = item['goods_info']['steam_price_cny']
                    if(data['name'] != itemName):
                        continue
                    point = 1
                    print(itemName + ': ' + itemSellPirce + '   ' + itemBuyPrice + '   ' + itemSteamPrice)
                    dic = {}
                    dic['buffSellPrice'] = itemSellPirce
                    dic['buffBuyPrice'] = itemBuyPrice
                    dic['steamPrice'] = itemSteamPrice
                    data1.append(dic)
                if(point == 0):
                    dic = {}
                    dic['buffSellPrice'] = '1.00'
                    dic['buffBuyPrice'] = '1.00'
                    dic['steamPrice'] = '1.00'
                    data1.append(dic)
            else:
                print("响应码错误" + response.status_code)
            time.sleep(5)
        return data1
    except:
        print('爬取失败')

def getUUUserID():
    uuUrl = 'https://api.youpin898.com/api/user/Account/GetUserInfo'
    html = session.get(uuUrl, headers=uuHeaders)
    html.encoding = 'utf-8'
    jsonStr = json.loads(html.text)
    userID = jsonStr['Data']['UserId']
    return userID
def getUUJewelryList(dataList):
    uuUrl = 'https://api.youpin898.com/api/homepage/search/match'
    jewelryList = []
    for data in dataList:
        name = data['name']
        uuData = {
            'keyWords': name,
            'listType': '10'
        }
        html = session.post(uuUrl, headers=uuHeaders, json=uuData)
        jsonStr = json.loads(html.text)
        items = jsonStr['Data']['dataList']
        if (len(items) != 0):
            point = 0
            for item in items:
                jewelryID = item['templateId']
                jewelryName = item['commodityName']
                if (jewelryName != name):
                    continue
                point = 1
                jewelryList.append(jewelryID)
            if (point == 0):
                jewelryList.append(0)
        time.sleep(0.1)
    return jewelryList

def getUUSellPrice(jewelryList,userID):
    uuUrl = 'https://api.youpin898.com/api/homepage/v2/es/commodity/GetCsGoPagedList'
    uuSellPriceList = []
    for jewelry in jewelryList:
        if (jewelry == 0):
            uuSellPriceList.append('0.0')
            continue
        uuData = {
            'listSortType': 1,
            'listType': 10,
            'pageIndex': 1,
            'pageSize': 10,
            'sortType': 1,
            'stickers': {},
            'stickersIsSort': False,
            'templateId': jewelry,
            'userId': userID
        }
        html = session.post(uuUrl, headers=uuHeaders, json=uuData)
        jsonStr = json.loads(html.text)
        name = jsonStr['Data']['CommodityList'][0]['CommodityName']
        price = jsonStr['Data']['CommodityList'][0]['Price']
        print(name + ': ' + price)
        uuSellPriceList.append(price)
        time.sleep(0.1)
    return uuSellPriceList
def getUUBuyPrice(jewelryList):
    uuUrl = 'https://api.youpin898.com/api/youpin/commodity/purchase/find'
    uuBuyPriceList = []
    for jewelry in jewelryList:
        if (jewelry == 0):
            uuBuyPriceList.append(1.00)
            continue
        uuData = {
            'pageIndex': 1,
            'pageSize': 50,
            'templateId': jewelry
        }
        html = session.post(uuUrl, headers=uuHeaders, json=uuData)
        jsonStr = json.loads(html.text)
        price = 100.00
        priceList = jsonStr['data']['response']
        if(len(priceList) != 0):
            price = priceList[0]['unitPrice']
        print(priceList[0]['commodityName'] + ': ' + str(price/100.00))
        uuBuyPriceList.append(price/100.00)
        time.sleep(0.1)
    return uuBuyPriceList
def start(fileName):
    if os.path.exists(fileName):
        jewelryList = xr_formExcel(fileName)
        jewelryList = list(dict.fromkeys(jewelryList))
        os.remove(fileName)
        print('删除旧文件')
    else:
        boxIDList = getAllBoxID()
        jewelryList = getJewelryList(boxIDList)

    dataList = getC5Price(jewelryList)
    print(len(dataList))
    uuJewelryList = getUUJewelryList(dataList)
    print(len(uuJewelryList))
    userID = getUUUserID()
    uuSellPriceList = getUUSellPrice(uuJewelryList, userID)
    uuBuyPriceList = getUUBuyPrice(uuJewelryList)
    dataList2 = getBuffAllPrice(dataList)
    print(len(dataList2))
    xw_toExcel(dataList,dataList2,uuSellPriceList,uuBuyPriceList)
    print('成功写入')

start(fileName)


