import csv
import re
from datetime import datetime
from string import Template
from urllib.request import urlopen

from bs4 import BeautifulSoup
from slackclient import SlackClient


def _fetch_home_page():
    # Fetch x-kom home page content from the internet
    return urlopen('https://www.x-kom.pl/')


def _parse_home_page(page_content):
    # Parse x-kom home page using BeautifulSoup library
    soup = BeautifulSoup(page_content, 'html.parser')

    # Get product name, old and new price from the parsed home page
    product_name = soup.find('p', {'class': 'product-name'}).text.strip()
    old_price = soup.find('div', {'class': 'old-price'}).text.strip()
    new_price = soup.find('div', {'class': 'new-price'}).text.strip()

    # Get link to product page from parsed home page
    hot_shot_script = soup.find_all('script', {'type': 'text/javascript'})[1].text.strip()
    regexp = re.compile(r"/goracy_strzal/\d+")
    hot_shot_url = regexp.search(hot_shot_script).group(0)

    return [product_name, old_price, new_price, hot_shot_url]


def save_results_to_csv_log(product_name, old_price, new_price):
    # Save page parsing results to file hot_shot.csv in current working directory
    with open('hot_shot.csv', 'a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([datetime.now(), product_name, old_price, new_price])


class XKomProcessor:
    def __init__(self, _slack_api_token, _slack_channel):
        # Initialize instance with value of Slack API token and name of channel to post messages to
        self.__slack_api_token = _slack_api_token
        self.__slack_channel = _slack_channel

    def __login_to_slack(self):
        # Login to slack
        return SlackClient(self.__slack_api_token)

    def __send_message_to_slack(self, slack_client, product_name, old_price, new_price, hot_shot_url):
        # Compose message
        message_template = Template('><https://www.x-kom.pl$hot_shot_url|*$product_name*> is now on sale.\n>Old price: '
                                    '$old_price.\n>New price: $new_price.')
        message_text = message_template.substitute(hot_shot_url=hot_shot_url,
                                                   product_name=product_name,
                                                   old_price=old_price,
                                                   new_price=new_price)

        # Send message
        slack_client.api_call(
            'chat.postMessage',
            channel=self.__slack_channel,
            text=message_text,
            unfurl_links=True,
            unfurl_media=True
        )

    # noinspection PyUnreachableCode
    def process(self):
        # Open home page
        page_content = _fetch_home_page()

        # Parse home page
        product_name, old_price, new_price, hot_shot_url = _parse_home_page(page_content)

        # Print result to STDOUT if run in debugging mode
        if __debug__:
            print(product_name, old_price, new_price, hot_shot_url, end='\n', sep=';')

        # Save result in CSV log file
        save_results_to_csv_log(product_name, old_price, new_price)

        # Login to Slack - API key is expected to be set via environment variable
        slack_client = self.__login_to_slack()

        # Send message to Slack
        self.__send_message_to_slack(slack_client, product_name, old_price, new_price, hot_shot_url)


# Allow execution of the module
if __name__ == '__main__':
    import sys

    # Read configuration from script arguments
    slack_api_token = sys.argv[1]
    slack_channel = sys.argv[2]

    # Initialize x-kom page processor
    processor = XKomProcessor(slack_api_token, slack_channel)

    # process page
    processor.process()
