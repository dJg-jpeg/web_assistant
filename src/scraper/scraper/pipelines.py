# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraperPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item


class ScraperNPipeline(object):
    """
    Removes signs from the price value. i.e replaces 10000/= with 10000
    """
    def process_item(self, item, spider):
        if item.get('title'):
            item['title'] = item['title'].replace('\n', '')
            return item