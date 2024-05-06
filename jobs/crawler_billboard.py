import os
from multiprocessing import Process

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from billboard_chart.billboard_chart.spiders.billboard_chart_billboard200 import BillboardChartBillboard200Spider
from billboard_chart.billboard_chart.spiders.billboard_chart_global200 import BillboardChartGlobal200Spider
from billboard_chart.billboard_chart.spiders.billboard_chart_hot100 import BillboardChartHot100Spider
from billboard_chart.billboard_chart.spiders.billboard_chart_tiktoktop50 import BillboardChartTiktokTop50Spider

from config import settings as config_settings

settings = Settings({
    'BOT_NAME': "billboard_chart",
    'SPIDER_MODULES': ["billboard_chart.billboard_chart.spiders"],
    'NEWSPIDER_MODULE': "billboard_chart.billboard_chart.spiders",
    'ROBOTSTXT_OBEY': False,
    'ITEM_PIPELINES': {
        "billboard_chart.billboard_chart.pipelines.BillboardChartPipeline": 300,
        "billboard_chart.billboard_chart.pipelines.SongMongoDBWriterPipeline": 400,
        "billboard_chart.billboard_chart.pipelines.JsonWriterPipeline": 500,
        "billboard_chart.billboard_chart.pipelines.RankingMongoDBWriterPipeline": 600,
        "billboard_chart.billboard_chart.pipelines.PlaylistMongoDBWriterPipeline": 700,

    },
    'MONGO_URI': config_settings.MONGO_URI,
    'MONGO_DATABASE': config_settings.MONGO_MUSIC_CHARTS_DBNAME,
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': "2.7",
    'FEED_EXPORT_ENCODING': "utf-8"
})

runner = CrawlerRunner(settings=settings)
configure_logging(settings)


def billboard_chart_hot100_crawler():
    process_crawl(BillboardChartHot100Spider)


def billboard_chart_billboard200_crawler():
    process_crawl(BillboardChartBillboard200Spider)


def billboard_chart_global200_crawler():
    process_crawl(BillboardChartGlobal200Spider)


def billboard_chart_tiktoktop50_crawler():
    process_crawl(BillboardChartTiktokTop50Spider)


def process_crawl(spider: scrapy.Spider):
    configure_logging(settings=settings)
    p = Process(target=crawl, args=([spider]))
    p.start()
    p.join()


def crawl(spider: scrapy.Spider):
    d = runner.crawl(spider)
    # d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    process_crawl(BillboardChartHot100Spider)
