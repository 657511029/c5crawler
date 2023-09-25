import re
import json
import time
import pandas as pd
import requests
from urllib.parse import quote
import xlsxwriter as xw
import os

from fake_useragent import UserAgent


class csqaq:
    def __init__(self):
        self.lowPrice = 10
        self.highPrice = 300
        self.fileName = '../jewelry3.xls'
        self.C5Headers = {
            'User-Agent': UserAgent.random,
            # 'Cookie': 'aliyungf_tc=973ec8d0de2e40404ce0f1d2dc14bdb5699941578837a76c922e3d083aa02f74; alicfw=2842237974%7C2044019511%7C1328233706%7C1328232806; alicfw_gfver=v1.200309.1; NC5_crossAccessToken=undefined; NC5_deviceId=169413670065317710; NC5_version_id=new_web_grey; noticeList=%5B%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1694136705; _bl_uid=3zl6emUm93Ox3z94L5jv1C624z42; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1694136740'
        }
        self.csqaqHeaders = {
            'User-Agent': UserAgent().random,
            # 'Cookie': 'Hm_lvt_15af8706a9ce32d18f868b867df3203f=1694654085; Hm_lpvt_15af8706a9ce32d18f868b867df3203f=1694654085'
        }
        self.jewelryList = []
        self.nameList = []
        self.boxIDList = []
        self.dataList = []
        self.csqaqIDList = []
        self.buffAndUUMap = {}

    def xr_nameFormExcel(self):
        df = pd.read_excel(self.fileName, sheet_name='sheet1')
        listx = df['饰品名称'].tolist()
        listx = [str(i) for i in listx]
        return listx

    def xr_C5idFormExcel(self):
        df = pd.read_excel(self.fileName, sheet_name='sheet1')
        listx = df['C5饰品id'].tolist()
        listx = [str(i) for i in listx]
        return listx

    def xw_toExcel(self):  # xlsxwriter库储存数据到excel
        dataList = self.dataList
        buffAndUUMap = self.buffAndUUMap
        workbook = xw.Workbook(self.fileName)  # 创建工作簿
        worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
        worksheet1.activate()  # 激活表
        title = ['饰品名称', 'C5饰品id', 'C5自发/buff', 'C5自发/uu求购', 'buff在售/uu求购', 'steam/buff', 'c5自发价格',
                 'buff最低售价', 'buff最高求购', 'uu最低售价', 'uu最高求购']  # 设置表头
        worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
        i = 2  # 从第二行开始写入数据
        for j in range(len(dataList)):
            name = dataList[j]['name']
            C5Price = float(dataList[j]['price'])
            C5ID = dataList[j]['itemID']
            if (name not in buffAndUUMap.keys()):
                continue
            buffAndUUPrice = buffAndUUMap[name]
            buffSellPrice = buffAndUUPrice['buffSellPrice']
            buffBuyPrice = buffAndUUPrice['buffBuyPrice']
            steamPrice = buffAndUUPrice['steamPrice']
            uuSellPrice = buffAndUUPrice['uuSellPrice']
            uuBuyPrice = buffAndUUPrice['uuBuyPrice']
            if (buffSellPrice == 0.00):
                print('该饰品buff在售为0:  ' + name)
                continue
            if (uuBuyPrice == 0.00):
                print('该饰品uu求购为0:  ' + name)
                continue
            buffProfit = (0.99 * C5Price / buffSellPrice - 1) * 100
            steamProfit = buffSellPrice / (steamPrice * 0.86)
            uuBuyProfit = (0.99 * C5Price / uuBuyPrice - 1) * 100
            buffUU = (buffBuyPrice / uuBuyPrice - 1) * 100
            insertData = [name, C5ID, buffProfit, uuBuyProfit, buffUU, steamProfit, C5Price, buffSellPrice,
                          buffBuyPrice, uuSellPrice, uuBuyPrice]
            row = 'A' + str(i)
            worksheet1.write_row(row, insertData)
            i += 1
        worksheet1.set_column('A:A', 50)
        worksheet1.set_column('B:K', 20)
        workbook.close()  # 关闭表

    def getAllBoxID(self):
        urlPathStart = 'https://www.c5game.com/playground/case'
        try:
            url = urlPathStart
            response = requests.get(url, headers=self.C5Headers)
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

    def getJewelryList(self):
        try:
            boxIDList = self.boxIDList
            urlStart = 'https://www.c5game.com/napi/trade/c5-games/blind-box/v1/case-detail?case_id='
            jewelryList = []
            for boxID in boxIDList:
                url = urlStart + boxID
                response = requests.get(url, headers=self.C5Headers)
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
            return jewelryList

        except:
            print('获取C5饰品ID列表失败')

    def getC5Price(self):
        try:
            jewelryList = self.jewelryList
            urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
            urlPathEnd = '&delivery=2&page=1&limit=10'
            dataList = []
            for jewelry in jewelryList:
                url = urlPathStart + jewelry + urlPathEnd
                response = requests.get(url, headers=self.C5Headers)
                jsonStr = json.loads(response.text)
                items = jsonStr['data']['list']
                if (len(items) != 0):
                    item = items[0]
                    name = item['itemName']
                    price = item['cnyPrice']
                    if (float(price) < self.lowPrice):
                        continue
                    if (float(price) > self.highPrice):
                        continue
                    dic = {}
                    dic['name'] = name
                    dic['price'] = price
                    dic['itemID'] = jewelry
                    dataList.append(dic)
            return dataList
        except:
            print('获取C5饰品自发价格失败')


    def getCsqaqIDList(self):
        try:
            nameList = self.nameList
            urlPathStart = 'https://csqaq.com/proxies/api/v1/detail?result='
            csqaqIDList = []
            for name in nameList:
                jewelryName = quote(name).replace('%7C', '|')
                jewelryName = jewelryName.replace('%28', '(')
                jewelryName = jewelryName.replace('%29', ')')
                url = urlPathStart + jewelryName
                response = requests.get(url, headers=self.csqaqHeaders)
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
        except:
            print('获取csqaq饰品ID数据失败')

    def getBuffAndUUPriceList(self):
        try:
            csqaqIDList = self.csqaqIDList
            urlPathStart = 'https://csqaq.com/proxies/api/v1/info/good?id='
            buffAndUUMap = {}
            for csqaqID in csqaqIDList:
                itemID = csqaqID['id']
                itemName = csqaqID['name']
                if (itemID == '0'):
                    print('名称找不到    ' + itemName)
                    continue
                url = urlPathStart + itemID
                response = requests.get(url, headers=self.csqaqHeaders)
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
        except:
            print('获取csqaq饰品数据失败')

    def start(self):
        T1 = time.time()
        if os.path.exists(self.fileName):
            jewelryList = self.xr_C5idFormExcel(self)
            self.jewelryList = list(dict.fromkeys(jewelryList))
            nameList = self.xr_nameFormExcel(self)
            self.nameList = list(dict.fromkeys(nameList))
            os.remove(self.fileName)
            print('删除旧文件')
        else:
            self.boxIDList = self.getAllBoxID(self)
            self.jewelryList = self.getJewelryList(self)

        self.dataList = self.getC5Price(self)
        print('成功获取c5在售数据:      ' + str(len(self.dataList)))
        self.csqaqIDList = self.getCsqaqIDList(self)
        print('成功获取csqaqID数据:    ' + str(len(self.csqaqIDList)))
        self.buffAndUUMap = self.getBuffAndUUPriceList(self)
        print('成功获取buff和uu数据:   ' + str(len(self.buffAndUUMap)))
        self.xw_toExcel(self)
        print('写入成功')
        T2 = time.time()
        print('程序运行时间:%s分钟' % ((T2 - T1) / 60))


if __name__ == '__main__':
    cs = csqaq()
    cs.start()
