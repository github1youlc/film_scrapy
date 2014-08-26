from scrapy.item import Field, Item

class FilmItem(Item):
	url = Field()
	name = Field()
	director = Field()
	scenarist = Field()
	actors = Field()
	type = Field()
	area = Field()
	language = Field()
	releaseDate = Field()
	length = Field()
	alias = Field()
	rate = Field()
	description = Field()
	sub_id = Field()
	img_path = Field()
	img_url = Field()

