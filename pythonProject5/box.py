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
lowPrice = 10
highPrice = 2000
lowSaleNumber = 300
fileName = '../jewelry2.xls'
def xw_toExcel(data,data1,uuSellPriceList,uuBuyPriceList):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['饰品名称', 'c5自发价格','buff最低售价','buff最高求购','uu最低售价','uu最高求购','C5自发/buff','C5自发/uu求购','steam/buff']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        buffProfit =  (0.99 * float(data[j]['price'])/float(data1[j]['buffSellPrice']) - 1) * 100
        steamProfit = float(data1[j]['buffSellPrice'])/(float(data1[j]['steamPrice']) * 0.86)
        uuBuyProfit =  (0.99 * float(data[j]['price'])/uuBuyPriceList[j] - 1) * 100
        insertData = [data[j]["name"], data[j]["price"],data1[j]["buffSellPrice"],data1[j]["buffBuyPrice"],uuSellPriceList[j],uuBuyPriceList[j],buffProfit,uuBuyProfit,steamProfit]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    worksheet1.set_column('A:A',50)
    worksheet1.set_column('B:I',20)
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
                    if (itemName != data['name']):
                        continue
                    # statTrak = 'StatTrak'  # 去除暗金
                    # if (statTrak in itemName):
                    #     continue
                    # souvenir = '纪念品'
                    # if (souvenir in itemName):
                    #     continue
                    print(itemName + ': ' + itemSellPirce + '   ' + itemBuyPrice + '   ' + itemSteamPrice)
                    dic = {}
                    dic['buffSellPrice'] = itemSellPirce
                    dic['buffBuyPrice'] = itemBuyPrice
                    dic['steamPrice'] = itemSteamPrice
                    data1.append(dic)
            else:
                print("响应码错误" + response.status_code)
                sys.exit(1)
            time.sleep(2)
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
            jewelryList.append(jewelryID)
        time.sleep(0.1)
    return jewelryList

def getUUSellPrice(jewelryList,userID):
    uuUrl = 'https://api.youpin898.com/api/homepage/v2/es/commodity/GetCsGoPagedList'
    uuSellPriceList = []
    for jewelry in jewelryList:
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
        os.remove(fileName)
        print('删除旧文件')
    boxIDList = getAllBoxID()
    jewelryList = getJewelryList(boxIDList)
    dataList = getC5Price(jewelryList)
    print(len(dataList))
    dataList2 = getBuffAllPrice(dataList)
    print(len(dataList2))
    uuJewelryList = getUUJewelryList(dataList)
    print(len(uuJewelryList))
    userID = getUUUserID()
    uuSellPriceList = getUUSellPrice(uuJewelryList, userID)
    uuBuyPriceList = getUUBuyPrice(uuJewelryList)
    xw_toExcel(dataList, dataList2,uuSellPriceList,uuBuyPriceList)
    print('成功写入')

start(fileName)


