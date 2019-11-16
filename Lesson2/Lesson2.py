from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import time
import random
import json
import pandas as pd

def getSalary(salaryStr):
    if salaryStr[:2] == 'от':
        salary_min = salaryStr
        salary_max = 'не указана'
    elif salaryStr[:2] == 'до':
        salary_min = 'не указана'
        salary_max = vacancy_salary
    elif salaryStr.find('-') == -1:
        salary_min = 'не указана'
        salary_max = 'не указана'
    else:
        salary_min = salaryStr[:salaryStr.find('-')]
        salary_max = salaryStr[salaryStr.find('-') + 1:]
    return salary_min, salary_max

print('Input position:')
position = input()
print('Input number page:')
num_page = input()

if num_page.isdigit()==False:
    exit(-1)

#with open('hh.html', 'r', encoding='utf-8') as file:
#    html = file.read()

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
main_link = 'https://www.superjob.ru'

vacancies=[]

for page in range(int(num_page)):
    reg = requests.get(main_link+f'/vacancy/search/?keywords={position}&page={page+1}&geo%5Bc%5D%5B0%5D=1',headers=headers)
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


#  --------------------------------------------------------
main_link = 'https://hh.ru'


for page in range(int(num_page)):
    reg = requests.get(main_link+f'/search/vacancy?text={position}&page={page}',headers=headers)
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

df=pd.DataFrame(vacancies)
pass