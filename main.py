import requests
from bs4 import BeautifulSoup
from database import add_to_database, offer_not_exists, create_table_with_tech_for_lang, delete_table_of_skills
from selenium import webdriver
from time import time
import threading


class Offer:
    def __init__(self, offer_address, offer_name, location, company, salary):
        self.offer_address = offer_address
        self.offer_name = offer_name
        self.location = location
        self.company = company
        self.salary = salary


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        pass


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


def update_database_with_offers(splitted_response, driver):
    limit = limit_update_check()
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


URL = 'https://justjoin.it/feed.atom'
response = get_response_from_url(URL)
splitted_response = generate_offer_response(response)

t1 = time()
driver = initialize_chrome_driver()
update_database_with_offers(splitted_response, driver)
t2 = time()
print(f"It took {t2 - t1} s")

# create_table_with_tech_for_lang('python')
# delete_table_of_skills('python')

