
import json
import re
import sys
import time
from urllib.parse import quote

import requests
import xlsxwriter as xw
import os

keywordList = [
    'weapon_ak47',
    'weapon_awp',
    'weapon_m4a1_silencer',
    'weapon_m4a1',
    'weapon_sg556',
    'weapon_deagle',
    'weapon_usp_silencer',
    'weapon_glock',
    'weapon_p90'
]
qualityList = ['崭新出厂','略有磨损','久经沙场']
C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; NC5_uid=1000189316; NC5_crossAccessToken=undefined; noticeList=%5B%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1693550674,1693790900,1693986709,1694050560; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1694050560; CaseNotice=%E6%B4%BB%E5%8A%A8%E9%A5%B0%E5%93%81%E4%B8%80%E8%88%AC%E4%BC%9A%E5%9C%A830%E6%97%A5%E5%86%85%E6%9C%89%E5%BA%8F%E5%8F%91%E5%87%BA%EF%BC%8C%E5%A6%82%E6%9C%89%E9%97%AE%E9%A2%98%E5%8F%AF%E5%92%A8%E8%AF%A2%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%9C%8D%E3%80%82%20%20'
}

buffHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': '_ntes_nnid=a81ea4b883a087c51b7d8b9f7ce5c913,1690947339047; _ntes_nuid=a81ea4b883a087c51b7d8b9f7ce5c913; Device-Id=3ABe7sqJnoICsII0jmdm; timing_user_id=time_AJGrS6MTiv; Locale-Supported=zh-Hans; game=csgo; AQ_HD=1; YD_SC_SID=624E8F2F08404604A8ECC0A9A7594388; AQ_REQ_FROM=webzj; NTES_YD_SESS=dBpdmWLRcSGCvBLmxymnQiz1uDOnnJKj6pZgLdVoTmJuqC5iqgFBt6PFs.7EZ_6mYLWGAEyRRzg4zpmWcmrVCcXhE6sc0ELel7isPlQeNyozGQ4Bv2MXm8AUQDA86BN9Ql5iJERSwf6i5G7knOBRWek58SD.Z8sKYQjtjUoR2iJO1E1iNfaxaD8mwbUFM00mc4amJK7NJPBaxMW2w6qGY0kRwkvl0rN8LY5ngqdYqf9uP; S_INFO=1693206419|0|0&60##|13162147622; P_INFO=13162147622|1693206419|1|netease_buff|00&99|null&null&null#shh&null#10#0|&0|null|13162147622; remember_me=U1102355461|F8sxxahVWHiaaHcRtzmqH4i7KbjmPoDu; session=1-9vKV3-1blP5LYUmdEDJMMUNrlIIEJmgOIJJ_DXeN70vX2038039389; csrf_token=ImE2OGI3ZDViMTI1ZjcwNGZjODM3ZjQ2ODFiZTMzOWE5MDE0Y2EzNTQi.F83ZPw.P_pUG0eBtFdQ1Qo2wEbBwhoDn-E'
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

lowPrice = 200
highPrice = 1000
lowSaleNumber = 300
fileName = '../jewelry4.xls'

jewelryList = []
def xw_toExcel(buffList,dataList,uuSellPriceList, uuBuyPriceList):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['饰品名称','buff最低售价','buff最高求购','C5自发/buff','C5自发/uu求购','buff在售/uu求购','c5自发价格','uu最低售价','uu最高求购', 'C5饰品id']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(buffList)):
        buffProfit = (0.99 * float(dataList[j]['price']) / float(buffList[j]['buffSellPrice']) - 1) * 100
        uuBuyProfit = (0.99 * float(dataList[j]['price']) / uuBuyPriceList[j] - 1) * 100
        buffUU = (float(buffList[j]['buffSellPrice']) / uuBuyPriceList[j] - 1) * 100
        insertData = [buffList[j]["name"],float(buffList[j]["buffSellPrice"]),float(buffList[j]["buffBuyPrice"]),buffProfit,uuBuyProfit,buffUU,float(dataList[j]["price"]),float(uuSellPriceList[j]),uuBuyPriceList[j],dataList[j]['itemID']]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    worksheet1.set_column('A:A',50)
    worksheet1.set_column('B:J',20)
    workbook.close()  # 关闭表

def getJewelryList():
    buffList = []
    for keyword in keywordList:
        url = 'https://buff.163.com/api/market/goods?game=csgo&category=' + keyword + '&min_price=' + str(lowPrice) + '&max_price=' + str(highPrice) + '&quality=normal&use_suggestion=0&_=1693817331414'
        response = requests.get(url, headers=buffHeaders)
        if response.status_code == 200:
            jsonStr = json.loads(response.text)
            items = jsonStr['data']['items']
            pageNum = jsonStr['data']['total_page']
            if(len(items) == 0):
                continue
            for item in items:
                itemName = item['name']
                if ((qualityList[0] not in itemName) & (qualityList[1] not in itemName) & (qualityList[2] not in itemName)):
                    continue
                sellPrice = item['sell_min_price']
                buyPrice = item['buy_max_price']
                map = {}
                map['name'] = itemName
                map['buffSellPrice'] = sellPrice
                map['buffBuyPrice'] = buyPrice
                print(itemName)

                buffList.append(map)
            if(pageNum > 1):
                for i in range(1, pageNum):
                    url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=' + str(i + 1) + '&category=' + keyword + '&min_price=' + str(lowPrice) + '&max_price=' + str(highPrice) + '&quality=normal&use_suggestion=0&_=1693817331414'
                    response = requests.get(url, headers=buffHeaders)
                    if response.status_code == 200:
                        jsonStr = json.loads(response.text)
                        items = jsonStr['data']['items']
                        if(i > jsonStr['data']['total_page'] - 1):
                            break
                        for item in items:
                            itemName = item['name']
                            if ((qualityList[0] not in itemName) & (qualityList[1] not in itemName) & (
                                    qualityList[2] not in itemName)):
                                continue
                            sellPrice = item['sell_min_price']
                            buyPrice = item['buy_max_price']
                            map = {}
                            map['name'] = itemName
                            map['buffSellPrice'] = sellPrice
                            map['buffBuyPrice'] = buyPrice
                            print(itemName)
                            buffList.append(map)
    print(len(buffList))
    return buffList
    # jewelryList = list(dict.fromkeys(jewelryList))
    # print(len(jewelryList))
    # return jewelryList

def getC5JewelryListByName(jewelryList):
    idList = []
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/item-search/v1/list?appId=730&keyword='
    for jewelry in jewelryList:
        name = jewelry['name']
        name = quote(name)
        name = name.replace('%20', '+')
        name = name.replace('%28', '(')
        name = name.replace('%29', ')')
        url = urlPathStart + name
        response = requests.get(url, headers=C5Headers)
        if response.status_code == 200:
            jsonStr = json.loads(response.text)
            items = jsonStr['data']['list']
            for item in items:
                itemName = item['itemName']
                if (itemName != jewelry['name']):
                    continue
                map = {}
                map['itemId'] = item['itemId']
                map['itemName'] = itemName
                idList.append(map)
    print(len(idList))
    return idList

def getC5Price(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
    urlPathEnd = '&delivery=2&page=1&limit=10'
    dataList = []
    for jewelry in jewelryList:
        itemId = jewelry['itemId']
        url = urlPathStart + itemId + urlPathEnd
        response = requests.get(url, headers=C5Headers)
        jsonStr = json.loads(response.text)
        items = jsonStr['data']['list']
        if (len(items) != 0):
            item = items[0]
            name = item['itemName']
            price = item['cnyPrice']
            print(name + ": " + price)
            dic = {}
            dic['name'] = name
            dic['price'] = price
            dic['itemID'] = itemId
            dataList.append(dic)
        else:
            dic = {}
            dic['name'] = jewelry['itemName']
            dic['price'] = '0.0'
            dic['itemID'] = itemId
            dataList.append(dic)
    return dataList
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
        if(len(items) != 0):
            point = 0
            for item in items:
                jewelryID = item['templateId']
                jewelryName = item['commodityName']
                if (jewelryName != name):
                    continue
                point = 1
                jewelryList.append(jewelryID)
            if(point == 0):
                jewelryList.append(0)
        time.sleep(0.1)
    return jewelryList

def getUUSellPrice(jewelryList,userID):
    uuUrl = 'https://api.youpin898.com/api/homepage/v2/es/commodity/GetCsGoPagedList'
    uuSellPriceList = []
    for jewelry in jewelryList:
        if(jewelry == 0):
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
def start():
    if os.path.exists(fileName):
        os.remove(fileName)
        print('删除旧文件')
    buffList = getJewelryList()
    idList = getC5JewelryListByName(buffList)
    dataList = getC5Price(idList)
    print(len(dataList))
    uuJewelryList = getUUJewelryList(dataList)
    print(len(uuJewelryList))
    userID = getUUUserID()
    uuSellPriceList = getUUSellPrice(uuJewelryList, userID)
    uuBuyPriceList = getUUBuyPrice(uuJewelryList)
    xw_toExcel(buffList,dataList,uuSellPriceList, uuBuyPriceList)
    print('成功写入')
start()
