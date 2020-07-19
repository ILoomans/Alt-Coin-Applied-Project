from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from tqdm import tqdm
import time



driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.newsbtc.com/category/crypto/")
#driver.get("https://cointelegraph.com/tags/altcoin")

agree = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-cookie"]')))
agree.click()


errors =0
for x in tqdm(range(0,2000)):
    # driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="jeg_block_loadmore "]'))
        )    
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(1)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="jeg_block_loadmore "]'))
        )

        element.click()
    except:
        errors= errors+1
        break

print(errors)    
with open("/home/block/Documents/AppliedProject/Scrape/Assets/NewsBTC.html", "w") as f:
    f.write(driver.page_source)

    


