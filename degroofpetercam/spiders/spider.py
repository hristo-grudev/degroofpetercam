import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import DegroofpetercamItem
from itemloaders.processors import TakeFirst


class DegroofpetercamSpider(scrapy.Spider):
	name = 'degroofpetercam'
	start_urls = ['https://press.degroofpetercam.lu/']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class,"story-card--with-date")]')
		for post in post_links:
			link = post.xpath('.//a/@href').get()
			date = post.xpath('.//span/text()').get()
			if date:
				date = re.findall(r"(\d+\s[a-zA-ZÀ-ÿ. ]+\s\d+)", date)[0]
			yield response.follow(link, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h2 | ancestor::p[@class="date"] | ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=DegroofpetercamItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
