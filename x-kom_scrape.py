from bs4 import BeautifulSoup
from datetime import datetime
from slackclient import SlackClient
from urllib.request import urlopen

import os
import csv

url = 'https://www.x-kom.pl/'

page = urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

product_name = soup.find('p', {'class': 'product-name'}).text.strip()
old_price = soup.find('div', {'class': 'old-price'}).text.strip()
new_price = soup.find('div', {'class': 'new-price'}).text.strip()

print(product_name, old_price, new_price, sep=';')

with open('hot_shot.csv', 'a', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([datetime.now(), product_name, old_price, new_price])

slack_token = os.environ['SLACK_API_KEY']
sc = SlackClient(slack_token)

sc.api_call(
  'chat.postMessage',
  channel='general',
  text=product_name + ' is now on sale. Old price: ' + old_price + '. New price: ' + new_price + '.'
)
