import scrapy
import json
import re
import csv
import requests
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

import pdb

class Costco(scrapy.Spider):
    name = "costco"

    domain = "http://www.costco.com/"
    start_urls = ["http://www.aaronbrothers.com/store_locator/?zipcode=85250&distance=10000000000&commit=Find"]
    store_id = []

    def __init__(self):
        ca_json = open('cities_us.json', 'rb')
        self.city_list = json.load(ca_json)

    def start_requests(self):
        for city in self.city_list:
            request_url = "https://www.costco.com/AjaxWarehouseBrowseLookupView?langId=-1&storeId=10301&numOfWarehouses=10&hasGas=false&hasTires=false&hasFood=false&hasHearing=false&hasPharmacy=false&hasOptical=false&hasBusiness=false&tiresCheckout=0&isTransferWarehouse=false&populateWarehouseDetails=true&warehousePickupCheckout=false&latitude="+str(city["latitude"])+"&longitude=" + str(city["longitude"]);
            yield scrapy.Request(url=request_url, callback=self.parse_store)

    # calculate number of pages
    def parse_store(self, response):
        try:
            store_list = json.loads(response.body)
            for store in store_list:
                item = ChainItem()
                if store['stlocID'] in self.store_id:
                    continue
                self.store_id.append(store['stlocID'])
                item['store_number'] = store['stlocID']
                item['country'] = 'United States'
                item['latitude'] = store['latitude']
                item['longitude'] = store['longitude']
                item['store_name'] = store['locationName']
                item['address'] = store['address1']
                item['city'] = store['city']
                item['state'] = store['state']
                item['zip_code'] = store['zipCode']

                yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace('&#8217;', "'")
        else:
            return ""




        

