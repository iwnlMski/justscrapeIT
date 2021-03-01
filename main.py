import requests
from bs4 import BeautifulSoup


class Offer:
    def __init__(self, offer_address, offer_name, location, company, salary):
        self.offer_address = offer_address
        self.offer_name = offer_name
        self.location = location
        self.company = company
        self.salary = salary


def get_response_from_url(url):
    return requests.get(url)


def split_response_into_list(response):
    return [ele+'</entry>' for ele in response.text.split('</entry>')]


def create_list_of_offers(splitted_response):
    for offer in splitted_response:
        soup = BeautifulSoup(offer, 'html.parser')
        offer_link = soup.entry.id.text.strip()
        offer_title = soup.entry.title.text.strip()
        company_name = soup.entry.author.text.strip()
        soup = BeautifulSoup(soup.summary.text, 'html.parser')
        offer_salary = soup.p.text.strip().splitlines()[0]
        offer_location = soup.p.text.strip().splitlines()[1]
        return Offer(offer_link, offer_title, offer_location, company_name, offer_salary)
        break


URL = 'https://justjoin.it/feed.atom'
response = get_response_from_url(URL)
splitted_response = split_response_into_list(response)

temp = create_list_of_offers(splitted_response)
print(temp.offer_address)
print(temp.salary)
print(temp.company)
print(temp.location)
print(temp.offer_name)