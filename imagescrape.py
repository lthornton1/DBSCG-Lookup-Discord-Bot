# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~ DBSCG Lookup Discord Bot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Generates all of the urls for images paried with each card id number ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd

def cardImgScrape():
    urls = []
    cards = []

    html = urlopen('http://www.dbs-cardgame.com/us-en/cardlist/?search=true&category=428006')
    bs = BeautifulSoup(html, 'html.parser')
    results = bs.find(id='snaviList')

    length = len(results)
    iter1 = iter(range(1,length-1))
    for x in iter1:
        link = results.contents[x].find('a')
        newlink = link.get('href').replace(".", "")
        newurl = "http://www.dbs-cardgame.com/us-en/cardlist" + newlink
        urls.append(newurl)
        next(iter1,None)

    length = len(urls)
    iter2 = iter(range(0,length-1))
    for y in iter2:
        response = requests.get(urls[y])
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img', {'class':'zoomcard'})
        for image in images:
            cur = image['src']
            cur2 = cur.replace("../../images/cardlist/cardimg/","")
            cur3 = cur2.replace(".png","")
            fixed = cur.replace("../../","http://www.dbs-cardgame.com/")
            cards.append((cur3,fixed))

    df = pd.DataFrame(cards, columns=['id', 'img'])
    df.to_csv('csv/cardimg.csv', index=False, encoding='utf-8')
