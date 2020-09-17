from scrapy.spiders import Spider


import scrapy
from ..items import QuoteItem


class QuotesSpider(Spider):
    name = "tutorial_quotes"

    start_urls = ['http://lab.scrapyd.cn']

    # def start_requests(self):
    #     urls = [
    #         'http://lab.scrapyd.cn/page/1/',
    #         'http://lab.scrapyd.cn/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quote_elem = response.css('div.quote')

        for v in quote_elem:  # 循环获取每一条名言里面的：名言内容、作者、标签
            text = v.css('.text::text').extract_first()  # 提取名言
            author = v.css('.author::text').extract_first()  # 提取作者
            tags = v.css('.tags .tag::text').extract()  # 提取标签
            tags = ','.join(tags)  # 数组转换为字符串
            yield QuoteItem(text=text, author=author, tags=tags)

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


