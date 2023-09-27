# c5crawler
# c5爬虫

### develop.py 开发模块

### newC5game.py 捡漏脚本：从jewelry5.xls中读取c5饰品id,比较c5底价和uu求购最高价,比较igxe底价和uu求购最高价

### csqaq.py 爬取c5自发价格，buff和uu的在售底价和求购最高价，并计算利润写入jewelry3.xls文件，效率远高于box.py

### ipPools.py 从redis取出高效率的高匿ip写入ip_pools.txt

### bestC5game.py newC5game的高并发模式（待开发）

### reconfiguration.py newC5game的标准化写法

### buff.py 从buff筛选出指定饰品和对应的c5饰品id

### test.py 测试模块

### C5AutoBuy.py 获取c5可进行自动收货的高利润求购

### C5Buy.py 自动调整c5求购（待开发）