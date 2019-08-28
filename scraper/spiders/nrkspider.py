from scrapy.spiders import SitemapSpider
from scrapy.selector import Selector
from scraper.items import Article, Image
import pandas as pd

def articleurl_to_category(url):
    split_url = url.split('/')
    if len(split_url)<4:
        return ""
    return split_url[3]

def articleurl_to_id(url):
    if('nrk' not in url):
        return url

    split_url = url.split('.')
    split_url = split_url[len(split_url)-1]

    if not split_url.isdigit():
        return url

    return split_url

def pictureurl_to_id(url):
    split_url = url.split('/')
    return split_url[len(split_url)-1]

class nrksitemapcounter(SitemapSpider):
	name = 'nrk_sitemapcounter'
	itemap_urls = ['https://www.nrk.no/sitemap.xml']

	def parse(self, response):
		id = articleurl_to_id(url)
		with open('sitemap_ids.csv', 'a+') as f:
		        f.write(str(id))
		        f.write('\n')

class nrkspider(SitemapSpider):
    name = 'nrk_spider'
    sitemap_urls = ['https://www.nrk.no/sitemap.xml']
    allowed_domains = ['nrk.no']
    parsed_urls_path = 'parsed_urls.csv'
    parsed_urls = pd.read_csv(parsed_urls_path)
    counter = 0
    parsed_ids = []
    write_limit = 10



    def parse(self, response):
        url = response.request.url
        id = articleurl_to_id(url)
        if id in self.parsed_urls:
            return

        article = Article()
        article['item_id'] = id
        article['category'] = articleurl_to_category(url)

        article_selectors = response.xpath("(//article[contains(@class, 'article') and contains(@role, 'main')])[1]")
        bulletin_selectors = response.xpath("(//article[contains(@class, 'bulletin')])[1]")


        self.counter += 1


        if len(article_selectors) > 0:
            items, hasText = self.parse_article(article_selectors, article)
        elif len(bulletin_selectors)>0:
            items, hasText = self.parse_bulletin(bulletin_selectors, article)
        else:
            self.log("Type of url not found: " + url)
            return


        if self.counter > self.write_limit:
            self.save_ids()
            self.counter = 0

        if hasText:
            self.parsed_ids.append(str(id))
            return items
        else:
            with open('failed_ids.csv', 'a+') as f:
                f.write(str(id))
                f.write('\n')



    def parse_article(self, selectors, article):
        selector = selectors[0]
        article['type'] = "Article"
        items = [article]

        titles = selector.xpath("//header/h1/text()").extract()
        if len(titles) != 0:
            article['title'] = titles[0]


        ingresses = selector.xpath("//header/div[contains(@itemprop, 'description')]//p/text()").extract()
        if len(ingresses) != 0:
            article['ingress'] = ingresses[0]

        article['authors'] = selector.xpath("//a[contains(@class, 'author__name')]/text()").extract()

        dates = selector.xpath("//time[contains(@itemprop, 'datePublished')]/@datetime").extract()
        if len(dates) != 0:
            article['date'] = dates[0]

        article['text'] = selector.xpath("//div[contains(@itemprop,'articleBody')]/*[name()!='div']//text()").extract()

        hasText = len(article['text'])>0
        article_urls = selector.xpath("//div[contains(@itemprop,'articleBody')]/*[name()!='div']//@href").extract()
        article_urls = [articleurl_to_id(url) for url in article_urls]
        article['urls'] = article_urls



        image_ids = set(selector.xpath("//img/@id").extract())
        article['article_pictures'] = image_ids
        for image_id in image_ids:
            img = self.extract_img(selector, image_id, article)
            items.append(img)

        return items, hasText



    def parse_bulletin(self, selectors, article):
        selector = selectors[0]
        article['type'] = "Bulletin"
        article['title'] = selector.xpath("//div[contains(@class, 'text-body')]/h2/text()").extract()[0]
        article['text'] = selector.xpath("//div[contains(@class, 'text-body')]/p/text()").extract()
        article['article_pictures'] = []
        hasText = len(article['text'])>0


        try:
            article['date'] = selector.xpath("//div[contains(@class, 'text-body')]/time/@datetime").extract()[0]
            article['main_story'] = selector.xpath("//a[contains(@class,'compilation')]/text()").extract()[0]
        except:
            self.log("Error while parsing:" + article['item_id'])

        return article, hasText


    def extract_img(self, selector, image_id, article):
        img = Image()
        img['item_id'] = image_id
        try:
            image_text =  ''.join(selector.xpath("(//img[@id='" + image_id +"'])[1]/../../figcaption//text()").extract())
            img['picture_text'] = image_text
            src = selector.xpath("(//img[@id='" + image_id +"'])[1]/@srcset").extract()[0].split(' ')[0]
            img['url'] = pictureurl_to_id(src)
        except:
            self.log( "Error while parsing image: " + article['url'])

        return img

    def sitemap_filter(self, entries):
            for entry in entries:
                url = entry['loc']
                if articleurl_to_id(url) in self.parsed_urls:
                    continue
                yield entry

    def save_ids(self):
        with open(self.parsed_urls_path, 'a+') as f:
            for id in self.parsed_ids:
                f.write(id)
                f.write('\n')
        self.parsed_ids = []


# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
