from urllib.parse import urlsplit
import time

# aws_scraper = AWSScraper(15)

# links = aws_scraper.get_product_links()

# page = aws_scraper.process(links[0])

# print(links[0:3])



class AWSProductCrawler:
    def __init__(self, chroma, scraper):
        self.politenessInterval = 10
        self.crawled = []
        self.allowed = []
        self.disallowed = []
        self.aws_scraper = scraper
        self.chroma = chroma
        self.links = self.aws_scraper.get_product_links()
    

    def checkAllowed(self, link):
        return True
        
    def crawl(self, pages=300):
        
        for link in self.links:
            if link not in self.crawled:

                if len(self.crawled) > pages:
                    break
                self.crawled.append(link)
                yield self.aws_scraper.process(link)
                time.sleep(2)

    def populateIndex(self, limit=300):

        
        for url, page in self.crawl(limit):
            self.chroma.add(url, page)

