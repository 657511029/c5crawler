import json
import requests

uuHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0NDAwMmFkZDJmYmE0NTJkOTY3YTNiOWI1Yzc2ZDZlNSIsIm5hbWVpZCI6IjE4NzA5MzAiLCJJZCI6IjE4NzA5MzAiLCJ1bmlxdWVfbmFtZSI6IllQMDAwMTg3MDkzMCIsIk5hbWUiOiJZUDAwMDE4NzA5MzAiLCJuYmYiOjE2OTI2Njg1NzUsImV4cCI6MTY5MzUzMjU3NSwiaXNzIjoieW91cGluODk4LmNvbSIsImF1ZCI6InVzZXIifQ.s5D7pv182lInbCDTrI5EUHgGzgjIOyir0H9BfiUSLeY',
    'Content-Type': 'application/json',
    'Referer': 'https://www.youpin898.com/',
    'Origin': 'https://www.youpin898.com',
    'Apptype': '1'
}
nameList = ['M4A1 消音型 | 暴怒野兽 (久经沙场)']

def getUUAllPrice(nameList):
    urlPathStart = 'https://api.youpin898.com/api/homepage/search/list'
    # try:
    for name in nameList:
            formData = {
                'gameId': '730',
                'keyword': name,
                # 'keyWords': name,
                # 'listSortType': null,
                # 'listType': '10',
                'pageIndex': 1,
                'pageSize': 10
                # 'sortType': 1,
                # 'stickers': {}
                # 'stickersIsSort': 'false'
            }
            url = urlPathStart
            response = requests.post(url,data=formData, headers=uuHeaders)
            if response.status_code == 200:
                jsonStr = json.loads(response.text)
                print(response.text)
                print(jsonStr)
                # itemList = jsonStr['data']['commodityTemplateList']
                # if(len(itemList) != 0):
                #     item = itemList[0]
                #     itemID = item['Id']
                #     print(itemID)
    # except:
    #     print('爬取失败')
getUUAllPrice(nameList)