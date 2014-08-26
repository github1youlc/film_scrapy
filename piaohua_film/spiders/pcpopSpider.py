# coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import random
import urllib
import re
import scrapy
from MyUtil import unicode_to_utf8,strArray_to_str
import Item
from DBHelper import insert_film, is_url_not_crawled
import MyLogger

log = MyLogger.log
img_path_pre = '/mnt/hgfs/film_pic/'

class PopSpider(CrawlSpider):
	name = 'pop_film'
	allowed_domains = ['movie.pcpop.com']
	start_urls = ['http://movie.pcpop.com/']
	rules = (Rule(SgmlLinkExtractor(allow=('t\d+_\d+\.html',))),
			Rule(SgmlLinkExtractor(allow=('\d+_\d+_\d+_\d+\.html',)), callback='parse_item', follow=True),)

	def parse_item(self, response):
		print response.url
		item = Item.FilmItem()
		m = re.match('http://movie\.pcpop\.com/(\d+_\d+_\d+_\d+)\.html', response.url)
		if m == None or m.groups()[0] == None:
			log.error("Not expected url")
			return item
		sub_id = m.groups()[0]
		if (not is_url_not_crawled(sub_id)):
			log.info("aready crawled")
			return item
	#	item['name'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[1]/div/text()').extract())
		item['name'] = unicode_to_utf8(response.xpath('/html/body/center/div[6]/div/div/b/text()').extract())
		item['img_url'] =  unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[1]/div[1]/img/@src').extract())
		item['alias'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[2]/text()').extract())
		item['director'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[2]/a/text()').extract())
		if item['director'] == '':
			item['director'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[2]/text()').extract())
		item['scenarist'] = item['director']
		item['actors'] = unicode_to_utf8(strArray_to_str(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[2]//a[re:test(@class, "one")]/text()').extract(), u','))
		item['area'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[4]/div[2]/text()').extract())
		item['language'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[5]/div[2]/text()').extract())
		item['type'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[6]/div[2]/a/text()').extract())
		item['releaseDate'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[7]/div[2]/text()').extract())
		item['length'] = unicode_to_utf8(response.xpath('/html/body/center/div[7]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[8]/div[2]/text()').extract()) 
	#	item['rate'] = unicode_to_utf8(response.xpath('//iframe["@id=frame1"]/descendant::td[re:test(@align, "left")]/span/span/text()').extract())
		# for rate is got dynamicly, it can not to crawled, so use random rate
		item['rate'] = str(float(random.randrange(60,99,1))/10)
		item['description'] = unicode_to_utf8(response.xpath('//div[re:test(@class, "movb42")]/descendant::text()').extract())
		item['sub_id'] = sub_id
		item['img_path'] = img_path_pre + sub_id + '.jpg'
		urllib.urlretrieve(item['img_url'], item['img_path'])
#		print item['name']
#		print item['director']
#		print item['scenarist']
#		print item['actors']
#		print item['type']
#		print item['area']
#		print item['language']
#		print item['releaseDate']
#		print item['length']
#		print item['alias']
#		print item['rate']
#		print item['description']
#		print item['sub_id']
		insert_film(item)
		return item
