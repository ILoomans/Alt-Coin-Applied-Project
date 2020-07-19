from bs4 import BeautifulSoup
import requests
import datetime
import time
import pandas as pd
from tqdm import tqdm, trange

months = [{'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}]



def getData(x):
    try:
        #use findall and then get the second
        ref = x.find('a',href=True)

        req = requests.get(ref['href'])
        subsoup = BeautifulSoup(req.content, 'html.parser')
        meta = subsoup.find("div", {"class": "meta"})
        meta = meta.find('p').getText()
        meta = meta.split('|')
        dt = meta[1].replace(',','').strip().split(' ')
        now = str(dt[2])+'-'+str(months[0][dt[0]])+'-'+dt[1]+str(meta[2])+':00'
        author = meta[0]
        timestamp = time.mktime(datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S").timetuple())
        textData = subsoup.find("div", {"class": "article-content"}).getText()
        title = subsoup.find("h1", {"class": "title"}).getText()
        return ['Bitcoinist',title,author,timestamp,textData]
    except:
        print('error')


with open("/home/block/Documents/AppliedProject/Scrape/Assets/CoinDesk.html", "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents)
    sub = soup.find("div", {"class": "story-stack"})
    els = sub.findAll('div',{'class':'text-content'})
    data = [getData(item) for item in tqdm(els)]
    df = pd.DataFrame(data,columns = ['Source','Title','Author','TimeStamp','Text'])
    print(df.shape)
    df.to_csv('/home/block/Documents/AppliedProject/Scrape/Assets/CoinDesk.csv')
