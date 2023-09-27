from redis import StrictRedis


class IpPool:
    def __init__(self):
        self.host = 'localhost'
        self.port = 6379
        self.db = 0
        self.password = '521633'
        self.name = 'proxies:universal'
        self.file = open('ip_pool.txt', 'w+')
    def crawl(self):
        redis = StrictRedis(host=self.host, port=self.port, db=self.db, password=self.password)
        ipList = redis.zrangebyscore(self.name,100, 100, start=None, num=None, withscores=False)
        ipList = [x.decode('utf-8') for x in ipList]
        for ip in ipList:
            self.file.write(ip + '\n')
        self.file.close()
        print('写入ip池成功: ' + str(len(ipList)))
        # 执行完毕关闭文本


if __name__ == '__main__':
    ip = IpPool()
    ip.crawl()
