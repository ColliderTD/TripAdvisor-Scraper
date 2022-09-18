import scrapy
from ..items import RestaurantResultItem

class ResultSpider(scrapy.Spider):
    name = 'result'
    allowed_domains = ['www.tripadvisor.com.br']
    start_urls = ['https://www.tripadvisor.com.br/{page}']
    current_page = 1
    max_pages = 0

    custom_settings = {
        'FEEDS' : {
            'output/search_results.json': {
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
        self.start_urls[0] = self.start_urls[0].replace("{page}", kwargs['page'])
        print(f"Starting scraping : {self.start_urls[0]}")
        print("")
    
    def parse(self, response):
        print(f"HTTP STATUS : {response.status}")
        self.current_page = int(response.css("span.pageNum.current::attr(data-page-number)").get())
        restaurant_list = response.css("div.YHnoF")

        print(f"Current Page : {str(self.current_page)} ")
        print("")

        for restaurant_result in restaurant_list:
            item = RestaurantResultItem()
            item['title'] = restaurant_result.css("a.Lwqic::text")[2].get()
            item['page_link'] = restaurant_result.css("a.Lwqic::attr(href)").extract()[0]

            print(f"Restaurant : {item['title']}")
            print(f"Link : {item['page_link']}")
            print("")
            yield(item)

        next_page = response.css(f"a.pageNum.taLnk[data-page-number='{self.current_page+1}']::attr(href)").get()

        if (next_page):
            if (self.max_pages):
                if (self.current_page >= self.max_pages):
                    return

            yield scrapy.Request(response.urljoin(next_page), self.parse)

            print("Going to next page...")
            print("")