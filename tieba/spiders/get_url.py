# -*- coding: UTF-8 -*-
import scrapy
from tieba.items import TiebaItem

class TiebaSpider(scrapy.Spider):
    name = "get_url"
    start_urls = [
        'http://tieba.baidu.com/f?kw=%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84&ie=utf-8&pn=0',
    ]

    def parse(self, response):
        sites = response.xpath('//div[@class="t_con cleafix"]')
        for site in sites:
            #desc = site.xpath('div[@class="col2_right j_threadlist_li_right "]/div/div/a/text()').extract()

            item = TiebaItem()
            #item['desc'] = [d.encode('utf-8') for d in desc]
            item['desc'] = site.xpath('div[@class="col2_right j_threadlist_li_right "]/div/div/a/text()').extract()[0]
            item['url'] = site.xpath('div[@class="col2_right j_threadlist_li_right "]/div/div/a/@href').extract()[0]
            item['count'] = site.xpath('div[@class="col2_left j_threadlist_li_left"]/span/text()').extract()[0]
            yield item

        '''
        for page in response.xpath('//a[@class="j_th_tit "]/@href').extract():
            url = 'http://tieba.baidu.com/' + page
            with open('urls.txt',"a") as f:
                f.write(url + '\n')
        '''

        next_page = response.xpath('//a[@class="next pagination-item "]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
