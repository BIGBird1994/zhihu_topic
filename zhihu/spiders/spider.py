# coding=utf-8
from scrapy import Request,Spider
from ..items import ZhihuItem
from json import loads


class Zhihu_Spider(Spider):
      name = 'zhihu_spider'
      start_urls = [
          'https://www.zhihu.com/search?q=%E9%A3%8E%E5%8F%98%E7%BC%96%E7%A8%8B&utm_content=search_suggestion&type=content',
          'https://www.zhihu.com/api/v4/search_v3?t=topic&q=%E6%97%B6%E5%B0%9A%E7%A9%BF%E6%90%AD&correction=1&offset=10&limit=10&show_all_topics=1&search_hash_id=e2f41e786a77cec6159636bd7a2ee471'
      ]
      allowed_domains = []
      api = 'https://www.zhihu.com/api/v4/search_v3?t=topic&q={}AD&correction=1&offset=10&limit=10&show_all_topics=1&search_hash_id=e2f41e786a77cec6159636bd7a2ee471'
      topic_api = 'https://www.zhihu.com/topic/{}/hot'
      
      def start_requests(self):
              
           yield Request(url=self.start_urls[0],callback=self.parse_topic_link)
           yield Request(url=self.start_urls[-1],callback=self.parse_topic_offset)

      def parse_topic_link(self, response):
          for data in response.xpath('//a[@class="TopicLink"]'):
              topic_href = data.xpath('@href').extract_first()
              yield Request(url=topic_href,callback=self.parse_top_question)

      def parse_topic_offset(self, response):
          resp = loads(response.text)
          for data in resp.get('data'):
              topic_id = data['object']['id']
              yield Request(url=self.topic_api.format(topic_id),callback=self.parse_top_question)
          if resp.get('paging').get('is_end') == 'false':
              print(resp.get('paging').get('is_end'))
              next = resp['paging']['next']
              yield Request(url=next,callback=self.parse_topic_offset)

      def parse_top_question(self, response):
          for data in response.xpath('//meta[@itemprop="url"]'):
              question_href = data.xpath('@href').extract()

