from bs4 import BeautifulSoup
import requests, re


def getItems(query):
    url = 'https://www.walmart.com/search/?query='+query+'&grid=false&store=1780'
    cookie = {'t-loc-psid':'1572198768124|1780'}

    r = requests.get(url, cookies=cookie)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.findAll("div", {"data-tl-id" : re.compile('ProductTileListView-*')})
    print(items)

getItems("milk")
