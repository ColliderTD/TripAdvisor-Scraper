from scrapy.signalmanager import dispatcher
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy import signals

from tripadvisor_scrapper.items import PageItem
from tripadvisor_scrapper.spiders.result import ResultSpider
from tripadvisor_scrapper.spiders.page import PageSpider
SEARCH_PAGE = "Restaurants-g60745-Boston_Massachusetts.html"
MAX_SEARCH_PAGES = 10

def main():
    print("Starting TripAdvisor scraper.")
    print("")

    settings = get_project_settings()
    settings.set("LOG_ENABLED", True)
    settings.set("LOG_LEVEL", "DEBUG")
    runner = CrawlerRunner(settings=settings)

    data ={
        "page_results" : [],
        "pages_count" : 0
    }

    def on_error(err):
        print("ERROR : ", err)

    def get_results(signal, sender, item, response, spider):
        if type(spider) == ResultSpider:
            data['page_results'].append(item)
        if type(spider) == PageSpider:
            data['pages_count'] += 1

    def on_finish_pages(none):
        reactor.stop()
        pages_count = data["pages_count"]
        print(f"Finished, scraped ({pages_count}) Page(s)")

    def on_search_result(result):
        # Run pages scraper
        d = runner.crawl(PageSpider, pages=[x['page_link'] for x in data["page_results"]])
        d.addErrback(on_error)
        d.addCallback(on_finish_pages)
    
    dispatcher.connect(get_results, signal=signals.item_scraped)

    deferred = runner.crawl(ResultSpider, page=SEARCH_PAGE, max_pages=MAX_SEARCH_PAGES)
    deferred.addCallback(on_search_result)
    deferred.addErrback(on_error)

    reactor.run()  # the script will block here until all crawling jobs are finished

main()