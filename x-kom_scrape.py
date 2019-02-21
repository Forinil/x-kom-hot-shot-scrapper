from bs4 import BeautifulSoup
from datetime import datetime
from slackclient import SlackClient
from string import Template
from urllib.request import urlopen

import os
import csv

# Open page
url = 'https://www.x-kom.pl/'
page = urlopen(url)

# Parse page
soup = BeautifulSoup(page, 'html.parser')

# Get product name, old and new price from the parsed page
product_name = soup.find('p', {'class': 'product-name'}).text.strip()
old_price = soup.find('div', {'class': 'old-price'}).text.strip()
new_price = soup.find('div', {'class': 'new-price'}).text.strip()

# Print result to STDOUT
print(product_name, old_price, new_price, sep=';')

# Save result in CSV log file
with open('hot_shot.csv', 'a', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([datetime.now(), product_name, old_price, new_price])

# Login to Slack - API key is expected to be set via environment variable
slack_token = os.environ['SLACK_API_KEY']
sc = SlackClient(slack_token)

# Compose message
message_template = Template('$product_name is now on sale. Old price: $old_price. New price: $new_price.')
message_text = message_template.substitute(product_name=product_name, old_price=old_price, new_price=new_price)

# Send message
sc.api_call(
  'chat.postMessage',
  channel='general',
  text=message_text
)
