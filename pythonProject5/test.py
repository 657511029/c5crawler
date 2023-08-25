import json
import re

import requests

uuHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzOTUxOWQwMDE0ZjU0NWEyYWVmYWMwZjMxZDdhOTNkNiIsIm5hbWVpZCI6IjE4NzA5MzAiLCJJZCI6IjE4NzA5MzAiLCJ1bmlxdWVfbmFtZSI6IllQMDAwMTg3MDkzMCIsIk5hbWUiOiJZUDAwMDE4NzA5MzAiLCJuYmYiOjE2OTI5Mjc0NDUsImV4cCI6MTY5Mzc5MTQ0NSwiaXNzIjoieW91cGluODk4LmNvbSIsImF1ZCI6InVzZXIifQ.iWGhQgIbECZxafgS9P1aRg54FYeJFqnaTpWoVjI1Ovo',
    'Referer': 'https://www.youpin898.com/',
    'Apptype': '1'
}

def getUUAllPrice():
    urlPathStart = 'https://api.youpin898.com/api/homepage/search/list'
    # try:
    url = urlPathStart
    formData = {
        'gameId' : '730',
        'keyWords' : '暴怒野兽',
        'listSortType' : '2',
        'listType' : '10',
        'pageIndex' : 1,
        'pageSize' : 20,
        'sortType' : '0',
        'stickers' : {},
        'stickersIsSort' : False,

    }
    response = requests.post(url,data=formData,headers=uuHeaders)
    if response.status_code == 200:
        html = response.text
        print(html)
    # except:
    #     print('爬取失败')
getUUAllPrice()