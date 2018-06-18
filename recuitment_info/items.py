# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecuitmentInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # 职位名称
    position_name = scrapy.Field()
    # 职位类型
    position_type = scrapy.Field()
    # 招聘人数
    recuit_num = scrapy.Field()
    # 工作地点
    work_location = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()
    # 工作职责
    work_duty = scrapy.Field()
    # 工作要求
    work_demand = scrapy.Field()
