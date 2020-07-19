from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm





driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://bitcoinist.com/category/altcoin-news/")
#driver.get("https://cointelegraph.com/tags/altcoin")




errors =0
for x in tqdm(range(0,250)):
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    wait = WebDriverWait(driver, 10)

    #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT,"Load More Articles")))
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//a[text()="Load More Articles"]'))
        )

        element.click()
    except:
        errors= errors+1
        break

print(errors)    
with open("/home/block/Documents/AppliedProject/Scrape/Assets/bitcoinist.html", "w") as f:
    f.write(driver.page_source)

    












driver.close()