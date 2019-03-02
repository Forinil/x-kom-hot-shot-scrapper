import os

from XKomProcessor import XKomProcessor

if __name__ == '__main__':
    # Read configuration from environment variables
    slack_api_token = os.environ['SLACK_API_KEY']
    slack_channel = os.getenv('XKS_CHANNEL', 'general')

    # Initialize x-kom page processor
    processor = XKomProcessor(slack_api_token, slack_channel)

    # process page
    processor.process()
