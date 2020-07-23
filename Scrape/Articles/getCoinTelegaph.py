from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import pandas as pd
from tqdm import tqdm, trange
import pytz

#tz = pytz.timezone('UTC')



def getData(x):
        #use findall and then get the second
    try:
        ref = x.findAll('a')
        print(ref[0]['href'])
        
        # req = requests.get('https://www.coindesk.com'+ref[1]['href'])
        # subsoup = BeautifulSoup(req.content, 'html.parser')
        # t = subsoup.find('time')['datetime']
        # naive_time = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
        # tz_time = tz.localize(naive_time)
        # london_tz = pytz.timezone('Europe/London')
        # london_time = tz_time.astimezone(london_tz)

        # t = str(london_time)[:-6]
        # timestamp = time.mktime(datetime.strptime(t, '%Y-%m-%d %H:%M:%S').timetuple())
        # author = subsoup.find('section',{'class':'sidebar-profile dark author'})
        # author = author.find('h5',{'class':'heading'}).getText()

        # title = subsoup.find('h1',{'class':'heading'}).getText()
        # textData = subsoup.find('section',{'class':'has-media news article-body'})
        # # remove the disclosure
        # try:
        #     textData.find('div', {'class':"article-disclosure"}).decompose()
        # except:
        #     print('nodisclosure')
        # return ['CoinDesk',title,author,timestamp,textData.getText()]

    except:
        print('error')
        return ['','','','','']
   




with open("/home/block/Documents/AppliedProject/Scrape/Assets/CoinTelegraph.html", "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents)
    els = soup.find("div", {"class": "posts-listing posts-listing_inline"})
    els = els.findAll('li',{'class':'posts-listing__item'})
    print(len(els))
    data = [getData(item) for item in tqdm(els[:10])]
    # df = pd.DataFrame(data,columns = ['Source','Title','Author','TimeStamp','Text'])
    # df.to_csv('/home/block/Documents/AppliedProject/Scrape/Assets/CoinTelegraph.csv')
    # print(df)
