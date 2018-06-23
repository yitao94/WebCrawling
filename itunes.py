import re
import os
import requests
import time
from lxml import html
from pprint import pprint

global number
number = 0

class AppCrawler:
    
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.current_depth = 0
        self.depth_links = []
        self.apps = []

    def crawl(self):
        app = self.get_app_from_link(self.starting_url)
        self.apps.append(app)
        self.depth_links.append(app.links)

        while self.current_depth < self.depth:
            current_links = []
            for link in self.depth_links[self.current_depth]:
                global number
                number += 1
                print(number)
                # print('url: '+ str(link) + '\n\r')
                current_app = self.get_app_from_link(link)
                current_links.extend(current_app.links)
                self.apps.append(current_app)
            self.current_depth += 1
            self.depth_links.append(current_links)

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        # print start_page.text
        tree = html.fromstring(start_page.text)
        # pprint(tree)
        name = tree.xpath('//h1[@class="product-header__title product-header__title--app-header"]/text()')[0]
        # print name
        # for a in name:
        #     print(ord(a))
        reg = r'([^\n ].+[^\n ])'
        name = re.search(reg, name).group()
        # print ('name: ' + str(name))
        
        developer = tree.xpath('//a[@class="link"]/text()')[0]
        # print('developer: ' + str(developer))

        price = tree.xpath('//li[@class="inline-list__item inline-list__item--bulleted"]/text()')[0]
        # print('price: ' + str(price))
        
        links = tree.xpath('//a[@data-test-we-lockup-kind="iosSoftware"]/@href')
        # for link in links:
            # print('link: ' + str(link))
        
        app = App(name, developer, price, links, link)
        
        return app

class App:

    def __init__(self, name, developer, price, links, url):
        self.name = name
        self.developer = developer
        self.price = price
        self.links = links
        self.url = url

    def __str__(self):
        return('Name: ' + self.name.encode('UTF-8') +
                '\n\rDeveloper: '+ self.developer.encode('UTF-8') +
                '\n\rPrice: '+ self.price.encode('UTF-8') +
                '\n\rUrl: '+ self.url.encode('UTF-8') +
                '\n\r')

def main():
    crawler = AppCrawler('https://itunes.apple.com/us/app/super-mario-run/id1145275343', 1)
    crawler.crawl()

    for app in crawler.apps:
        print app

if __name__ == '__main__':
    """
    name='happy tree friends'
    developer='yitao'
    price=str(1)
    links='www.baidu.com'
    app=App(name, developer, price, links)
    print(app)
    """
    main()
