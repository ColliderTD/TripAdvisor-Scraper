import scrapy
import base64
from ..items import PageItem

class PageSpider(scrapy.Spider):
    name = "page"
    allowed_domains = ['www.tripadvisor.com.br']
    start_urls = []

    custom_settings = {
        'FEEDS' : {
            'output/page_results.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 4,
                'overwrite' : True
            }
        }
    }

    def __init__(self, **kwargs):
        super().__init__(self.name, **kwargs)

        if (kwargs.get('pages')):
            self.start_urls = [ "https://"+self.allowed_domains[0]+x for x in kwargs["pages"] ]

    def parse(self, response):
        item = PageItem()

        name = response.css(".HjBfq::text").get()
        address = response.css("span.cNFrA:nth-child(1) > span:nth-child(1) > a:nth-child(2)::text").get()
        phone = response.css("span.AYHFM > a:nth-child(1)::text").get()

        site_encoded_url = response.css("span.cNFrA:nth-child(3) > span:nth-child(1) > a:nth-child(2)::attr(data-encoded-url)").get()
        site = None

        if (site_encoded_url):
            site = base64.b64decode(site_encoded_url).decode('utf8')

        menu_encoded_url = response.css("span.DsyBj:nth-child(4) > a:nth-child(2)::attr(data-encoded-url)").get()
        menu = None

        if (menu_encoded_url):
            menu = base64.b64decode(menu_encoded_url).decode('utf8')

        if (site):
            site = site[4:][:-4]
        
        if (menu):
            menu = menu[4:][:-4]

        punctuation = response.css(".ZDEqb::text").get()
        price = response.css(".BMlpu > div:nth-child(1) > div:nth-child(2)::text").get()
        
        if (price):
            price = price.replace('\xa0', '')

        print(
        f"Page : {response.url}",
        f"Name : {name}",
        f"address : {address}",
        f"site : {site}",
        f"menu : {menu}",
        f"punctuation : {punctuation}",
        f"price : {price}",
        "",
        sep='\n'
        )

        item['name'] = name
        item['address'] = address
        item['phone'] = phone
        item['site'] = site
        item['menu'] = menu
        item['punctuation'] = punctuation
        item['price'] = price

        yield item