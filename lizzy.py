import os
import json
import requests
import codecs
from scrapy.selector import Selector

class LizzySpider():
    def __init__(self):
        self.filename = 'source_page.html'

    def log(self, entry):
        filename = 'data.csv'
        try:
            file = open(filename, 'a')
        except IOError:
            file = open(filename, 'w')
        json.dump(entry, file)
        file.write(os.linesep)
        file.close()

    def get_source(self):
        url = "https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=antique&rt=nc&LH_Auction=1"
        source_code = requests.get(url)
        plaintext = source_code.text

        with open(self.filename, 'wb') as f:
            f.write(plaintext.encode("UTF-8"))
            f.close()
        print 'Saved file: ' + self.filename

    def select_info(self, text):
        price = Selector(text=text).xpath('//li[@class=$val]/span/text()', val='lvprice prc').extract_first()
        title = Selector(text=text).xpath('//h3[@class=$val]/a/text()', val='lvtitle').extract_first()
        no_bids = Selector(text=text).xpath('//li[@class=$val]/span/text()', val='lvformat').extract_first()
        unit = Selector(text=text).xpath('//li[@class=$val]/span/b/text()', val='lvprice prc').extract_first()

        # Create a dictionary to store the scraped info
        scraped_info = {
            'product_title' : title,
            'product_bids' : no_bids,
            'price_unit' : unit,
            'product_price' : price,
        }
        # log entry to a log file
        self.log(scraped_info)

    def scrap(self):
        self.get_source()
        file = open(self.filename, 'r')
        text = file.read()
        self.select_info(text)


test = LizzySpider()
test.scrap()
