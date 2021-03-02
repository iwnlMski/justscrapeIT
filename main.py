import requests
from bs4 import BeautifulSoup
from database import add_to_database, offer_not_exists, fill_table_with_skills
from selenium import webdriver
from time import time


class Offer:
    def __init__(self, offer_address, offer_name, location, company, salary):
        self.offer_address = offer_address
        self.offer_name = offer_name
        self.location = location
        self.company = company
        self.salary = salary


def initialize_chrome_driver():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    return webdriver.Chrome(options=op)


def get_response_from_url(url):
    return requests.get(url)


def generate_offer_response(response):
    for offer in response.text.split('</entry>')[0:-1]:
        yield offer + '</entry>'


def get_skillset_from_url(url, driver):
    driver.get(url)
    skill_set_soup = BeautifulSoup(driver.page_source, 'html.parser')
    return [x['title'] for x in skill_set_soup.find_all(attrs={'class': 'css-1xm32e0'})]


def limit_update_check():
    for limit in range(101):
        yield limit


def update_database_with_offers(splitted_response):
    limit = limit_update_check()
    driver = initialize_chrome_driver()
    for offer in splitted_response:
        soup = BeautifulSoup(offer, 'html.parser')
        if offer_not_exists(soup.entry.id.text.strip()):
            summary_soup = BeautifulSoup(soup.summary.text, 'html.parser')
            skills = get_skillset_from_url(soup.entry.id.text.strip(), driver)
            skills = ', '.join(skills)
            data = {
                'link': soup.entry.id.text.strip(),
                'title': soup.entry.title.text.strip(),
                'company': soup.entry.author.text.strip(),
                'salary': summary_soup.p.text.strip().splitlines()[0],
                'location': summary_soup.p.text.strip().splitlines()[1],
                'skills': skills,
            }
            add_to_database(data)
        else:
            try:
                next(limit)
            except StopIteration:
                break
    return print('Done updating')


def get_tech_by_language(lang):
    pass


URL = 'https://justjoin.it/feed.atom'
response = get_response_from_url(URL)
splitted_response = generate_offer_response(response)

# t1 = time()
# update_database_with_offers(splitted_response)
# t2 = time()
# print(f"It took {t2 - t1} s")
temp = fill_table_with_skills('python')

# for skill_set in temp:
#     for skill in skill_set:
#         print(type(skill.split(', ')))
#         print(skill.split(', '))
