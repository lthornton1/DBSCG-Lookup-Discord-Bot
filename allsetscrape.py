# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~ DBSCG Lookup Discord Bot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~ Main card Scrapper, pulls all card info from the main website ~~~~~~~~~
# ~~~~~~~~~~~ Card types currently supported, Battle, Extra, Leader ~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

def cardDataScrape():
    urls = []
    leader = []
    battle = []
    extra = []

    url = 'http://www.dbs-cardgame.com/us-en/cardlist/?search=true&category=428006'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find(id='snaviList')

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
        # print("Scrapping", urls[y])
        response = requests.get(urls[y])
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('dl', attrs={'class':'cardListCol'})

        length = len(results)
        myiter = iter(range(0,length-1))
        for x in myiter:
            type = results[x].contents[7].find('dl', attrs={'class':'typeCol'})
            type2 = type.contents[3].text
            if type2 == 'LEADER':
                fname = results[x].find('dd', attrs={'class':'cardName'}).text
                bname = results[x+1].find('dd', attrs={'class':'cardName'}).text

                id = results[x].find('dt', attrs={'class':'cardNumber'}).text

                series = results[x].find('dl', attrs={'class':'seriesCol'})
                sname = series.contents[3].text

                color = results[x].find('dl', attrs={'class':'colorCol'})
                cname = color.contents[3].text

                rarity = results[x].find('dl', attrs={'class':'rarityCol'})
                rname = rarity.contents[3].text

                fpower = results[x].find('dl', attrs={'class':'powerCol'})
                fplv = fpower.contents[3].text
                bpower = results[x+1].find('dl', attrs={'class':'powerCol'})
                bplv = bpower.contents[3].text

                fchar = results[x].find('dl', attrs={'class':'characterCol'})
                fcname = fchar.contents[3].text
                bchar = results[x+1].find('dl', attrs={'class':'characterCol'})
                bcname = bchar.contents[3].text

                ftrait = results[x].find('dl', attrs={'class':'specialTraitCol'})
                fspt = ftrait.contents[3].text
                btrait = results[x+1].find('dl', attrs={'class':'specialTraitCol'})
                bspt = btrait.contents[3].text

                fera = results[x].find('dl', attrs={'class':'eraCol'})
                fename = fera.contents[3].text
                bera = results[x+1].find('dl', attrs={'class':'eraCol'})
                bename = bera.contents[3].text

                date = results[x].find('dl', attrs={'class':'availableDateCol'})
                rdate = date.contents[3].text

                fskill = results[x].find('dl', attrs={'class':'skillCol'})
                fskl = fskill.contents[3]

                final = re.sub('<br/>','\n',str(fskl))
                final = re.sub('<[/]?dd>','',final)
                final = re.sub('</img>','',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/red_ball.png"/>','(R)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/blue_ball.png"/>','(U)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/black_ball.png"/>','(B)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/yellow_ball.png"/>','(Y)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/green_ball.png"/>','(G)',final)
                final = re.sub('<[^>]*alt=\"','**[',final)
                final = re.sub('\" class[^>]*>',']** ',final)
                final = re.sub(r'[^\x00-\x7F]+','', final)
                final = re.sub('<dd class="centerText">','',final)

                bskill = results[x+1].find('dl', attrs={'class':'skillCol'})
                bskl = bskill.contents[3]

                final2 = re.sub('<br/>','\n',str(bskl))
                final2 = re.sub('<[/]?dd>','',final2)
                final2 = re.sub('</img>','',final2)
                final2 = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/red_ball.png"/>','(R)',final2)
                final2 = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/blue_ball.png"/>','(U)',final2)
                final2 = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/black_ball.png"/>','(B)',final2)
                final2 = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/yellow_ball.png"/>','(Y)',final2)
                final2 = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/green_ball.png"/>','(G)',final2)
                final2 = re.sub('<[^>]*alt=\"','**[',final2)
                final2 = re.sub('\" class[^>]*>',']** ',final2)
                final2 = re.sub(r'[^\x00-\x7F]+','', final2)
                final2 = re.sub('<dd class="centerText">','',final2)

                leader.append((id, type2, fname, bname, cname, sname, rname, fplv, bplv, fcname,bcname,fspt,bspt,fename,bename,rdate,final,final2))
                next(myiter, None)
            elif type.contents[3].text == 'BATTLE':
                fname = results[x].find('dd', attrs={'class':'cardName'}).text

                id = results[x].find('dt', attrs={'class':'cardNumber'}).text

                series = results[x].find('dl', attrs={'class':'seriesCol'})
                sname = series.contents[3].text

                color = results[x].find('dl', attrs={'class':'colorCol'})
                cname = color.contents[3].text

                rarity = results[x].find('dl', attrs={'class':'rarityCol'})
                rname = rarity.contents[3].text

                fpower = results[x].find('dl', attrs={'class':'powerCol'})
                fplv = fpower.contents[3].text

                fchar = results[x].find('dl', attrs={'class':'characterCol'})
                fcname = fchar.contents[3].text

                ftrait = results[x].find('dl', attrs={'class':'specialTraitCol'})
                fspt = ftrait.contents[3].text

                fera = results[x].find('dl', attrs={'class':'eraCol'})
                fename = fera.contents[3].text

                date = results[x].find('dl', attrs={'class':'availableDateCol'})
                rdate = date.contents[3].text

                fskill = results[x].find('dl', attrs={'class':'skillCol'})
                fskl = fskill.contents[3]

                final = re.sub('<br/>','\n',str(fskl))
                final = re.sub('<[/]?dd>','',final)
                final = re.sub('</img>','',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/red_ball.png"/>','(R)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/blue_ball.png"/>','(U)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/black_ball.png"/>','(B)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/yellow_ball.png"/>','(Y)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/green_ball.png"/>','(G)',final)
                final = re.sub('<[^>]*alt=\"','**[',final)
                final = re.sub('\" class[^>]*>',']** ',final)
                final = re.sub(r'[^\x00-\x7F]+','', final)
                final = re.sub('<dd class="centerText">','',final)

                en = results[x].find('dl', attrs={'class':'energyCol'})
                energy = en.contents[3]
                energy = re.sub('<br/>','\n',str(energy))
                energy = re.sub('<[/]?dd>','',energy)
                energy = re.sub('</img>','',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/red_ball.png"/>','(R)',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/blue_ball.png"/>','(U)',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/black_ball.png"/>','(B)',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/yellow_ball.png"/>','(Y)',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/green_ball.png"/>','(G)',energy)
                energy = re.sub('<[^>]*alt=\"','**',energy)
                energy = re.sub('\" class[^>]*>','**',energy)
                energy = re.sub(r'[^\x00-\x7F]+','**',energy)
                energy = re.sub('<dd class="centerText">','',energy)

                cen = results[x].find('dl', attrs={'class':'comboEnergyCol'})
                cenergy = cen.contents[3].text

                cpow = results[x].find('dl', attrs={'class':'comboPowerCol'})
                cpower = cpow.contents[3].text

                battle.append((id, type2, fname, cname, sname, rname, fplv, fcname,fspt,fename,rdate,final,energy,cenergy,cpower))

            elif type.contents[3].text == 'EXTRA':
                fname = results[x].find('dd', attrs={'class':'cardName'}).text

                id = results[x].find('dt', attrs={'class':'cardNumber'}).text

                series = results[x].find('dl', attrs={'class':'seriesCol'})
                sname = series.contents[3].text

                color = results[x].find('dl', attrs={'class':'colorCol'})
                cname = color.contents[3].text

                rarity = results[x].find('dl', attrs={'class':'rarityCol'})
                rname = rarity.contents[3].text

                date = results[x].find('dl', attrs={'class':'availableDateCol'})
                rdate = date.contents[3].text

                fskill = results[x].find('dl', attrs={'class':'skillCol'})
                fskl = fskill.contents[3]

                final = re.sub('<br/>','\n',str(fskl))
                final = re.sub('<[/]?dd>','',final)
                final = re.sub('</img>','',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/red_ball.png"/>','(R)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/blue_ball.png"/>','(U)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/black_ball.png"/>','(B)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/yellow_ball.png"/>','(Y)',final)
                final = re.sub('<img alt="" class="skillTextBall" src="../../images/cardlist/common/green_ball.png"/>','(G)',final)
                final = re.sub('<[^>]*alt=\"','**[',final)
                final = re.sub('\" class[^>]*>',']** ',final)
                final = re.sub(r'[^\x00-\x7F]+','', final)
                final = re.sub('<dd class="centerText">','',final)

                en = results[x].find('dl', attrs={'class':'energyCol'})
                energy = en.contents[3]
                energy = re.sub('<br/>','\n',str(energy))
                energy = re.sub('<[/]?dd>','',energy)
                energy = re.sub('</img>','',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/red_ball.png"/>','(R)',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/blue_ball.png"/>','(U)',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/black_ball.png"/>','(B)',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/yellow_ball.png"/>','(Y)',energy)
                energy = re.sub('<img alt="" class="colorCostBall" src="../../images/cardlist/common/green_ball.png"/>','(G)',energy)
                energy = re.sub('<[^>]*alt=\"','**',energy)
                energy = re.sub('\" class[^>]*>','**',energy)
                energy = re.sub(r'[^\x00-\x7F]+','**',energy)
                energy = re.sub('<dd class="centerText">','',energy)

                extra.append((id, type2, fname, cname, sname, rname, rdate,final,energy))

        df = pd.DataFrame(leader, columns=['id', 'type2', 'fname', 'bname', 'cname', 'sname', 'rname', 'fplv', 'bplv', 'fcname','bcname','fspt','bspt','fename','bename','rdate','fskl','bskl'])
        df.to_csv('csv/leader.csv', index=False, encoding='utf-8')

        df = pd.DataFrame(battle, columns=['id', 'type2', 'fname', 'cname', 'sname', 'rname', 'fplv', 'fcname','fspt','fename','rdate','fskl','energy','cenergy','cpower'])
        df.to_csv('csv/battle.csv', index=False, encoding='utf-8')

        df = pd.DataFrame(extra, columns=['id', 'type2', 'fname', 'cname', 'sname', 'rname', 'rdate','fskl','energy'])
        df.to_csv('csv/extra.csv', index=False, encoding='utf-8')
