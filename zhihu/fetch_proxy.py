# encoding=utf-8
from redis import Redis
import requests
import asyncio


class FetchProxy(object):

    def __init__(self,host,port,password):
        self.r = Redis(host=host,port=port,password=password)

    async def get_proxy(self):
        print("获取proxy")
        url = 'http://webapi.http.zhima.com/'
        try:
            resp = await requests.get(url)
            proxy = resp.text
            # print(proxy)
            proxy_list = proxy.split('\r\n')[:-1]
            if proxy_list is not None:
               return proxy_list
        except Exception as e:
            print(e)


    async def test_proxy(self,proxy_list):
        try:
            for p in proxy_list:
                # print("测试proxy")
                # url = 'https://www.baidu.com'
                # proxie = {
                #     'https': 'https://{}'.format(p)
                # }
                # header = {
                #     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
                # }
                # resp = requests.get(url, proxies=proxie, headers=header, timeout=2)
                # print(resp.status_code)
                # if resp.status_code == 200:
               proxy = "https://{}".format(p)
               await self.r.lpush("zhima_proxy",proxy)
               print('save to redis!!!')
        except Exception as e:
            print(e)

    def count_proxy(self):
        return self.r.llen("zhima_proxy")

    async def fetch_proxy(self):
        proxy = await self.r.lpop("zhima_proxy")
        if proxy is not None and self.r.llen("zhima_proxy") > 10:
           return proxy.decode(encoding="utf-8")
        else:
            print('need to fetch proxy!!')
            self.main()

    async def save_proxy(self,proxy):
        await self.r.rpush("zhima_proxy",proxy)

    # def drop_proxy(self,proxy):
    #     self.r.lrem("zhima_proxy",proxy,-1)
    #
    # def delete_keys(self):
    #     self.r.delete("zhima_proxy")
    
    @classmethod
    async def main(self):
        f = FetchProxy()
        while f.count_proxy() == None or f.count_proxy() < 50:
                proxy_list = f.get_proxy()
                f.test_proxy(proxy_list)
                print("already fetch %s" % f.count_proxy())
        print(f.count_proxy())

if __name__ == '__main__':
     asyncio.get_event_loop().run_until_complete(FetchProxy().main())





