import os
import json
import requests
import codecs
from scrapy.selector import Selector
'''
# Objectives: find profitable auctions on ebay.com antiques
# Project funtions:
    * (InProgress) Turn search pages automatically.
    * (Pending) Able to set selector conditions, example: bids_no > 100.
    * (Checked) Dump the scraped results.
    * (Checked) Scrape the selected keywords from a page given an URL.
'''



class LizzySpider():
    def __init__(self):
        # Search target.
        self.target = "antique"
        # Number of pages to be crawl.
        self.scope = 5

    def log(self, entry):
        filename = 'data.json'
        try:
            file = open(filename, 'a')
        except IOError:
            file = open(filename, 'w')
        json.dump(entry, file, indent=1)
        file.write(os.linesep)
        file.close()

    def select_info(self, text):
        price = Selector(text=text).xpath('//li[@class=$val]/span/text()', val='lvprice prc').extract()
        title = Selector(text=text).xpath('//h3[@class=$val]/a/text()', val='lvtitle').extract()
        no_bids = Selector(text=text).xpath('//li[@class=$val]/span/text()', val='lvformat').extract()
        unit = Selector(text=text).xpath('//li[@class=$val]/span/b/text()', val='lvprice prc').extract()

        # need a better way to organize output entries!!! help needed
        # Create a dictionary to store the scraped info
        scraped_info = {
            'product_title' : title,
            'product_bids' : no_bids,
            'price_unit' : unit,
            'product_price' : price,
        }

        # log entries to a log file
        self.log(scraped_info)

    def gen_page(self, page_no):
        """
        Generate urls for each pages, page_number should less than the maximum pages
        """
        if page_no is 1:
            next_page = ""
            print next_page
        else:
            next_page = "&_pgn=" + str(page_no)
            print next_page

        target = self.target
        url = "https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_Auction=1&_nkw={target}&rt=nc{next_page}"
        # url = "https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_Auction=1&_nkw=antique&rt=nc"
        source_code = requests.get(url)
        plaintext = source_code.text
        return plaintext

    def get_source(self):
        """
        crawl pages one by one
        """
        for page_no in xrange(self.scope):
            plaintext = self.gen_page(page_no+1)
            self.select_info(plaintext)

        # This part were used to download pages and store as a html file.
        # with open(self.filename, 'wb') as f:
        #     f.write(plaintext.encode("UTF-8"))
        #     f.close()
        # print 'Saved file: ' + self.filename

    def scrap(self):
        self.get_source()

        # This part were used to download pages and store as a html file.
        # file = open(self.filename, 'r')
        # text = file.read()
        # self.select_info(text)


test = LizzySpider()
test.scrap()
