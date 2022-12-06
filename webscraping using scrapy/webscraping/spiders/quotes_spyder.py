import scrapy
from ..items import QuotesItem

class QuotesSpyder(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://bluelimelearning.github.io/my-fav-quotes/'
    ]
    
    def parse(self, response):
        items = QuotesItem()
        for quotes in response.css("div.quotes"):
            qt ="".join(quotes.css(".aquote::text").extract())
            items['quotes'] = qt.strip()
            items['author'] = quotes.css(".author::text").extract_first().strip()
            
            yield items