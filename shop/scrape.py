from bs4 import BeautifulSoup
import requests, re


def getItems(query):
    url = 'https://www.walmart.com/search/?query='+query+'&grid=false&store=1780'
    cookie = {'t-loc-psid':'1572198768124|1780'}

    r = requests.get(url, cookies=cookie)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.findAll("div", {"data-tl-id" : re.compile('ProductTileListView-*')})
    parsed = []
    for item in items:
        title = item.find("a", {'class':'product-title-link line-clamp line-clamp-2'})
        id = title['href'].split("/")[-1]
        img = item.find("img", {'data-pnodetype':"item-pimg"})
        price = item.find('span', {'class':'price-group'})
        if title is None or img is None or price is None:
            continue
        #print(title.decode_contents(), img['src'], price.decode_contents())
        parsed.append({'title':title.get_text(), 'id':id, 'image':img['src'], 'price':price.get_text()})
    return parsed
