import re
import json
import requests


lowPrice = 10
highPrice = 2000

C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; noticeList=%5B%22174%22%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1692579256,1692670832,1692751966,1692841262; NC5_newC5login=1; PHPSESSID=eto84kfqiql35fpetcaedussr3; CaseNotice=%E6%B4%BB%E5%8A%A8%E9%A5%B0%E5%93%81%E4%B8%80%E8%88%AC%E4%BC%9A%E5%9C%A830%E6%97%A5%E5%86%85%E6%9C%89%E5%BA%8F%E5%8F%91%E5%87%BA%EF%BC%8C%E5%A6%82%E6%9C%89%E9%97%AE%E9%A2%98%E5%8F%AF%E5%92%A8%E8%AF%A2%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%9C%8D%E3%80%82%20%20; NC5_uid=1000189316; NC5_isShowInspect=-1; _csrf=ef31974c96bf8f8cda74f9546539babbd8d43ae8ec6df9fb0bf128ad362262c9a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Tnltc1spYsUAgB6xoY7ly4uGTGbCJpat%22%3B%7D; NC5_crossAccessToken=undefined; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1692858886'
}

def getAllBoxID():
    urlPathStart = 'https://www.c5game.com/playground/case'
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

def getJewelryList(boxIDList):
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
                    if (out in itemName):
                        continue
                    itemID = item['item_id']
                    jewelryList.append(itemID)
    jewelryList = list(dict.fromkeys(jewelryList))
    return jewelryList

def getC5Price(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/purchase/v2/list?itemId='
    urlPathEnd = '&delivery=&styleId=&page=1&limit=10'
    dataList = []
    for jewelry in jewelryList:
        url = urlPathStart + jewelry + urlPathEnd
        response = requests.get(url, headers=C5Headers)
        jsonStr = json.loads(response.text)
        items = jsonStr['data']['list']
        if (len(items) != 0):
            item = items[0]
            price = item['cnyPrice']
            name = item['itemName']
            if (float(price) < lowPrice):
                continue
            if (float(price) > highPrice):
                continue
            print(name + ": " + str(price))
            dic = {}
            dic['name'] = name
            dic['jewelry'] = jewelry
            dic['price'] = price
            dataList.append(dic)
    return dataList
def getC5AutoPrice(dataList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/purchase/v2/list?itemId='
    urlPathEnd = '&delivery=2&styleId=&page=1&limit=10'
    for data in dataList:
        jewelry = data['jewelry']
        url = urlPathStart + jewelry + urlPathEnd
        response = requests.get(url, headers=C5Headers)
        jsonStr = json.loads(response.text)
        items = jsonStr['data']['list']
        autoPrice = 0.00
        if(len(items) != 0):
            item = items[0]
            autoPrice = item['cnyPrice']
        if (autoPrice/data['price'] < 0.97):
            print(data['name'] + ": " + str(data['price']) + '    ' + str(autoPrice))
def start():
    boxIDList = getAllBoxID()
    print(len(boxIDList))
    jewelryList = getJewelryList(boxIDList)
    print(len(jewelryList))
    dataList = getC5Price(jewelryList)
    print(len(dataList))
    print('可进行自动求购的饰品')
    getC5AutoPrice(dataList)
start()