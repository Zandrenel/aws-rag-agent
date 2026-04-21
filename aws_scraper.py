import requests, json
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

class AWSScraper:
    def __init__(self, products=264):
        self.raw_data = ""
        # self.driver = seleniumDriver
        self.productListURL = f"https://aws.amazon.com/api/dirs/items/search?item.directoryId=products-cards-interactive-aws-products-ams&item.locale=en_US&tags.id=GLOBAL%23local-tags-aws-products-type%23service%7CGLOBAL%23local-tags-aws-products-type%23feature&sort_by=item.additionalFields.title&sort_order=asc&size={products}"
        self.productURLs = []
        
    #https://aws.amazon.com/products/
    def get_product_links(self):
        rawProducts = requests.get(self.productListURL)
        products = json.loads(rawProducts.text)

        self.productURLs = []
        for item in products["items"]:
            url = item["item"]["additionalFields"]["ctaLink"]
            # print(json.dump(item["item"], indent=2))
            newurl = urlsplit(url, scheme=None, allow_fragments=False)
            
            try:
                finalurl = "https://" + newurl.netloc + newurl.path
                self.productURLs.append(finalurl)
            except CantParseURL:
                print(f"{url} could't be parsed")


        return self.productURLs

    def process(self, url):
        rawPage = requests.get(url)

        return url, rawPage.text



