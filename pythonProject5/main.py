import re
import json
import requests
from urllib.parse import quote
import xlsxwriter as xw
import os
#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': 'NC5_deviceId=169050548948190205; NC5_version_id=new_web_grey; _bl_uid=dOlRek6nlI9vh1baRqs8h8sk14mL; C5Lang=zh; NC5_crossAccessToken=undefined; noticeList=%5B%22173%22%5D; hideNotice=0; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1691629692,1691716535; CaseNotice=%E6%B4%BB%E5%8A%A8%E9%A5%B0%E5%93%81%E4%B8%80%E8%88%AC%E4%BC%9A%E5%9C%A830%E6%97%A5%E5%86%85%E6%9C%89%E5%BA%8F%E5%8F%91%E5%87%BA%EF%BC%8C%E5%A6%82%E6%9C%89%E9%97%AE%E9%A2%98%E5%8F%AF%E5%92%A8%E8%AF%A2%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%9C%8D%E3%80%82%20%20; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1691725854'
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
            '格洛克 18型 | 荒野反叛 (久经沙场)',
            'AK-47 | 阿努比斯军团 (略有磨损)',
            'AWP | 狮子之日 (久经沙场)',
            'AWP | 浮生如梦 (略有磨损)',
            'AK-47 | 复古浪潮 (久经沙场)',
            'M4A1 消音型 | 印花集 (久经沙场)',
            'AWP | 迷人眼 (久经沙场)',
            'AWP | 浮生如梦 (久经沙场)',
            'AWP | 冥界之河 (久经沙场)',
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
            '格洛克 18型 | 子弹皇后 (略有磨损)',
            'MP9 | 星使 (久经沙场)',
            'AK-47 |翡翠细条纹 (久经沙场)'
            ]
def xw_toExcel(data):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['饰品名称', 'c5价格']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        insertData = [data[j]["name"], data[j]["price"]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    workbook.close()  # 关闭表

#根据饰品id列表获取价格列表（名称：价格）
def getPrice(jewelryList):
    urlPathStart = 'https://www.c5game.com/napi/trade/steamtrade/sga/sell/v3/list?itemId='
    urlPathEnd = '&delivery=2&page=1&limit=10'
    try:
        data = []
        for jewelry in jewelryList:
            url = urlPathStart + jewelry + urlPathEnd
            response = requests.get(url, headers=headers)
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
        xw_toExcel(data)
    except:
        print('爬取失败')

#根据检索关键词列表获取价格列表（名称：价格）
def getAllPrice(nameList):
    urlPathStart = 'https://www.c5game.com/csgo?marketKeyword='
    try:
        jewelryList = []
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
                for item in itemIDList:
                    item = item.strip()
                    item = item.strip('\"')
                    item_id = item[1:].split('/')[0]
                    jewelryList.append(item_id)
        getPrice(jewelryList)
    except:
        print('爬取失败')



def start(nameList,fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
        print('删除旧文件')
    getAllPrice(nameList)

start(nameList,fileName)


