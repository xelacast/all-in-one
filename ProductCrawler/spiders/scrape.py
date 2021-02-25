import re
import scrapy
import time

from scrapy.crawler import CrawlerProcess

#! NOTE on activating spiders outsite of the folder
# get the scrapy settings of the project you want to run and set them with CrawlerProcess or RunSpider


######* GAMESTOP SPIDER ######
class GameStop(scrapy.Spider):
    name = 'gamestop'
    url = 'https://www.gamestop.com/video-games/playstation-5/consoles'
    custom_settings = {
        "FEEDS": {
            "data/gamestop.csv": {"format": "csv"},
        },
    }
    headers = {
        'authority': 'www.gamestop.com',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,el;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'referer': 'https://www.gamestop.com/',
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            headers=self.headers,
            callback=self.parse,
        )

    def parse(self, response):
        for item in response.css('.product-grid-tile-wrapper'):

            product_description = item.css('.pd-name::text').get()
            product_price = item.css('span.actual-price').re(r'[0-9.]+')[0]
            product_url = 'https://www.gamestop.com' + \
                item.css('a.link-name::attr(href)').get()
            product_status = item.css('button.add-to-cart div::text').get()
            product_brand = 'Sony'
            product_website = 'gamestop'

            yield {
                'product_status': product_status,
                'product_description': product_description,
                'product_brand': product_brand,
                'product_url': product_url,
                'product_price': product_price,
                'product_site': product_website,
            }


######* NEWEGG SPIDER #######
class Newegg(scrapy.Spider):
    name = 'newegg'
    url = 'https://www.newegg.com/p/pl?N=100007709%20601357247'
    custom_settings = {
        "FEEDS": {
            "data/newegg.csv": {"format": "csv"},
        },
    }
    headers = {
        'authority': 'www.newegg.com',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,el;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'referer': 'https://www.newegg.com/tools/custom-pc-builder/pl/ID-48?N=601357282',
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            headers=self.headers,
            callback=self.parse,
        )

    def parse(self, response):
        for item in response.css('.item-container'):
            product_description = item.css('a.item-title::text').get()
            product_brand = product_description.split(' ')[0]
            product_status = item.css('button.btn::text').get()
            product_url = item.css('a.item-title::attr(href)').get()
            product_price = '$' + \
                item.css('li.price-current strong::text').get()
            product_price += item.css('li.price-current sup::text').get()
            product_site = 'newegg'
            # no product Sku

            yield {
                'product_status': product_status,
                'product_description': product_description,
                'product_brand': product_brand,
                'product_url': product_url,
                'product_price': product_price,
                'product_site': product_site,
            }


######* WALMART SPIDER ######
class Walmart(scrapy.Spider):

    name = 'walmart'
    start_urls = [
        'https://www.walmart.com/ip/PlayStation-5-Console/363472942',
        'https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815',
    ]
    custom_settings = {
        "FEEDS": {
            "data/walmart.csv": {"format": "csv"},
        },
    }
    headers = {
        'authority': 'www.walmart.com',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,el;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'referer': 'https://www.walmart.com/',
    }


# grab container that have the keyword console in them

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        product_description = response.css('h1.prod-ProductTitle::text').get()
        product_status = response.css('.prod-blitz-copy-message b::text').get()
        product_price = response.css('span.price span::text').re(r'[0-9.]+')[0]
        product_url = response.url
        product_brand = 'Sony'
        product_site = 'walmart'

        yield {
            'product_status': product_status,
            'product_description': product_description,
            'product_price': product_price,
            'product_url': product_url,
            'product_brand': product_brand,
            'product_site': product_site,
        }


######* BESTBUY SPIDER ######
class BestBuy(scrapy.Spider):
    name = 'bestbuy'
    start_urls = [
        # ps5 consoles
        'https://www.bestbuy.com/site/playstation-5/ps5-consoles/pcmcat1587395025973.c?id=pcmcat1587395025973',
        # pc components
        # blanked out right now to focus on one product
        # 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206900%20XT',
        'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090',
        # 'https://www.bestbuy.com/site/promo/amd-ryzen-5000'


    ]
    custom_settings = {
        "FEEDS": {
            "data/bestbuy.csv": {"format": "csv"},
        },
    }
    headers = {
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,el;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'referer': 'https://www.bestbuy.com/',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse,
            )
            time.sleep(1)

    def parse(self, response):

        for item in response.css('.sku-item'):
            product_status = item.css(
                ".add-to-cart-button::text").get()
            product_description = item.css(
                "a::text").get().replace('- ', '')
            product_brand = product_description.split(" ")[0]
            product_url = 'https://www.bestbuy.com' + \
                item.css('a::attr(href)').get()
            product_price = item.css(
                '.priceView-customer-price span::text').getall()[0]
            product_site = 'bestbuy'

            yield {
                'product_status': product_status,
                # 'product_title': item.css("a::text").get().replace('- ', ''),
                'product_description': product_description,
                'product_brand': product_brand,
                # 'product_sku': product_sku,
                'product_url': product_url,
                'product_price': product_price,
                'product_site': product_site,
            }
        next_page = response.css('a.sku-list-page-next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,
                                 headers=self.headers,
                                 callback=self.parse)


######* ACTIVATE CRAWL #######
# process = CrawlerProcess(
#     # "FEEDS": {
#     #     "data/myip.csv": {"format": "csv"},
#     # },
# )
# process.crawl(GameStop)
# process.crawl(Newegg)
# process.crawl(Walmart)
# process.crawl(BestBuy)
# process.start()
