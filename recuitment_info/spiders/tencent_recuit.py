# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from recuitment_info.items import RecuitmentInfoItem


class TencentRecuitSpider(CrawlSpider):
    """腾讯 技术类招聘信息爬取"""
    name = 'tencent_recuit'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?keywords=&lid=0&tid=87&start=0#a']

    # 下一页链接的提取规则，返回匹配的链接对象链接
    page_link = LinkExtractor(allow=r'start=\d+')
    # 招聘信息详情页面的链接匹配规则
    # detail_link = LinkExtractor(allow=r'position_detail.php?id=\d+')

    rules = (
        Rule(page_link, callback='parse_item', follow=True),
        # Rule(detail_link, callback='parse_detail', follow=False)
    )

    def parse_item(self, response):
        # item = RecuitmentInfoItem()

        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            item = RecuitmentInfoItem()
            # 职位名称
            item['position_name'] = each.xpath("./td[1]/a/text()").extract()[0]
            # 详情连接
            positionlink = each.xpath("./td[1]/a/@href").extract()[0]
            # 职位类别
            item['position_type'] = each.xpath("./td[2]/text()").extract()[0]
            # 招聘人数
            item['recuit_num'] = each.xpath("./td[3]/text()").extract()[0]
            # 工作地点
            item['work_location'] = each.xpath("./td[4]/text()").extract()[0]
            # 发布时间
            item['publish_time'] = each.xpath("./td[5]/text()").extract()[0]

            yield scrapy.Request(url='https://hr.tencent.com/' + positionlink, meta={'item': item},
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        # 职位名称
        # item['position_name'] = response.xpath("//tbody/tr[@class='h']/td/text()").extract()[0]
        # 职位类型
        # item['position_type'] = response.xpath("//tbody/tr[@class='c bottomline']/td[2]/text()").extract()[0]
        # 招聘人数
        # item['recuit_num'] = response.xpath("//tbody/tr[@class='c bottomline']/td[3]/text()").extract()[0]
        # 工作地点
        # item['work_location'] = response.xpath("//tbody/tr[@class='c bottomline']/td[1]/text()").extract()[0]
        # 发布时间
        # publish_time = scrapy.Field()
        duty = response.xpath("//table/tr[@class='c'][1]/td/ul[@class='squareli']//li/text()").extract()
        #print(duty)
        # 工作职责
        item['work_duty'] = ''.join(duty)

        demand = response.xpath("//table/tr[@class='c'][2]/td/ul[@class='squareli']//li/text()").extract()
        #print(demand)
        # 工作要求
        item['work_demand'] = ''.join(demand)

        yield item
