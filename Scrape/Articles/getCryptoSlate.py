from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import pandas as pd
from tqdm import tqdm, trange
import pytz

months = [{'January':'01','February':'02','Marcj':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}]

tz = pytz.timezone('UTC')


def getData(x):
    try:
        req = requests.get(x)
        soup = BeautifulSoup(req.content,'html.parser')
        name = soup.find('span',{'class':'name'}).getText()
        title = soup.find('h1',{'class':'post-title'}).getText()
        initial_time = soup.find('span',{'class':'post-date'}).getText()
        initial_time = initial_time.split(' ')
        t= months[0][initial_time[0]]
        md = str(initial_time[2]+'-'+t+'-'+initial_time[1].replace(',','')+' '+initial_time[4]+' '+initial_time[5])
        native_time = datetime.strptime(md,'%Y-%m-%d %H:%M %p')
        tz_time = tz.localize(native_time)
        london_tz = pytz.timezone('Europe/London')
        london_time = tz_time.astimezone(london_tz)
        t = str(london_time)[:-6]
        timestamp = time.mktime(datetime.strptime(t, '%Y-%m-%d %H:%M:%S').timetuple())
        article = soup.find('div',{'class':'container single-post-box-container clearfix'})
        article = article.find('article')

        if article.find('div',{'class':'cs-edge-splash clearfix'}) is None:
            try:
                article.find('div', {'class':"post-cta"}).decompose()
            except:
                print('NOCTA')
            
            try:
                article.find('div', {'class':"cpa-signup cryptocom placement clearfix"}).decompose()
            except:
                print('NO SIGNUP')
            
            try:
                article.find('div', {'class':"top footer-disclaimer"}).decompose()
            except:
                print('NO TRANSPARANCY')

            try:
                article.find('div', {'class':"footer-disclaimer"}).decompose()
            except:
                print('NO DISCLAIMER')
            return ['CryptoSlate',title,name,timestamp,article.getText()]
        else:
            return ['','','','','']
        
    except:
        print('failed')
        return ['','','','','']
    

    # try:

    #     ref = x.find('a',href=True)
    #     req = requests.get(ref['href'])
    #     subsoup = BeautifulSoup(req.content, 'html.parser')
    #     meta = subsoup.find("div", {"class": "meta"})
    #     meta = meta.find('p').getText()
    #     meta = meta.split('|')
    #     dt = meta[1].replace(',' ,'').strip().split(' ')
    #     now = str(dt[2])+'-'+str(months[0][dt[0]])+'-'+dt[1]+str(meta[2])+':00'
    #     author = meta[0]
    #     timestamp = time.mktime(datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S").timetuple())
    #     textData = subsoup.find("div", {"class": "article-content"}).getText()
    #     title = subsoup.find("h1", {"class": "title"}).getText()
    #     return ['Bitcoinist',title,author,timestamp,textData]
    # except:
    #     print('error')
    #     return ['','','','','']


def getLinks():
    data = [getPages(item) for item in range(1,35)]
    fin = []
    for x in data:
        req = requests.get(x)
        soup = BeautifulSoup(req.content, 'html.parser')
        soup = soup.find('section',{'class':'list-feed'})
        soup = soup.findAll('article')
        for t in soup:
            fin.append(t.find('a')['href'])
    info = [getData(x) for x in tqdm(fin)]
    df = pd.DataFrame(info,columns = ['Source','Title','Author','TimeStamp','Text'])
    df.to_csv('/home/block/Documents/AppliedProject/Scrape/Assets/CryptoSlate.csv')
    print(df)

 

    


def getPages(x):
    if x==1:
        return 'https://cryptoslate.com/altcoins'
    else:
        return 'https://cryptoslate.com/altcoins/page'+str(x)

print(getLinks())