#https://blockonomi.com/

# get col 8 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import pandas as pd
from tqdm import tqdm, trange
import pytz

tz = pytz.timezone('UTC')


def fetchLinks(x):
    return x['href']


def getLinks():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://blockonomi.com/")
    #driver.get("https://cointelegraph.com/tags/altcoin")
    cancel = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID,"onesignal-slidedown-cancel-button")))
    cancel.click()
    errors =0
    data = []
    for x in tqdm(range(0,500)):
        try:
            time.sleep(2)
            el = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//span[@class='page-numbers label-next']")))
            driver.execute_script("arguments[0].scrollIntoView();", el)
            el.click()
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            soup = soup.find('div',{'class':'posts-dynamic posts-container ts-row grid count-0 grid-cols-2'})
            soup = soup.findAll('a',{'class':'image-link'})
            add = [fetchLinks(x) for x in soup]
            data = data +add
        except:
            print('error experienced at loop: '+str(x))
    driver.close()
    return data

    
    # rerun coindesk 


    #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT,"Load More Articles")))
    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.visibility_of_element_located((By.XPATH, '//a[text()="Load More Articles"]'))
    #     )

    #     element.click()
    # except:
    #     errors= errors+1
    #     break


def generateData(x):
    try:
        req = requests.get(x)
        soup = BeautifulSoup(req.content, 'html.parser')
        author = soup.find('a',{'rel':'author'}).getText()
        title= soup.find('h1',{'class':'post-title'}).getText()
        t = soup.find('time',{'class':'post-date'})['datetime']
        article = soup.find('div',{'class':'post-content description cf entry-content has-share-float content-spacious'}).getText()
        t = str(t)[:-6]
        naive_time = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
        tz_time = tz.localize(naive_time)
        london_tz = pytz.timezone('Europe/London')
        london_time = tz_time.astimezone(london_tz)
        t = str(london_time)[:-6]
        timestamp = time.mktime(datetime.strptime(t, '%Y-%m-%d %H:%M:%S').timetuple())
        return ['Blockonomi',title,author,timestamp,article]
    except:
        print('fail in fetching info')
        return ['','','','','']
    
data = getLinks()
output = [generateData(x) for x in tqdm(data)]
df = pd.DataFrame(output,columns = ['Source','Title','Author','TimeStamp','Text'])
df.to_csv('/home/block/Documents/AppliedProject/Scrape/Assets/Blockonomi.csv')
print(df)