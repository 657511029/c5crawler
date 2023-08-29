import re
import json
import sys
import time

import requests
from urllib.parse import quote
import xlsxwriter as xw
import os


receiveSteamId = ''
num = 3
C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEwMDAxODkzMTYsImN0ZSI6MTY5MzI4NjQ0NH0.7CB4SD10hRBZ2XJxy6u5uVyM0ntMXcYdlNE2UK8nh74',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; noticeList=%5B%22174%22%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1692841262,1692934095,1693202075,1693271339; PHPSESSID=cr1imn04n3kmb1a2f11m6bgb7v; CaseNotice=%E6%B4%BB%E5%8A%A8%E9%A5%B0%E5%93%81%E4%B8%80%E8%88%AC%E4%BC%9A%E5%9C%A830%E6%97%A5%E5%86%85%E6%9C%89%E5%BA%8F%E5%8F%91%E5%87%BA%EF%BC%8C%E5%A6%82%E6%9C%89%E9%97%AE%E9%A2%98%E5%8F%AF%E5%92%A8%E8%AF%A2%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%9C%8D%E3%80%82%20%20; NC5_accessToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEwMDAxODkzMTYsImN0ZSI6MTY5MzI4NjQ0NH0.7CB4SD10hRBZ2XJxy6u5uVyM0ntMXcYdlNE2UK8nh74; NC5_uid=1000189316; NC5_newC5login=1; NC5_crossAccessToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEwMDAxODkzMTYsImN0ZSI6MTY5MzI4NjQ0NH0.7CB4SD10hRBZ2XJxy6u5uVyM0ntMXcYdlNE2UK8nh74; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1693286446; _csrf=d41ae7c6116774fc8803ff4f385d3a6118fb5c929f56bacd040607ae35736c3ea%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22qNiwHb3yi9QXSVAYCjVFLBSAWX53B-vx%22%3B%7D'
}

def getJewelryList():
    try:
        urlStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/purchase/v2/personal-list?page=1&limit=30&status=1&appId=730&type='
        jewelryList = []
        url = urlStart
        response = requests.get(url, headers=C5Headers)
        if response.status_code == 200:
            jsonStr = json.loads(response.text)
            buyList = jsonStr['data']['list']
            for item in buyList:
                itemID = item['itemId']
                id = item['id']
                map = {}
                map['itemID'] = itemID
                map['id'] = id
                jewelryList.append(map)
            return jewelryList
    except:
        print('爬取失败')

def cancelJewelryList(jewelryList):
    try:
        urlStart = 'https://www.c5game.com/napi/trade/steamtrade/trade-purchase/v1/cancel'
        for jewelry in jewelryList:
            url = urlStart
            data = {
                'purchaseId': jewelry['id']
            }
            response = requests.post(url,json=data, headers=C5Headers)
            if response.status_code == 200:
                print('取消求购成功')
    except:
        print('爬取失败')
def getJewelryBuyInfo(jewelryList):
    try:
        urlStart = 'https://www.c5game.com/napi/trade/steamtrade/item/price/v1/553489664/detail?styleId=0&itemId='
        maxPurchasePriceList = []
        for jewelry in jewelryList:
            url = urlStart + jewelry['itemID']
            response = requests.get(url, headers=C5Headers)
            if response.status_code == 200:
                jsonStr = json.loads(response.text)
                maxPurchasePrice = jsonStr['data']['maxPurchasePrice']
                map = {}
                map['maxPurchasePrice'] = maxPurchasePrice
                map['jewelry'] = jewelry['itemID']
                maxPurchasePriceList.append(map)
        return maxPurchasePriceList
    except:
        print('爬取失败')

def setJewelryBuy(jewelryList):
    try:
        urlStart = 'https://www.c5game.com/napi/trade/steamtrade/trade-purchase/v5/create'
        purchaseIdList = []
        for jewelry in jewelryList:
            url = urlStart
            data = {
                'currencyType': 0,
                'itemId': jewelry['jewelry'],
                'num': num,
                'openSecretFree': 1,
                'price': str(jewelry['maxPurchasePrice'] + 0.01),
                'receiveSteamId': receiveSteamId,
                'styleId': "0"
            }
            response = requests.post(url,json=data, headers=C5Headers)
            if response.status_code == 200:
                jsonStr = json.loads(response.text)
                purchaseId = jsonStr['data']['id']
                purchaseIdList.append(purchaseId)
        return purchaseIdList
    except:
        print('爬取失败')

def overJewelryBuy(purchaseIdList):
    try:
        urlStart = 'https://www.c5game.com/napi/trade/steamtrade/pay/v1/create'
        for purchaseId in purchaseIdList:
            url = urlStart
            data = {
                'autoSendOffer': 0,
                'couponId': "0",
                'currencyType': "0",
                'gateway': "",
                'nimbleParam': "",
                'orderIds': [purchaseId],
                'payMoney': 0,
                'payPassword': "",
                'promotionId': "",
                'receiveSteamId': receiveSteamId,
                'type': 2,
                'useBalance': 1
            }
            response = requests.post(url,json=data, headers=C5Headers)
            if response.status_code == 200:
                print('改价成功')
    except:
        print('爬取失败')


def start():
    jewelryList = getJewelryList()
    cancelJewelryList(jewelryList)
    jewelryBuyList = getJewelryBuyInfo(jewelryList)
    setJewelryBuy(jewelryBuyList)

start()