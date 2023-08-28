import re
import json
import requests
from urllib.parse import quote
import xlsxwriter as xw
import os
import time
#c5请求头
C5Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; noticeList=%5B%22174%22%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1692172574,1692232776,1692342532,1692579256; NC5_newC5login=1; PHPSESSID=k0fjhp52p33799n9190nohilah; NC5_uid=1000034675; _csrf=f541e85145f3e481df5fc48fa59eb5acc9692219bbbee695d2ba127d3d6ee22fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22y3NfbUJBxrDDE3T-6qn5bT_k-fFuPWqz%22%3B%7D; NC5_crossAccessToken=undefined; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1692596042'
}
buffHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': '_ntes_nnid=a81ea4b883a087c51b7d8b9f7ce5c913,1690947339047; _ntes_nuid=a81ea4b883a087c51b7d8b9f7ce5c913; Device-Id=3ABe7sqJnoICsII0jmdm; timing_user_id=time_AJGrS6MTiv; Locale-Supported=zh-Hans; game=csgo; AQ_HD=1; YD_SC_SID=624E8F2F08404604A8ECC0A9A7594388; AQ_REQ_FROM=webzj; NTES_YD_SESS=dBpdmWLRcSGCvBLmxymnQiz1uDOnnJKj6pZgLdVoTmJuqC5iqgFBt6PFs.7EZ_6mYLWGAEyRRzg4zpmWcmrVCcXhE6sc0ELel7isPlQeNyozGQ4Bv2MXm8AUQDA86BN9Ql5iJERSwf6i5G7knOBRWek58SD.Z8sKYQjtjUoR2iJO1E1iNfaxaD8mwbUFM00mc4amJK7NJPBaxMW2w6qGY0kRwkvl0rN8LY5ngqdYqf9uP; S_INFO=1693206419|0|0&60##|13162147622; P_INFO=13162147622|1693206419|1|netease_buff|00&99|null&null&null#shh&null#10#0|&0|null|13162147622; remember_me=U1102355461|F8sxxahVWHiaaHcRtzmqH4i7KbjmPoDu; session=1-9vKV3-1blP5LYUmdEDJMMUNrlIIEJmgOIJJ_DXeN70vX2038039389; csrf_token=ImE2OGI3ZDViMTI1ZjcwNGZjODM3ZjQ2ODFiZTMzOWE5MDE0Y2EzNTQi.F83ZPw.P_pUG0eBtFdQ1Qo2wEbBwhoDn-E'
}
#文件名
fileName = '../jewelry.xls'
#饰品名称列表
nameList = ['M4A1 消音型 | 暴怒野兽 (久经沙场)',
            'M4A4 | 死寂空间 (略有磨损)',
            'AK-47 | 混沌点阵 (崭新出厂)',
            'M4A4 | 喧嚣杀戮 (久经沙场)',
            'USP | 黑色魅影 (久经沙场)',
            'M4A4 | 龙王 (略有磨损)',
            '格洛克 18 型 | 荒野反叛 (久经沙场)',
            'AK-47 | 阿努比斯军团 (略有磨损)',
            'AWP | 狮子之日 (久经沙场)',
            'AWP | 浮生如梦 (略有磨损)',
            'AK-47 | 复古浪潮 (久经沙场)',
            'M4A1 消音型 | 印花集 (久经沙场)',
            'AWP | 迷人眼 (久经沙场)',
            'AWP | 浮生如梦 (久经沙场)',
            'AWP | 冥界之河 (崭新出厂)',
            'USP 消音版 | 倒吊人 (久经沙场)',
            'AK-47 | 蓝色层压板 (久经沙场)',
            'AK-47 | 精英之作 (崭新出厂)',
            'AWP | 树蝰 (久经沙场)',
            '沙漠之鹰 | 阴谋者 (崭新出厂)',
            'M4A4 | 黑色魅影 (久经沙场)',
            'M4A4 | 活色生香 (久经沙场)',
            'M4A4 | 彼岸花 (略有磨损)',
            'M4A1 消音型 | 破碎铅秋 (久经沙场)',
            'AWP | 猫猫狗狗 (略有磨损)',
            'FN57 | 怒氓 (久经沙场)',
            '沙漠之鹰 | 机械工业 (久经沙场)',
            'MAC-10 | 霓虹骑士 (略有磨损)',
            'AK-47 | 蓝色层压板 (略有磨损)',
            'M4A1 消音型 | 氮化处理 (略有磨损)',
            '沙漠之鹰 | 机械工业 (崭新出厂)',
            '沙漠之鹰 | 机械工业 (略有磨损)',
            'AK-47 | 幻影破坏者 (略有磨损)',
            '沙漠之鹰 | 大佬龙 (久经沙场)',
            'P90 | 二西莫夫 (久经沙场)',
            'AK-47 | 幻影破坏者 (久经沙场)',
            '格洛克 18 型 | 子弹皇后 (略有磨损)',
            'MP9 | 星使 (久经沙场)',
            'AK-47 |翡翠细条纹 (久经沙场)'
            ]
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

#根据饰品id列表获取价格列表（名称：价格）
def getC5Price(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
    urlPathEnd = '&delivery=2&page=1&limit=10'
    try:
        data = []
        for jewelry in jewelryList:
            url = urlPathStart + jewelry + urlPathEnd
            response = requests.get(url, headers=C5Headers)
            jsonStr = json.loads(response.text)
            items = jsonStr['data']['list']
            if(len(items) != 0):
                item = items[0]
                name = item['itemName']
                price = item['cnyPrice']
                statTrak = 'StatTrak'                                         #去除暗金
                if(statTrak in name):
                    continue
                souvenir = '纪念品'
                if(souvenir in name):
                    continue
                print(name + ": " + price)
                dic = {}
                dic['name'] = name
                dic['price'] = price
                data.append(dic)
        return data
    except:
        print('爬取失败')

#根据检索关键词列表获取价格列表（名称：价格）
def getC5AllPrice(nameList):
    urlPathStart = 'https://www.c5game.com/csgo?marketKeyword='
    try:
        jewelryList = []
        for name in nameList:
            url = urlPathStart + quote(name)
            response = requests.get(url, headers=C5Headers)
            if response.status_code == 200:
                html = response.text
                id_pattern = '<a href="/csgo' + '(.*?)/sell" target="_blank" class="mb20"'
                data_id = json.dumps(re.findall(id_pattern, html)).encode('unicode-escape').decode('unicode-escape')
                data_id = data_id.strip('[')
                data_id = data_id.strip(']')
                itemIDList = data_id.split(',')
                for item in itemIDList:
                    item = item.strip()
                    item = item.strip('\"')
                    item_id = item[1:].split('/')[0]
                    jewelryList.append(item_id)
        return jewelryList
    except:
        print('爬取失败')


def getBuffAllPrice(nameList):
    urlPathStart = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search='
    urlPathEnd = '&use_suggestion=0&_=1691975943061'
    try:
        data = []
        for name in nameList:
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
                    data.append(dic)
            time.sleep(3)
        return data
    except:
        print('爬取失败')

def start(nameList,fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
        print('删除旧文件')
    C5JewelryList = getC5AllPrice(nameList)
    C5Data = getC5Price(C5JewelryList)
    print(len(C5Data))
    buffData = getBuffAllPrice(nameList)
    print(len(buffData))
    xw_toExcel(C5Data,buffData)
    print('成功写入')

start(nameList,fileName)


