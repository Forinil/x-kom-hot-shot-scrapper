import logging.config
import os

from exceptions import ProcessingException
from XKomProcessor import XKomProcessor

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Calculate default log directory - logs subdirectory of directory containing this script
    default_log_path = os.path.join(os.path.dirname(__file__), 'logs')

    # Read configuration from environment variables
    slack_api_token = os.environ['SLACK_API_KEY']
    slack_channel = os.getenv('XKS_CHANNEL', 'general')
    log_directory = os.getenv('LOG_DIR', default_log_path)

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
                'filename': os.path.join(log_directory, 'application.log'),
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

    # Initialize x-kom page processor
    processor = XKomProcessor(slack_api_token, slack_channel)

    # process page
    try:
        processor.process()
    except ProcessingException as ex:
        logger.exception("Exception raised while processing: %s", ex, exc_info=True)
