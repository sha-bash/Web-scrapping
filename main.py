import json
import requests
from bs4 import BeautifulSoup

HOST = 'https://spb.hh.ru/search/vacancy'
KEYWORDS = ['Django', 'Flask']
PARAMS = {
    'text': 'Python',
    'area': ['1', '2'],  # Москва и Санкт-Петербург
    'order_by': 'publication_time',
    'search_period': '0',
    'items_on_page': '20'
}

headers = {'User-Agent': 'Mozilla/5.0'}

with requests.Session() as session:
    session.headers.update(headers)
    response = session.get(HOST, params=PARAMS)
    soup = BeautifulSoup(response.text, 'html.parser')

vacancies = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})

vacancy_list = []
for vacancy in vacancies:
    title = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
    if any(keyword in title for keyword in KEYWORDS):
        link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        salary = salary.text if salary else 'Не указано'
        company = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
        city = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text

        vacancy_list.append({
            'title': title,
            'link': link,
            'company': company.strip(),
            'city': city.strip(),
            'salary': salary.strip() if salary else salary
        })

print(json.dumps(vacancy_list, ensure_ascii=False, indent=4))
