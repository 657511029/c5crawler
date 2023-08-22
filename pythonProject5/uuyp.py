import json
import requests

uuHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkMzg2YmIzOWE2OTA0ODM2ODNjMDczZTdhMjU0NGZhMCIsIm5hbWVpZCI6IjE4NzA5MzAiLCJJZCI6IjE4NzA5MzAiLCJ1bmlxdWVfbmFtZSI6IllQMDAwMTg3MDkzMCIsIk5hbWUiOiJZUDAwMDE4NzA5MzAiLCJuYmYiOjE2OTIwNjExNTQsImV4cCI6MTY5MjkyNTE1NCwiaXNzIjoieW91cGluODk4LmNvbSIsImF1ZCI6InVzZXIifQ.8wp13fKZtn6MYG5A9pGhjF79LncTecijq86cfX-aqBw'
}
nameList = ['M4A1 消音型 | 暴怒野兽 (久经沙场)']

def getUUAllPrice(nameList):
    urlPathStart = 'https://api.youpin898.com/api/homepage/search/list'
    # try:
    for name in nameList:
            formData = {
                'gameId': '\"730\"',
                'keyWords': '\"' + name + '\"',
                'listSortType': '\"2\"',
                'listType': '\"10\"',
                'pageIndex': '1',
                'pageSize': '20',
                'sortType': '\"0\"',
                'stickers': '{}',
                'stickersIsSort': 'false'
            }
            url = urlPathStart
            response = requests.post(url,formData, headers=uuHeaders)
            if response.status_code == 200:
                jsonStr = json.loads(response.text)
                itemList = jsonStr['data']['commodityTemplateList']
                if(len(itemList) != 0):
                    item = itemList[0]
                    itemID = item['Id']
                    print(itemID)
    # except:
    #     print('爬取失败')
getUUAllPrice(nameList)