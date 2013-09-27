#coding: utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from web_content_catch.items import WebContentCatchItem 
from web_content_catch.pipelines import WebContentCatchPipeline
import re

web_regular = re.compile('\s*www.amazon.cn\s*')
product_regular = re.compile('\s*/(B00\w{7})/\s*')
pipeline = AmazonProductPipeline()

class AmazonProductSpider(BaseSpider):
    name = "wenweipo"
    allowed_domains = ["bbs.wenweipo.com"]
    start_urls = [
            "http://bbs.wenweipo.com/",
    ]
    count = 0
    used_url = set()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        
        newurls = hxs.select('//a/@href').extract()
        validurls = []
        for url in newurls:
            p = web_regular.search(url)
            if not p:
                continue
            validurls.append(url)

            product_search = product_regular.search(url)
            if not product_search:
                continue
            for product in product_search.groups():
                if product:
                    self.count += 1
                    print 'product: ', product
                    print 
                    print 
                    print 
                    print 
                    item = AmazonProductItem()
                    item['product'] = product
                    pipeline.process_item(item, None)

        for url in validurls:
            if self.count < 20000 and not self.used_url.issuperset([url]):
                self.used_url.add(url)
                yield self.make_requests_from_url(url)
            else:
                return
                


