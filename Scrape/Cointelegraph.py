from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time





driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://cointelegraph.com/tags/altcoin")


#
accept = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//button[contains(@class, "btn privacy-policy__accept-btn")]'))
)
accept.click()



no = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//button[contains(@class, "sendpulse-prompt-btn sendpulse-accept-btn sp_notify_prompt")]'))
)
no.click()


errors =0
for x in tqdm(range(0,1000)):
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    wait = WebDriverWait(driver, 10)
    time.sleep(1)

    #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT,"Load More Articles")))
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//button[contains(@class, "btn posts-listing__more-btn")]'))
        )
        element.click()
    except:
        break
        errors= errors+1
        

print(errors)    
with open("/home/block/Documents/AppliedProject/Scrape/Assets/CoinTelegraph.html", "w") as f:
    f.write(driver.page_source)



