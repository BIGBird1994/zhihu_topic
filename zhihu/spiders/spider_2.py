# # coding=utf-8
# from scrapy import Request,Spider
# from ..items import ZhihuItem
# from json import loads
# import re
# from ..fetch_proxy import FetchProxy
# from scrapy.exceptions import CloseSpider
# 
# 
# class Zhihu_Spider(Spider):
#       name = 'zhihu'
#       start_urls = [
#           # 'https://www.zhihu.com/topic/19551052/hot',
#           # 'https://www.zhihu.com/topic/19641262/hot',
#           # 'https://www.zhihu.com/topic/19644670/hot',
#           'https://www.zhihu.com/topic/20047559/hot',
#           'https://www.zhihu.com/topic/20057148/hot',
#           'https://www.zhihu.com/topic/19868718/hot',
#           'https://www.zhihu.com/topic/19900175/hot'
#       ]
#       allowed_domains = [
#                          'zhuanlan.zhihu.com',
#                          'zhihu.com'
#                          ]
#       topic_ids = ['20047559','20057148','19868718','19900175']
#       topic_api = 'https://www.zhihu.com/api/v4/topics/{}/feeds/essence?&limit=10&offset=5'
#       question_url = 'https://www.zhihu.com/question/{}/'
#       answer_api = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&offset=20&limit=20&sort_by=default'
#       log_url = 'https://www.zhihu.com/question/{}/log'
#       f = FetchProxy()
# 
# 
#       def start_requests(self):
#           with open('./ids.txt','r') as f:
#               for line in f.readlines:
#                   if line:
#                       id = line.strip()
#                       url = self.question_url.format(id)
#                       yield Request(url=url, meta={'id': id, 'url': url}, callback=self.parse_answer,
#                                     errback=self.error_handle)
#           for url in self.start_urls:
#                yield Request(url=url,meta={'url':url},callback=self.parse_question,errback=self.error_handle,dont_filter=True)
#           for id in self.topic_ids:
#               url = self.topic_api.format(id)
#               yield Request(url=url,meta={'url':url},callback=self.parse_question_id,errback=self.error_handle,dont_filter=True)
#           
# 
#       def parse_question_id(self, response):
#           if '请点击图中倒立的文字'  in response.text or response.status == 302 or response.status == 403:
#               url = response.meta['url']
#               yield Request(url=url,meta={'url':url},callback=self.parse_question_id,dont_filter=True)
#           elif response.status == 200:
#               res = loads(response.text)
#               for data in res['data']:
#                   if data['target'].get('question'):
#                      id = data['target']['question']['id']
#                      # yield Request(url=self.log_url.format(id),meta={'id':id},callback=self.parse_question_author)
#                      url = self.question_url.format(id)
#                      yield Request(url=url,meta={'id':id,'url':url},callback=self.parse_answer,errback=self.error_handle)
#                      # yield Request(url=self.answer_api.format(data['target']['question']['id']),callback=self.parse_answer_offset)
#                   else:
#                       print(data['target'])
# 
# 
#               proxy = response.meta['proxy']
#               self.f.save_proxy(proxy)
#               self.logger.info('<------- save %s to redis ------->' % proxy)
#               if res['paging'].get('is_end') == False:
#                  next = res['paging']['next']
#                  yield Request(url=next,meta={'url':next},callback=self.parse_question_id,errback=self.error_handle)
#               else:
#                   print(res,type(res['paging']['next']))
# 
# 
#       def parse_question(self, response):
#           if '请点击图中倒立的文字'  in response.text or response.status == 302 or response.status == 403:
#               url = response.meta['url']
#               yield Request(url=url,meta={'url':url},callback=self.parse_question,dont_filter=True)
#           elif response.status == 200 :
#               for data in response.xpath('//a[@data-za-detail-view-element_name="Title"]'):
#                   href = data.xpath('@href').extract_first()
#                   print(href)
#                   if 'answer' in href:
#                       id = re.findall(r'/question/(\d+)/answer',href)[0]
#                       # yield Request(url=self.log_url.format(id), meta={'id': id}, callback=self.parse_question_author)
#                       yield Request(url=self.question_url.format(id),meta={'id':id},callback=self.parse_answer,errback=self.error_handle)
#                       # yield Request(url=self.answer_api.format(id), callback=self.parse_answer_offset)
#                   else:
#                       pass
#                       # yield Request(url='https:{}'.format(href),callback=self.parse_zhuan_lan)
#               proxy = response.meta['proxy']
#               self.f.save_proxy(proxy)
#               self.logger.info('<------- save %s to redis ------->' % proxy)
# 
#       def parse_answer_offset(self, response):
#           if '请点击图中倒立的文字' in response.text:
#               url = response.meta['url']
#               item = response.meta['item']
#               meta = {'item': item, 'url': url}
#               yield Request(url=url, meta=meta, callback=self.parse_answer_offset,dont_filter=True)
#           elif response.status == 200:
#               res = loads(response.text)
#               for data in res['data']:
#                   item = response.meta['item']
#                   item['answer_info'] = data
#                   item['source_url'] = response.url
#                   yield item
#               proxy = response.meta['proxy']
#               self.f.save_proxy(proxy)
#               self.logger.info('<------- save %s to redis ------->' % proxy)
#               if res['paging'].get('is_end') == False:
#                  next = res['paging']['next']
#                  item = response.meta['item']
#                  meta = {'item': item, 'url': next}
#                  yield Request(url=next,meta=meta,callback=self.parse_answer_offset,errback=self.error_handle)
#               else:
#                   print(res['paging']['is_end'])
# 
#       def parse_answer(self, response):
#           if '请点击图中倒立的文字'  in response.text or response.status == 302 or response.status == 403:
#               url = response.meta['url']
#               id = response.meta['id']
#               yield Request(url=url,meta={'url':url,'id':id},callback=self.parse_answer,dont_filter=True)
#           elif response.status == 200 :
#               item = ZhihuItem()
#               question_info = {}
#               # question_info = response.meta['question_info']
#               key_words = response.xpath('//meta[@itemprop="keywords"]/@content').extract_first(default='')
#               if key_words is not None:
#                   question_info['key_words'] = key_words.split(',')
#               else:
#                   question_info['key_words'] = []
#               question_info['follower_count'] = response.xpath('//strong[@class="NumberBoard-itemValue"]/text()').extract()[0]
#               question_info['visit_count'] = response.xpath('//strong[@class="NumberBoard-itemValue"]/text()').extract()[1]
#               # question_info['author_name'] = re.findall(r'"name":"(\w+)"\,',response.text)[-2]
#               item['question_info'] = question_info
#               id = response.meta['id']
#               url = self.answer_api.format(id)
#               meta = {'item':item,'url':url}
#               yield Request(url=url,meta=meta,callback=self.parse_answer_offset,errback=self.error_handle)
#               proxy = response.meta['proxy']
#               self.f.save_proxy(proxy)
#               self.logger.info('<------- save %s to redis ------->' % proxy)
# 
# 
#       def parse_zhuan_lan(self, response):
#           pass
# 
# 
#       def parse_question_author(self, response):
#           question_info = {}
#           question_info['question_author'] = response.xpath('//span[@class="zg-gray-normal"]/preceding-sibing::*').extract_first(default='')
#           id = response.meta['id']
#           yield Request(url=self.question_url.format(id),meta={'quetion_info':question_info,'id':id},callback=self.parse_answer)
# 
# 
#       def error_handle(self, failure):
#           req = failure.request
#           url = req.meta['url']
#           if 'www.zhihu.com/topic' in url:
#               meta = {'url':url}
#               print('<--- parse_question, {} --->'.format(url))
#               yield Request(url=url,meta=meta,callback=self.parse_question,dont_filter=True,errback=self.error_handle)
#           elif 'www.zhihu.com/api/v4/topics' in url:
#               meta = {'url': url}
#               print('<--- parse_question_id, {} --->'.format(url))
#               yield Request(url=url, meta=meta, callback=self.parse_question_id, dont_filter=True,
#                             errback=self.error_handle)
#           elif 'www.zhihu.com/question' in url:
#               meta = {'url': url,'id':req.meta['id']}
#               print('<--- parse_question_answer, {} --->'.format(url))
#               yield Request(url=url, meta=meta, callback=self.parse_answer, dont_filter=True,
#                             errback=self.error_handle)
#           elif 'www.zhihu.com/api/v4/questions?' in url:
#               meta = {'item': req.meta['item'], 'url': url}
#               print('<--- parse_answer_offset, {} --->'.format(url))
#               yield Request(url=next, meta=meta, callback=self.parse_answer_offset,dont_filter=True,
#                             errback=self.error_handle)



