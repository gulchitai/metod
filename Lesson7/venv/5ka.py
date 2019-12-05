from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument('start-maximized')
chrome_options.add_argument('--headless')


driver = webdriver.Chrome(options=chrome_options)
driver.get('https://5ka.ru/special_offers/')
pages = 0
# import time

while True:
    # time.sleep(1)
    # button = driver.find_element_by_class_name('special-offers__more-btn')
    try:
        button = WebDriverWait(driver,60).until(
          EC.presence_of_element_located((By.CLASS_NAME, 'special-offers__more-btn'))
        )
        button.click()
        pages += 1
        print(f'Открыта {pages} страница')
    except:
        print(f'Всего {pages} страниц')
        break

goods = driver.find_elements_by_class_name('sale-card')

for good in goods:
    try:
        print(good.find_element_by_class_name('sale-card__title').text)
        print(float(good
                        .find_element_by_class_name('sale-card__price--new')
                        .find_element_by_xpath('span[1]')
                        .text)/100)
    except:
        print('Сбор данных окончен')
