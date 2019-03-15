# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class ZhihuItem(Item):
      answer_info = Field()
      source_url = Field()
      visit_count = Field()
      follower_count = Field()
      key_words = Field()
      question_info = Field()
      
      
      
class UserId(Item):
      user_id = Field()
