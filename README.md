# NRK news article scraper
Scrapes and saves all historical news articles from the NRK. NRK is the main norwegian public broadcaster. https://www.nrk.no/
The spider utilizes the sitemap to find articles, and then uses the regular structure of the articles to extract information on text and pictures. 

The spider is built on the python framework Scrapy. 

## Running scraper
In project folder run:
```console
scrapy crawl nrk_spider
```
