import scrapy
import re


class TiebaSpider(scrapy.Spider):
    name = "get_comment"
    start_urls = []
    for line in open('urls.txt'):
        start_urls.append(line)

    def parse(self, response):
        for comment in re.findall(r'd_post_content j_d_post_content  clearfix\">(.*?)<\/div>?', response.body):
            with open('comments.txt',"a") as f:
                f.write(comment + '\n')

        next_page = response.xpath('//a[@class="next pagination-item "]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)