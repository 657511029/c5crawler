import re
import json
import requests
from lxml import etree
from urllib.parse import quote
import time
import xlsxwriter as xw
import os
buffHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Cookie': '_ntes_nnid=a81ea4b883a087c51b7d8b9f7ce5c913,1690947339047; _ntes_nuid=a81ea4b883a087c51b7d8b9f7ce5c913; Device-Id=3ABe7sqJnoICsII0jmdm; timing_user_id=time_AJGrS6MTiv; P_INFO=13162147622|1691974203|1|netease_buff|00&99|null&null&null#shh&null#10#0|&0|null|13162147622; remember_me=U1102355461|2CftSTVqcxaY6rfX15EhBTdQMKiHLTUy; session=1-q59PRT0PyU5HigWHa4Y0UY8qs_sASDthgmRHwDGQtKu42038039389; Locale-Supported=zh-Hans; game=csgo; csrf_token=IjQzYmZhMzIxYTg1Mjk5Y2NkOTU2YzA2NTIxYTM5YTAyMTIyNzc5ZGYi.F8RUEg.YCaBvXfKhOEswgrvKOvUKHbNLXk',
    'Referer': 'https://buff.163.com/user-center/message/?type=trade'
}

def getBuffAllPrice():
    urlPathStart = 'https://buff.163.com/user-center/bookmark/goods?game=csgo'
    try:
        count = 0
        url = urlPathStart
        response = requests.get(url, headers=buffHeaders)
        if response.status_code == 200:
            data_name = []
            data = response.text
            tree = etree.HTML(data)
            print(tree)
            div_list = tree.xpath('//td[@class="name-cont"]//text()')
            print(div_list)
            # pattern = '<a href="/goods/(.*?)">(.*?)</a>'
            # data_last = json.dumps(re.findall(pattern, data))
            # data_list = re.split('\[|]|,',data_last)
            # print(data_list)
            # for item in data_list:
            #     print(item)
            # point = 0
            # for item in data_last:
            #     if point%2 == 1:
            #         data_name.append(item[1])
            #     point += 1
            # print(data_name)
        else:
            print('响应码错误: ' + response.status_code)

    except:
        print('爬取失败')
getBuffAllPrice()