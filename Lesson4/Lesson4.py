from lxml import html
import requests
from pprint import pprint
import pandas as pd

def parse_mail_ru():
    main_link = 'https://m.mail.ru'
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    response = requests.get(main_link, headers=headers).text
    root = html.fromstring(response)

    links = root.xpath('//div[contains (@id,"news-")]/a[@class="list__item"]/@href')
    names = root.xpath('//div[contains (@id,"news-")]/a[@class="list__item"]/div/span[@class="list__item__title"]/text()')

    df = pd.DataFrame()
    df['links'] = links
    df['names'] = names
    df['source'] = main_link

    dates = []
    for link in links:
        response = requests.get(link, headers=headers).text
        root = html.fromstring(response)
        public_date = root.xpath('//*[@class="note__text breadcrumbs__text js-ago"]/@datetime')
        dates.append(public_date)

    df['public_date'] = dates
    return df

def parse_lenta_ru():
    main_link = 'https://lenta.ru/'
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    response = requests.get(main_link, headers=headers).text
    root = html.fromstring(response)

    links =[]
    names = []
    dates = root.xpath('//section[@class="row b-top7-for-main js-top-seven"]/div/div/a/time')
    for d in dates:
        links.append(d.xpath('../@href'))
        names.append(d.xpath('../text()'))
    dates = root.xpath('//section[@class="row b-top7-for-main js-top-seven"]/div/div/a/time/@datetime')
    df = pd.DataFrame()
    df['links'] = links
    df['names'] = names
    df['source'] = main_link
    df['public_date'] = dates
    return df

df = parse_lenta_ru()
df2 = parse_mail_ru()
pass