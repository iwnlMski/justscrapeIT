import requests
from bs4 import BeautifulSoup

r = requests.get('https://justjoin.it/all/python')
soup = BeautifulSoup(r.text, 'html.parser')

print(soup.prettify())
# class='css-ic7v2w'