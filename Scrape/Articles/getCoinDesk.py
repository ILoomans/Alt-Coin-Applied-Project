from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import pandas as pd
from tqdm import tqdm, trange
import pytz

tz = pytz.timezone('UTC')



def getData(x):
        #use findall and then get the second
    try:
        ref = x.findAll('a')
        req = requests.get('https://www.coindesk.com'+ref[1]['href'])
        subsoup = BeautifulSoup(req.content, 'html.parser')
        t = subsoup.find('time')['datetime']
        naive_time = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
        tz_time = tz.localize(naive_time)
        london_tz = pytz.timezone('Europe/London')
        london_time = tz_time.astimezone(london_tz)

        t = str(london_time)[:-6]
        timestamp = time.mktime(datetime.strptime(t, '%Y-%m-%d %H:%M:%S').timetuple())
        author = subsoup.find('section',{'class':'sidebar-profile dark author'})
        author = author.find('h5',{'class':'heading'}).getText()

        title = subsoup.find('h1',{'class':'heading'}).getText()
        textData = subsoup.find('section',{'class':'has-media news article-body'})
        # remove the disclosure
        try:
            textData.find('div', {'class':"article-disclosure"}).decompose()
        except:
            print('nodisclosure')
        return ['CoinDesk',title,author,timestamp,textData.getText()]

    except:
        print('error')
        return ['','','','','']
   


        # meta = subsoup.find("div", {"class": "meta"})
        # meta = meta.find('p').getText()
        # meta = meta.split('|')
        # dt = meta[1].replace(',','').strip().split(' ')
        # now = str(dt[2])+'-'+str(months[0][dt[0]])+'-'+dt[1]+str(meta[2])+':00'
        # author = meta[0]
        # timestamp = time.mktime(datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S").timetuple())
        # textData = subsoup.find("div", {"class": "article-content"}).getText()
        # title = subsoup.find("h1", {"class": "title"}).getText()
        # return ['Bitcoinist',title,author,timestamp,textData]


with open("/home/block/Documents/AppliedProject/Scrape/Assets/CoinDesk.html", "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents)
    els = soup.findAll("div", {"class": "list-item-wrapper"})  
    data = [getData(item) for item in tqdm(els)]
    df = pd.DataFrame(data,columns = ['Source','Title','Author','TimeStamp','Text'])
    df.to_csv('/home/block/Documents/AppliedProject/Scrape/Assets/CoinDesk.csv')
    print(df)
