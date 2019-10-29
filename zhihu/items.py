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
      

class ForchangeItem(Item):
        q_title = Field()
        q_description = Field()
        q_nickname = Field()
        q_ctime = Field()
        q_follower = Field()
        q_broswer_num = Field()
        a_num = Field()
        a_content = Field()
        a_nickname = Field()
        a_time = Field()
        a_likenum = Field()
        comment_num = Field()
        comment_nickname = Field()
        comment_content = Field()
        
    
        
        
        
      
      
