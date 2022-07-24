from gc import callbacks
import scrapy
from whiskeyscraper.items import WhiskeyscraperItem
from scrapy.loader import ItemLoader


class WhiskeySpider(scrapy.Spider):
    name = 'whiskey'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky/all?item_availability=In+Stock']

    def parse(self, response):

        for products in response.css('div.product-item-info'):

            l = ItemLoader(item = WhiskeyscraperItem(), selector = products)

            l.add_css('name','a.product-item-link')
            l.add_css('price','span.price')
            l.add_css('link','a.product-item-link::attr(href)')

            yield l.load_item()
            

        next_page = response.css('a.action.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback= self.parse)