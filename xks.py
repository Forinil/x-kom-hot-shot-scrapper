import logging.config
import os
import sys

from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from XKomProcessor import XKomProcessor
from exceptions import ProcessingException

logger = logging.getLogger(__name__)


@retry(before_sleep=before_sleep_log(logger, logging.ERROR),  # Log before retrying
       reraise=True,  # Reraise last exception instead of raising RetryError
       retry=retry_if_exception_type(ProcessingException),  # Only retry after ProcessingException
       stop=stop_after_attempt(12),  # Stop after 12 attempts (roughly 136 minutes)
       wait=wait_exponential(max=8192))  # Increase wait time after each failure exponentially, up to 8192 seconds
def process_page(page_processor):
    page_processor.process()


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
        process_page(processor)
    except ProcessingException as ex:
        logger.exception("Exception raised while processing: %s", ex, exc_info=True)
        print("Error determining current Hot Shot Deal (", ex, ") - see application log for details", file=sys.stderr)
        exit(1)
