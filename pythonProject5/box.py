import re
import json
import sys
import time

import requests
from urllib.parse import quote
import xlsxwriter as xw
import os
C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; noticeList=%5B%22174%22%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1692579256,1692670832,1692751966,1692841262; NC5_newC5login=1; PHPSESSID=eto84kfqiql35fpetcaedussr3; CaseNotice=%E6%B4%BB%E5%8A%A8%E9%A5%B0%E5%93%81%E4%B8%80%E8%88%AC%E4%BC%9A%E5%9C%A830%E6%97%A5%E5%86%85%E6%9C%89%E5%BA%8F%E5%8F%91%E5%87%BA%EF%BC%8C%E5%A6%82%E6%9C%89%E9%97%AE%E9%A2%98%E5%8F%AF%E5%92%A8%E8%AF%A2%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%9C%8D%E3%80%82%20%20; NC5_uid=1000189316; NC5_isShowInspect=-1; _csrf=ef31974c96bf8f8cda74f9546539babbd8d43ae8ec6df9fb0bf128ad362262c9a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Tnltc1spYsUAgB6xoY7ly4uGTGbCJpat%22%3B%7D; NC5_crossAccessToken=undefined; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1692858886'
}
buffHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': '_ntes_nnid=a81ea4b883a087c51b7d8b9f7ce5c913,1690947339047; _ntes_nuid=a81ea4b883a087c51b7d8b9f7ce5c913; Device-Id=3ABe7sqJnoICsII0jmdm; timing_user_id=time_AJGrS6MTiv; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=45bFJy7EcYyXVpqRv0jFyz7fslEDJ36FLNisa4M5UtfbP_OdPs6CJlG62Bx1iTltDaX031c77WspWNtXLtQM_Lyu1l2LF1aRIxd2GImRHc5W0mpCKAYyt.3jmo3.lCHvmIOdf17hZEldO0xVzkC7XRVO.hoBi.2gDKih0tfW1v1iEDWWJnulp8oQA3necPkO7ymtq7Qe8gg1CFPLqlpIqnO7ZVKIFQH.aDOzsP4DPEvbG; S_INFO=1692752001|0|0&60##|13162147622; P_INFO=13162147622|1692752001|1|netease_buff|00&99|null&null&null#shh&null#10#0|&0||13162147622; remember_me=U1102355461|6P03qYmAbGdQNlIi37qpPGJUCazULUaE; session=1-GFY41TYmOC5NJ12WyuBdGodUIN6GRVl34JtGoLq3VgI42038039389; csrf_token=IjE1ZGVlMDI4MDdlNTJiNjFhZTk1ZDEzOGMyZDM0YzExMGEzMDQ3MjQi.F8bqoA.16WDm8Lc7GwIsdUmGZyskLqP1zc'
}
lowPrice = 10
highPrice = 500
lowSaleNumber = 300
fileName = '../jewelry1.xls'
def xw_toExcel(data,data1):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['饰品名称', 'c5自发价格','buff最低售价','buff最高求购','C5自发/buff','steam/buff']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        buffProfit =  (float(data[j]['price'])/float(data1[j]['buffSellPrice']) - 1) * 100
        steamProfit = float(data1[j]['buffSellPrice'])/(float(data1[j]['steamPrice']) * 0.86)
        insertData = [data[j]["name"], data[j]["price"],data1[j]["buffSellPrice"],data1[j]["buffBuyPrice"],buffProfit,steamProfit]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    worksheet1.set_column('A:A',50)
    worksheet1.set_column('B:F',20)
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
                if(float(price) < lowPrice):
                    continue
                if(float(price) > highPrice):
                    continue
                print(name + ": " + price)
                dic = {}
                dic['name'] = name
                dic['price'] = price
                dataList.append(dic)
        return dataList
    except:
        print('爬取失败')

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
                for item in itemList:
                    itemName = item['name']
                    itemSellPirce = item['sell_min_price']
                    itemBuyPrice = item['buy_max_price']
                    itemSteamPrice = item['goods_info']['steam_price_cny']
                    statTrak = 'StatTrak'  # 去除暗金
                    if (statTrak in itemName):
                        continue
                    souvenir = '纪念品'
                    if (souvenir in itemName):
                        continue
                    print(itemName + ': ' + itemSellPirce + '   ' + itemBuyPrice + '   ' + itemSteamPrice)
                    dic = {}
                    dic['buffSellPrice'] = itemSellPirce
                    dic['buffBuyPrice'] = itemBuyPrice
                    dic['steamPrice'] = itemSteamPrice
                    data1.append(dic)
            else:
                print("响应码错误" + response.status_code)
                sys.exit(1)
            time.sleep(3)
        return data1
    except:
        print('爬取失败')

def start(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
        print('删除旧文件')
    boxIDList = getAllBoxID()
    jewelryList = getJewelryList(boxIDList)
    dataList = getC5Price(jewelryList)
    print(len(dataList))
    dataList2 = getBuffAllPrice(dataList)
    print(len(dataList2))
    xw_toExcel(dataList, dataList2)
    print('成功写入')

start(fileName)


