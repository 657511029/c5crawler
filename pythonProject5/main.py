import urllib
from flask import Flask
import re
import json
import requests
from urllib.parse import quote
from urllib.parse import unquote

#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; C5Lang=zh; NC5_crossAccessToken=undefined; noticeList=%5B%22173%22%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1691629692,1691716535; CaseNotice=%E6%B4%BB%E5%8A%A8%E9%A5%B0%E5%93%81%E4%B8%80%E8%88%AC%E4%BC%9A%E5%9C%A830%E6%97%A5%E5%86%85%E6%9C%89%E5%BA%8F%E5%8F%91%E5%87%BA%EF%BC%8C%E5%A6%82%E6%9C%89%E9%97%AE%E9%A2%98%E5%8F%AF%E5%92%A8%E8%AF%A2%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%9C%8D%E3%80%82%20%20; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1691725854'
}
#根据饰品id列表获取价格列表（名称：价格）
def getPrice(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
    urlPathEnd = '&delivery=2&page=1&limit=10'
    try:
        for jewelry in jewelryList:
            url = urlPathStart + jewelry + urlPathEnd
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                jsonStr = json.loads(response.text)
                items = jsonStr['data']['list']
                if(len(items) != 0):
                    item = items[0]
                    name = item['itemName']
                    price = item['cnyPrice']
                    statTrak = 'StatTrak'                                         #去除暗金
                    if(statTrak in name):
                        continue
                    print(name + ": " + price)
            else:
                print('响应码错误:' + response.status_code)
    except:
        print('爬取失败')


#根据检索关键词列表获取价格列表（名称：价格）
def getAllPrice(nameList):
    urlPathStart = 'https://www.c5game.com/csgo?marketKeyword='
    try:
        for name in nameList:
            url = urlPathStart + quote(name)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                html = response.text
                id_pattern = '<a href="/csgo' + '(.*?)/sell" target="_blank" class="mb20" data-v-2d723912>'
                data_id = json.dumps(re.findall(id_pattern, html)).encode('unicode-escape').decode('unicode-escape')
                data_id = data_id.strip('[')
                data_id = data_id.strip(']')
                itemIDList = data_id.split(',')
                jewelryList = []
                for item in itemIDList:
                    item = item.strip()
                    item = item.strip('\"')
                    item_id = item[1:].split('/')[0]
                    jewelryList.append(item_id)
                getPrice(jewelryList)

            else:
                print('响应码错误:' + response.status_code)
    except:
        print('爬取失败')

nameList = ['暴怒野兽 崭新出厂']
getAllPrice(nameList)


