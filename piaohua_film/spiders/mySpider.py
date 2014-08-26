from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from MyUtil import unicode_to_utf8
import Item

class FilmSpider(CrawlSpider):
	name = 'piaohua_film'
	allowed_domains = ['www.piaohua.com']
	start_urls = ['http://www.piaohua.com']
	rules = (Rule(SgmlLinkExtractor(allow=('html/(.*)/\d+/\d+/\d+\.html',)), callback='parse_item', follow=True),)

	def parse_item(self, response):
		print response.url
		item = Item.PiaohuaItem()
		item['name'] = unicode_to_utf8(response.xpath('//*[@id="show"]/h3').extract())
		item['images'] = response.xpath('//*[@id="showdesc"]/img/@src').extract()
		item['info'] = unicode_to_utf8(response.xpath('//*[@id="showinfo"]/p[1]').extract())
		print item['info']
		return item
		
