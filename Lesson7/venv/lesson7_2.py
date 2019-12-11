from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
from pymongo import MongoClient
import json

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')
assert "М.Видео - интернет-магазин" in driver.title

html = driver.find_element_by_tag_name('html')
html.send_keys(Keys.PAGE_DOWN)

buttons = driver.find_elements_by_class_name('sel-hits-button-next')

list_price = []
list_name = []
list_link = []
for i in range(0,5):
    buttons[1].send_keys(Keys.ENTER)
    time.sleep(1)
    elems = driver.find_elements_by_class_name('accessories-product-list')
    elems_n = elems[1].find_elements_by_class_name('sel-product-tile-title')
    for e in elems_n:
        if e.text:
            list_link.append(e.get_attribute('href'))
            list_name.append(e.text)
    elems_p = elems[1].find_elements_by_class_name('c-pdp-price__current')
    for e in elems_p:
        if e.text:
            list_price.append(e.text)

driver.quit()
df = pd.DataFrame()
df['price'] = list_price
df['name'] = list_name
df['link'] = list_link

client = MongoClient('localhost', 27017)
db = client.lesson7

records = json.loads(df.T.to_json()).values()
db.mvideo.insert_many(records)
pass



