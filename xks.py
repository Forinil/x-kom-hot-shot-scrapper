import logging.config
import os

from XKomProcessor import XKomProcessor

if __name__ == '__main__':
    # Initialize logging
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': os.path.join('logs', 'application.log'),
                'encoding': 'utf8',
                'backupCount': 5,
                'maxBytes': 5242880
            },
        },
        'loggers': {
            '': {
                'handlers': ['default_handler'],
                'level': 'DEBUG',
                'propagate': False
            }
        }
    }
    logging.config.dictConfig(logging_config)

    # Read configuration from environment variables
    slack_api_token = os.environ['SLACK_API_KEY']
    slack_channel = os.getenv('XKS_CHANNEL', 'general')

    # Initialize x-kom page processor
    processor = XKomProcessor(slack_api_token, slack_channel)

    # process page
    processor.process()
