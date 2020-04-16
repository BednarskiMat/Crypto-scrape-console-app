import logging

import scrapy

from scrapy.crawler import CrawlerProcess
import os, json



class CryptoSpider(scrapy.Spider):
    name = "crypto_spider"
    start_urls = ['https://coinmarketcap.com/', 'https://coinmarketcap.com/2','https://coinmarketcap.com/3']
    logging.getLogger('scrapy').propagate = False

    def parse(self, response):
        row_select = '//tbody/tr'
        for coin in response.xpath(row_select):
            name = 'td/div[@class="cmc-table__column-name sc-1kxikfi-0 eTVhdN"]/a/text()'
            price = 'td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price"]/a/text()'
            yield {
                'name': coin.xpath(name).get(),
                'price': coin.xpath(price).get()
            }
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'cryptos.json'
})

def searchForCoin(name):
    searchFor = name
    for i in range(len(coins)):
        coin_name = coins[i].get("name")
        coin_price = coins[i].get("price")
        if searchFor.lower() == coin_name.lower():
             print(f"{coin_name}: {coin_price}")
        elif i == len(coins)-1 and searchFor.lower() != coin_name.lower() :
            print("Does not exist")


def top_three():
    for i in range(3):
        coin_name = coins[i].get("name")
        coin_price = coins[i].get("price")
        print(f"{i+1}: {coin_name}: {coin_price}")



if os.path.exists('cryptos.json'):
    os.remove('cryptos.json')
process.crawl(CryptoSpider)
process.start()
with open('./cryptos.json') as f:
  coins = json.load(f)

print('Welcome to Crypto Price Check')
print('Press 1 to search for a coin, Press 2 to list top 3 coins, or type "quit" to exit')
runner = True
while runner:
    task = input('>')
    if task == '1':
        coin = input("Enter coin name: ")
        searchForCoin(coin)
    elif task == '2':
        top_three()
    elif task.lower() == 'quit':
        print("Goodbye!")
        runner = False
    else:
        print("Unexpected value Entered.. quitting script")
        runner = False









