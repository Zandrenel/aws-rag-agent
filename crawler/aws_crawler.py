from urllib.parse import urlsplit

import time



class AWSProductCrawler:
    def __init__(self, chroma, scraper):
        self.politenessInterval = 10        
        self.crawled = []
        
        self.aws_scraper = scraper
        self.chroma = chroma
        self.allowed, self.disallowed = self.aws_scraper.parse_robots()
        self.links = self.aws_scraper.get_product_links()
        self.maxDepth = 3
        
        
    def checkAllowed(self, link):
        splitLink = urlsplit(link)        
        return not splitLink.path in self.disallowed

    def sameBase(self, link):
        splitLink = urlsplit(link)
        splitBase = urlsplit(self.aws_scraper.baseUrl)
        
        return splitLink.hostname == splitBase.hostname
            
    def crawl(self, pages=1000):
        
        for link in self.links:
            crawlStart = time.time()
            if link[1] not in self.crawled:

                if len(self.crawled) > pages:
                    break

                if link[0] <= self.maxDepth and self.checkAllowed(link[1]) and self.sameBase(link[1]):
                    
                    while time.time() - crawlStart < 2:
                        time.sleep(.1)
                        pass
                    
                    sublinks, path, text_blocks = self.aws_scraper.process(link[1])
                    self.crawled.append(link[1])

                    for link in sublinks:
                        if link[1] not in self.crawled:
                            self.links.append(link)                
                    print(f"Links Length: {len(self.links)}")
                    print(f"{time.strftime("%H:%M:%S")}: Crawled {len(self.crawled)} Pages so far")

                    for key, value in text_blocks.items():                                           
                        yield f"{path}-{key}", value




    def populateIndex(self, limit=3000):
        
        for url, page in self.crawl(limit):
            self.chroma.add(url, page)

if __name__ == '__main__':
    from aws_scraper import AWSScraper
    aws_scraper = AWSScraper(5)
    crawler
    links = aws_scraper.get_product_links()

    page = aws_scraper.process(links[0][1])
        
    # print(links[0:3])
