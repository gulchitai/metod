from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pymongo import MongoClient
import json

login = 'gulchitai@bk.ru'
password = ''


driver = webdriver.Chrome()
driver.get('https://m.mail.ru/login')
assert "Вход — Почта Mail.Ru" in driver.title

elem = driver.find_element_by_name('Login')
elem.send_keys(login)

elem = driver.find_element_by_name('Password')
elem.send_keys(password)

elem.send_keys(Keys.RETURN)
assert login in driver.title

letters = driver.find_elements_by_class_name('messageline__from')
subjects = driver.find_elements_by_class_name('messageline__subject')
dates = driver.find_elements_by_class_name('messageline__date')
links = driver.find_elements_by_class_name('messageline__link')

df = pd.DataFrame()
li = []
for l in letters:
    li.append(l.text)
    print(f'От кого: {l.text}')

df['from'] = li

li = []
for s in subjects:
    li.append(s.text)
    print(f'Тема: {s.text}')

df['subject'] = li

li = []
for d in dates:
    li.append(d.text)
    print(f'Дата получения: {d.text}')
df['date'] = li

li = []
for l in links:
    url = l.get_attribute("href")
    li.append(url)
    print(f'Ссылка: {url}')
df['link'] = li

i = 0
li2 = []
for l in li:
    driver.get(l)
    assert df.iloc[i,1] in driver.title

    body = driver.find_element_by_xpath('//div[@id="readmsg__body"]')
    li2.append(body.text)
    i += 1

df['body'] = li2
driver.quit()

client = MongoClient('localhost', 27017)
db = client.lesson7

records = json.loads(df.T.to_json()).values()
db.email.insert_many(records)
pass

