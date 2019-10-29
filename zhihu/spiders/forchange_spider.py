from scrapy import Request,Spider
# from ..items import ZhihuItem
import logging
import sys,os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class ForchangeSpider(Spider):
    name = 'forchange_spider'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Content-type': "application/json;charset=UTF-8",
        'cookie': '_zap=ef9cab50-e395-4b71-aa7b-aaa0bf7b3e46; d_c0="AFCmWfF7Lw6PTlJLTUkDgHYRxazWpMUEgeY=|1536484776"; __gads=ID=542853be4b172a97:T=1539754208:S=ALNI_MbtjI6yClO3qZ2hPqpkRv63vsIuig; tst=r; __utmv=51854390.100-1|2=registration_date=20140518=1^3=entry_date=20140518=1; z_c0="2|1:0|10:1567849950|4:z_c0|92:Mi4xYnBKYkFBQUFBQUFBVUtaWjhYc3ZEaVlBQUFCZ0FsVk4zc3RnWGdCVHJlS093TDM3M3owQjNqcW5jLVhSd3BlSFBB|a0f5ac3ff3443ad8c6c528d1c6855d692e49308ea046966207b46cb57ec95a27"; q_c1=073cb88e5bc644779954e14f61d60dc6|1569150463000|1536484790000; __utma=51854390.1212183169.1554459696.1570454336.1570630077.9; __utmz=51854390.1570630077.9.9.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/337403631/answer/840276679; tgw_l7_route=73af20938a97f63d9b695ad561c4c10c; _xsrf=9b4b3af3-592e-4dbd-939b-c32e868dcbf9; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1570675202,1570694447,1571044369,1571361816; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1571362210'
        # 'origin': ' https://fashion.zhiyitech.cn',
        # 'referer': 'https://fashion.zhiyitech.cn/find/1?findPage=true&filters=%5B%7B%22sex%22%3A%22%22,%22searchCategory%22%3A%22%22,%22rootCategory%22%3A%22%22%7D%5D',
        
    }
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': headers,
        'HTTPERROR_ALLOWED_CODES': [302, 400, 404, 403, 418, 429, 503],
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1
        
    }
    search_url = 'https://www.zhihu.com/search?q=风变编程&utm_content=search_history&type=content'
    answer_url = 'https://www.zhihu.com/question/{}/answer/{}'
    comment_url = 'https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=20&offset=0&status=open'
   
    def start_requests(self):
        yield Request(url=self.search_url,callback=self.parse)
        
    def parse(self, response):
        print(response.text)
        for data in response.xpath('//div[@class="List"]'):
            href = data.xpath('//meta[@itemprop="url"]/@content').extract_first(default=None)
            print(href)
        

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute('scrapy crawl forchange_spider'.split())
    
    
    
    
    