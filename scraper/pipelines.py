# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class ScraperPipeline(object):
    def process_item(self, item, spider):
        return item
class ItemWriterPipeline(object):

    def open_spider(self, spider):
        self.article_csv = open('out_articles.csv', 'a+', encoding = 'utf-8')
        self.image_csv = open('out_image.csv', 'a+', encoding = 'utf-8')

        self.article_writer = csv.writer(self.article_csv)
        self.image_writer = csv.writer(self.image_csv)



    def close_spider(self, spider):
        self.article_csv.close()
        self.image_csv.close()


    def process_item(self, item, spider):
        if 'type' in item.keys():
            self.article_writer.writerow(item.values())
        elif 'picture_text' in item.keys():
            self.image_writer.writerow(item.values())

        return item
