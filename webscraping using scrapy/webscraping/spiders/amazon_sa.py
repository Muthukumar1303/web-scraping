import random

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from ..items import AmazonSaItem

from scraper_api import ScraperAPIClient
client = ScraperAPIClient('7a7cc7a54995ef27d0bc0ac3d69e8a56')

class AmazonSaSpyder(scrapy.Spider):
    name = "amazon_sa"
    start_urls = [
        # 'https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A172456&qid=1670150590&ref=sr_pg_301',
        # 'https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A193870011&ref=nav_em__nav_desktop_sa_intl_computer_components_0_2_6_3',
        'https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A3011391011&ref=nav_em__nav_desktop_sa_intl_laptop_accessories_0_2_6_7'
        ]

    # rules = (
    #     Rule(LinkExtractor(),
    #          callback='parse_page',
    #          # hook to be called when this Rule generates a Request
    #          process_request='add_errback'),
    # )
    user_agents =[
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/62.0.3202.89 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
]
    # # this is just to no retry errors for this example spider
    # custom_settings = {
    #     'RETRY_ENABLED': False
    # }
    
    def parse(self, response):
        user_agent = self.user_agents[random.randint(0, len(self.user_agents)-1)]
        headers={
                    'USER_AGENT':user_agent
                }
        if response.status == 200 :
            items = AmazonSaItem()
            # items={}
            for card in response.css(".s-card-border"):
                items['image_path'] = card.css(".s-image").css("img").xpath("@src").extract_first()
                items['product_name'] = "".join(card.css(".a-text-normal::text").extract()).strip()
                items['product_price'] = "".join(card.css(".s-underline-text::text").extract()).strip().split(" ")[0]
                items['ratings'] = "".join(card.css(".aok-align-bottom ").css("i").css("span::text").extract()).strip()
                # yield items
                card_info = card.css(".a-text-normal").xpath("@href").extract_first()
                # yield response.follow(url=card_info, callback= self.parse_card,headers=headers , dont_filter = True, meta=items)
            
            next_page = response.css(".s-pagination-next").css("a").xpath("@href").get()
            if next_page:                
                yield response.follow(url=response.url, callback= self.parse,headers=headers , dont_filter = True)

    
    # def parse_card(serlf, response):
    #     items = AmazonSaItem()
    #     meta=response.meta
    #     for key, value in meta.items():
    #         if key in ["image_path","product_name","product_price","ratings"]:
    #             items[key] = value
    #     yield items