from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['scraping']
collection = db['articles']

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=chrome_options)

site_url = "https://4pda.to"

try:
    driver.get(site_url)
    pause_time = 20
    WebDriverWait(driver, pause_time) 
    posts = driver.find_elements(By.XPATH, "//article[@itemtype = 'http://schema.org/Article']")
    hrefs = driver.find_elements(By.XPATH, "//article[@itemtype = 'http://schema.org/Article']/div[@class='more-box']/a")
    post_data = {}
    for i in range(min(len(posts)+2, len(hrefs))):
        post_text = posts[i+2].text.split("\n")
        href = hrefs[i].get_attribute('href')
        title = post_text[2]
        pub_date = post_text[1]
        description = post_text[3] 
        post_data[title] = {"description": description, "published": pub_date, "link": href}
    collection.insert_one(post_data)
    
except Exception as e:
    print("Произошла ошибка:", e)

finally:
    driver.quit()