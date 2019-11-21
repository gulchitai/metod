from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import time
import random
import json
import pandas as pd
from pymongo import MongoClient

def getSalary(salaryStr):
    salaryStr = salaryStr.replace(' ', '')
    salary_min = 0
    salary_max = 0
    array = [int(n) for n in ''.join(c if c.isdigit() else ' ' for c in salaryStr).split()]
    if salaryStr[:2] == 'до' and len(array)==1:
        salary_max = array[0]
    elif salaryStr[:2] == 'от' and len(array)==1:
        salary_min = array[0]
    elif len(array)==2:
        salary_min = array[0]
        salary_max = array[1]
    return salary_min, salary_max


#with open('hh.html', 'r', encoding='utf-8') as file:
#    html = file.read()

def parseSuperJob(headers, position, num_page):
    vacancies = []
    main_link = 'https://www.superjob.ru'
    for page in range(int(num_page)):
        reg = requests.get(main_link+f'/vacancy/search/?keywords={position}&page={str(int(num_page)+1)}&geo%5Bc%5D%5B0%5D=1',headers=headers)
        if reg.status_code!=200:
            return vacancies
        html = reg.text
        parsed_html = bs(html, 'lxml')
        vacancies_block = parsed_html.find('script', {'type': 'application/ld+json'})
        data = json.loads(vacancies_block.text)
        for item in data['itemListElement']:
            reg = requests.get(item['url'],headers=headers)
            html = reg.text
            nonBreakSpace = u'\xa0'
            html = html.replace(nonBreakSpace,' ')
            parsed_html = bs(html, 'lxml')
            h1 = parsed_html.find('h1')
            vacancy_salary = h1.nextSibling.nextSibling.nextSibling.getText()
            vacancy_data = {}
            salary_min, salary_max = getSalary(vacancy_salary)
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['name'] = h1.getText()
            vacancy_data['link'] = item['url']
            vacancy_data['site'] = main_link
            vacancies.append(vacancy_data)
        pass
    return vacancies


#  --------------------------------------------------------

def parseHH(headers, position, num_page):
    vacancies = []
    main_link = 'https://hh.ru'
    for page in range(int(num_page)):
        reg = requests.get(main_link+f'/search/vacancy?text={position}&page={num_page}',headers=headers)
        if reg.status_code!=200:
            return vacancies
        #with open('hh.html','wb') as file:
        #    file.write(reg.content)
        html = reg.text
        nonBreakSpace = u'\xa0'
        html = html.replace(nonBreakSpace,' ')

        parsed_html = bs(html,'lxml')

        vacancies_block = parsed_html.find('div',{'class':'vacancy-serp'})
        vacancies_list = vacancies_block.findChildren(recursive=False)

        for vacancy in vacancies_list:
            vacancy_data={}
            main_info = vacancy.find('a',{'class':'bloko-link HH-LinkModifier'})
            if main_info is None:
                continue
            vacancy_name = main_info.getText()
            vacancy_link = main_info['href']
            l = main_info.findParent().findParent().findParent().next_sibling()
            if len(l)>0:
                vacancy_salary = l[0].getText().replace('&nbsp;','')
            else:
                vacancy_salary = ""

            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['site'] = main_link
            salary_min, salary_max = getSalary(vacancy_salary)
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max

            vacancies.append(vacancy_data)
        time.sleep(random.randint(1,5))
    return vacancies


def main():
    print('Input position:')
    position = input()
    print('Input number page:')
    num_page = input()

    if num_page.isdigit() == False:
        exit(-1)

    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

    client = MongoClient('localhost', 27017)
    db = client['test']

    for collection_name in db.list_collection_names():
        if collection_name == 'vacancies':
            collection = db['vacancies']
            collection.drop()

    result = db.vacancies.insert_many(parseSuperJob(headers, position, num_page))
    pprint(result.inserted_ids)
    result = db.vacancies.insert_many(parseHH(headers, position, num_page))
    pprint(result.inserted_ids)

    print('Input salary for search:')
    salary = input()
    if salary.isdigit() == False:
        exit(-1)

    objects = db.vacancies.find({'salary_min': {'$gte': int(salary)}})
    for obj in objects:
        pprint(obj)

if __name__=='__main__':
    main()