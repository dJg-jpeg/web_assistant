from django.core.management.base import BaseCommand
from src.scraper.scraper.spiders.dw import DwSpider
from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

from scrapy.settings import Settings
from src.scraper.scraper import settings as my_settings


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        # process = CrawlerProcess(get_project_settings())
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)

        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(DwSpider)
        process.start()
