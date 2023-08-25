import base64
import json
import requests


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
session = requests.Session()
loginUrl = "https://api.youpin898.com/api/user/Auth/PwdSignIn"

loginHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54',
    'Referer': 'https://www.youpin898.com/'
}
loginData = {
    'UserName': '13162147622',
    'UserPwd': 'Lenshanshan521',
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

def getUUUserID():
    uuUrl = 'https://api.youpin898.com/api/user/Account/GetUserInfo'
    html = session.get(uuUrl, headers=uuHeaders)
    html.encoding = 'utf-8'
    jsonStr = json.loads(html.text)
    userID = jsonStr['Data']['UserId']
    return userID
def getUUJewelryList(nameList):
    uuUrl = 'https://api.youpin898.com/api/homepage/search/list'
    jewelryList = []
    for name in nameList:
        uuData = {
            'gameId': '730',
            'keyWords': name,
            'listSortType': '2',
            'listType': '10',
            'pageIndex': 1,
            'pageSize': 20,
            'sortType': '0',
            'stickers': {},
            'stickersIsSort': False
        }
        html = session.post(uuUrl, headers=uuHeaders, json=uuData)
        html.encoding = 'utf-8'
        jsonStr = json.loads(html.text)
        JewelryID = jsonStr['Data']['commodityTemplateList'][0]['Id']
        jewelryList.append(JewelryID)
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
        html.encoding = 'utf-8'
        jsonStr = json.loads(html.text)
        price = jsonStr['Data']['CommodityList'][0]['Price']
        print(jsonStr['Data']['CommodityList'][0]['CommodityName'])
        uuSellPriceList.append(price)
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
        html.encoding = 'utf-8'
        jsonStr = json.loads(html.text)
        price = jsonStr['Data']['response'][0]['unitPrice']
        uuBuyPriceList.append(price)
    return uuBuyPriceList

jewelryList = getUUJewelryList(nameList)
print(len(jewelryList))
userID = getUUUserID()
uuSellPriceList = getUUSellPrice(jewelryList,userID)
uuBuyPriceList = getUUBuyPrice(jewelryList)
for i in range(0, len(nameList)):
    print(nameList[i] + ': ' + uuSellPriceList[i] + '   ' + uuBuyPriceList[i])