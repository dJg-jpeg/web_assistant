import scrapy
from scraper.scraper.items import NewsListItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class DwSpider(scrapy.Spider):
    name = 'dw'
    allowed_domains = ['dw.com']
    start_urls = ['https://www.dw.com/uk/%D0%BD%D0%BE%D0%B2%D0%B8%D0%BD%D0%B8/s-32419']

    # rules = (
    #     Rule(
    #         LinkExtractor(allow=("https://www.dw.com/uk/%D0%BD%D0%BE%D0%B2%D0%B8%D0%BD%D0%B8/s-32419'")),
    #         callback="parse",
    #         follow=True,
    #     ),
    # )


    def parse(self, response):
        I = ItemLoader(item = NewsListItem(),response=response)
        I.default_output_processor = TakeFirst()

        I.add_xpath('link', '//div[@class="news nocontent"]/a/@href')
        I.add_xpath('title', '//div[@class="news nocontent"]/a/h2/text()')
        I.add_xpath('date_of_news', '//div[@class="news nocontent"]/a/h2/span[@class="date"]/text()')


        yield I.load_item()

    # title = response.xpath('//div[@class="news nocontent"]/a/h2/text()').extract()
    # date_of_news = response.xpath('//div[@class="news nocontent"]/a/h2/span[@class="date"]/text()').extract()
    # import csv
    # def __init__(self):
    #     self.outfile = open("output.csv", "w", newline="", encoding='UTF-8')
    #     self.writer = csv.writer(self.outfile)
    # self.writer.writerow([links, title, date_of_news])
    # yield {
    #     'links' : links,
    #     'titles' : title,
    #     'time_news' : date_of_news
    # }
    # def closed(self,reason):
    #     self.outfile.close()

    #
    # item['link'] = links
    # item['title'] = title
    # item['date_of_news'] = date_of_news