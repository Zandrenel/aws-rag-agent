import requests, json
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

class AWSScraper:
    def __init__(self, products=264):
        self.raw_data = ""
        # self.driver = seleniumDriver
        self.productListURL = f"https://aws.amazon.com/api/dirs/items/search?item.directoryId=products-cards-interactive-aws-products-ams&item.locale=en_US&tags.id=GLOBAL%23local-tags-aws-products-type%23service%7CGLOBAL%23local-tags-aws-products-type%23feature&sort_by=item.additionalFields.title&sort_order=asc&size={products}"
        self.productURLs = []
        self.baseUrl = "https://aws.amazon.com/"
        
    #https://aws.amazon.com/products/
    def get_product_links(self):
        rawProducts = requests.get(self.productListURL)
        products = json.loads(rawProducts.text)

        self.productURLs = []
        for item in products["items"]:
            url = item["item"]["additionalFields"]["ctaLink"]

            newurl = urlsplit(url, scheme=None, allow_fragments=False)
            
            try:
                finalurl = "https://" + newurl.netloc + newurl.path
                self.productURLs.append((1, finalurl))
            except CantParseURL:
                print(f"{url} could't be parsed")

        return self.productURLs

    def parse_robots(self):
        robots = requests.get("https://aws.amazon.com/robots.txt")

        allowed = []
        disallowed = []
        
        for line in robots.text.split("\n"):
            parts = line.split(":")
            if parts[0] == "Allow":
                allowed.append(parts[1][:len(parts[1])-1])
            elif parts[0] == "Disallow":
                disallowed.append(parts[1][:len(parts[1])-1])

        return allowed, disallowed
    
    def process(self, url, level=1):
        
        rawPage = requests.get(url)
        
        soup = BeautifulSoup(rawPage.text, 'html.parser')
                
        def get_description(block):
            return block.h2 and not block.h2.text == "Did you find what you were looking for today?" and not block.h2.text == "Learn" and block.h2.has_attr('data-rg-n') and block.div and block.div.has_attr('data-rg-n')

        def get_sub_link(block):
            return block.has_attr('href') and block.has_attr('data-rg-n')
        
        # content_blocks = soup.find_all("div")
        content_blocks = soup.find_all(get_description)
        unique_descriptions = {}
        for block in content_blocks:
            unique_descriptions[block.h2.text] = block.div.text

        sublink_blocks = soup.find_all(get_sub_link)
        sublinks = [(level+1, link['href']) for link in sublink_blocks]
            
        return sublinks, url, unique_descriptions #rawPage.text



