from bs4 import BeautifulSoup
import requests, re


def getItems(query):
    url = 'https://www.walmart.com/search/?query='+query+'&grid=false&store=1780'
    cookie = {'t-loc-psid':'1572198768124|1780'}

    r = requests.get(url, cookies=cookie)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.findAll("div", {"data-tl-id" : re.compile('ProductTileListView-*')})
    for item in items:
        title = item.find("a", {'class':'product-title-link line-clamp line-clamp-2'})
        print(title.decode_contents())

getItems("milk")
