# -*- coding: utf-8 -*-
import scrapy


class Article(scrapy.Item):
    item_id = scrapy.Field(default='')
    date = scrapy.Field(default='')
    type = scrapy.Field(default='')
    category = scrapy.Field(default='')
    main_story = scrapy.Field(default='')
    title = scrapy.Field(default='')
    ingress = scrapy.Field(default='')
    authors = scrapy.Field(default='')
    text = scrapy.Field(default='')
    urls = scrapy.Field(default='')
    article_pictures = scrapy.Field(default='')



class Image(scrapy.Item):
    item_id = scrapy.Field(default='')
    url = scrapy.Field(default='')
    picture_text = scrapy.Field(default='')
