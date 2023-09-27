import re
import json
import time
import pandas as pd
import requests
from urllib.parse import quote
import xlsxwriter as xw
import os

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class InitUUHeader:
    def __init__(self):
        self.loginUrl = "https://api.youpin898.com/api/user/Auth/PwdSignIn"
        self.loginHeaders = {
            'User-Agent': UserAgent().random,
            'Referer': 'https://www.youpin898.com/'
        }
        self.loginData = {
            'UserName': '',
            'UserPwd': '',
            'Code': '',
            'SessionId': ''
        }
        self.session = requests.Session()
        self.uuHeaders = self.init_uuHeader()
    def init_uuHeader(self):
        # session对象登录，记录登录的状态
        html = self.session.post(url=self.loginUrl, headers=self.loginHeaders, json=self.loginData)
        token = json.loads(html.text)['Data']['Token']
        # session对象的登录的状态去请求
        uuHeaders = {
            'User-Agent': UserAgent().random,
            'Authorization': 'Bearer ' + token
        }
        print('初始化uu账户信息成功')
        return uuHeaders


class C5game:
    def __init__(self,jewelryID,ip,point,seesion,uuHeaders):
        self.lowPrice = 10
        self.highPrice = 2000
        self.jewelryID = jewelryID
        self.point = point
        self.C5Headers = {
            'User-Agent': UserAgent().random,
        #     'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; NC5_uid=1000189316; aliyungf_tc=a609d9540c8fa6321d5d7d286c9c200a03f0462c8e28eb7d284cdbc7bb35efa5; alicfw=1032882838%7C2016287211%7C1328233530%7C1328232805; alicfw_gfver=v1.200309.1; NC5_crossAccessToken=undefined; noticeList=%5B%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1694142048,1694396720,1694482744,1694573477; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1694576615'
        }
        self.igxeHeaders = {
            'User-Agent': UserAgent().random,
        }

        self.proxies = {
            'http': 'http://{}'.format(ip),
            'https': 'http://{}'.format(ip),
        }
        self.session = seesion
        self.uuHeaders = uuHeaders

    def getC5Price(self):
        urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
        urlPathEnd = '&delivery=&page=1&limit=10'
        try:
            url = urlPathStart + self.jewelryID + urlPathEnd
            response = requests.get(url, headers=self.C5Headers, proxies=self.proxies)
            jsonStr = json.loads(response.text)
            items = jsonStr['data']['list']
            if (len(items) != 0):
                item = items[0]
                name = item['itemName']
                price = item['cnyPrice']
                statTrak = 'StatTrak'  # 去除暗金
                if (statTrak in name):
                    return
                souvenir = '纪念品'
                if (souvenir in name):
                    return
                misicBox = '花脸'
                if (misicBox in name):
                    return
                out = '★'
                if (out in name):
                    return
                out1 = '伽玛多普勒'
                if (out1 in name):
                    return
                if (float(price) < self.lowPrice):
                    return
                if (float(price) > self.highPrice):
                    return
                self.getUUJewelryList(name, price)

        except:
            print('获取c5饰品价格失败')

    # def compareC5BuyPrice(self,jewelryID, price):
    #     urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/purchase/v2/list?itemId='
    #     urlPathEnd = '&delivery=&styleId=&page=1&limit=10'
    #     url = urlPathStart + jewelryID + urlPathEnd
    #     response = requests.get(url, headers=C5Headers)
    #     jsonStr = json.loads(response.text)
    #     items = jsonStr['data']['list']
    #     if (len(items) != 0):
    #         item = items[0]
    #         name = item['itemName']
    #         buyPrice = item['cnyPrice']
    #         if (float(price) < buyPrice):
    #             print(name + ': ' + str(price) + '  ' + str(buyPrice))

    def getUUJewelryList(self,name, price):
        try:
            uuUrl = 'https://api.youpin898.com/api/homepage/search/match'
            uuData = {
                'keyWords': name,
                'listType': '10'
            }
            html = self.session.post(uuUrl, headers=self.uuHeaders, json=uuData, proxies=self.proxies)
            jsonStr = json.loads(html.text)
            items = jsonStr['Data']['dataList']
            for item in items:
                jewelryID = item['templateId']
                jewelryName = item['commodityName']
                if (jewelryName != name):
                    continue
                self.compareUUBuyPrice(jewelryName, price, jewelryID)
        except:
            print('获取uu饰品id失败')

    def compareUUBuyPrice(self,name, price, jewelryID):
        try:
            uuUrl = 'https://api.youpin898.com/api/youpin/commodity/purchase/find'
            uuData = {
                'pageIndex': 1,
                'pageSize': 50,
                'templateId': jewelryID
            }
            html = self.session.post(uuUrl, headers=self.uuHeaders, json=uuData, proxies=self.proxies)
            jsonStr = json.loads(html.text)
            uuBuyPrice = 1.00
            priceList = jsonStr['data']['response']
            if (len(priceList) != 0):
                uuBuyPrice = priceList[0]['unitPrice'] / 100.00
            if (float(price) < uuBuyPrice):
                print((str(self.point) + ':').ljust(6) + '与uu求购相比(c5在售:uu求购):'.ljust(26) + name + ': ' + str(
                    price) + '  ' + str(uuBuyPrice))
            self.compareIgxePrice(name, uuBuyPrice)
        except:
            print('比较c5在售和uu求购失败')

    def compareIgxePrice(self,name, uuBuyPrice):
        try:
            urlStart = 'https://www.igxe.cn/market/csgo?keyword='
            jewelryName = quote(name)
            url = urlStart + jewelryName
            html = requests.get(url, headers=self.igxeHeaders, proxies=self.proxies)
            soup = BeautifulSoup(html.text, "html.parser")
            data_list = soup.find_all(class_="list list")
            assert len(data_list) == 1, "unmatched data list"
            candidates = [
                a for a in data_list[0].find_all("a") if a.find(class_="name").text == name
            ]
            if len(candidates) == 1:
                priceStr = candidates[0].find(class_="price").text
                igxePrice = float(priceStr[1:])
                if ((igxePrice != 0.0) and (uuBuyPrice > igxePrice)):
                    print((str(self.point) + ':').ljust(6) + '与igxe在售相比(igxe在售:uu求购):'.ljust(
                        26) + name + ': ' + str(
                        igxePrice) + '  ' + str(uuBuyPrice))
        except:
            print('比较igxe在售和uu求购失败')

class C5gameList:
    def __init__(self,fileName):
        self.fileName = fileName
        self.jewelryList = []
    def xw_toExcel(self):  # xlsxwriter库储存数据到excel
        jewelryList = self.jewelryList
        workbook = xw.Workbook(self.fileName)  # 创建工作簿
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
        worksheet1.set_column('A:A', 20)
        workbook.close()  # 关闭表

    def xr_formExcel(self):
        df = pd.read_excel(self.fileName, sheet_name='sheet1')
        listx = df['C5饰品id'].tolist()
        listx = [str(i) for i in listx]
        listx = list(dict.fromkeys(listx))
        self.jewelryList = listx
        return listx

class ReadIp:
    def __init__(self,fileName):
        self.fileName = fileName

    def readIp(self):
        f = open(self.fileName, "r")
        lines = f.readlines()  # 读取全部内容
        return lines


if __name__ == '__main__':
    T1 = time.time()
    fileName = '../jewelry5.xls'
    ipFileName = 'ip_pool.txt'
    if os.path.exists(fileName):

        c5gameList = C5gameList(fileName)
        print('读取文件')
        jewelryList = c5gameList.xr_formExcel()
        print(len(jewelryList))
        os.remove(fileName)
        c5gameList.xw_toExcel()
        print('更新旧文件')
        print(len(jewelryList))


        point = 0
        readIp = ReadIp(ipFileName)
        ipList = readIp.readIp()
        print('获取ip列表: ' + str(len(ipList)))

        initUUHeader = InitUUHeader()
        session = initUUHeader.session
        uuHeaders = initUUHeader.uuHeaders

        for jewelryID in jewelryList:
            point = point + 1
            c5game = C5game(jewelryID, ipList[1], point,session,uuHeaders)
            c5game.getC5Price()
        T2 = time.time()
        print('程序运行时间:%s分钟' % ((T2 - T1) / 60))
    else:
        print('C5饰品id存储文件不存在')


