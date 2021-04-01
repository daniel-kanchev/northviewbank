import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from northviewbank.items import Article
import requests
import json
import re


class northviewbankSpider(scrapy.Spider):
    name = 'northviewbank'
    start_urls = ['https://northviewbank.myhomehq.biz/v2/newsletters']

    def parse(self, response):
        json_response = json.loads(requests.get("https://northviewbank.myhomehq.biz/v2/newsletters").text)
        articles = json_response['data']['newsletters']
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article['campaign']['name']
            date = article['campaign_date']
            link = response.urljoin(article['campaign']['url'])
            content = article['campaign']['content']

            cleanr = re.compile('<.*?>')
            content = re.sub(cleanr, '', content).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('link', link)
            item.add_value('content', content)

            yield item.load_item()
