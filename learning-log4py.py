# GitHub repo: https://github.com/taogeYT/log4py
# pip install log4py
# This repo has the last commit on on Sep 13, 2020. This is not actively maintained
# Log Record Attribute Docs: https://docs.python.org/3/library/logging.html#logrecord-attributes
from log4py import Logger

config = {
    "handlers": {"file_handler": {"class": "logging.FileHandler", 'filename': 'flask_app.log'}},
    "loggers": {'__main__': {"level": "INFO", "handlers": ["file_handler"], 'propagate': False}}
}
Logger.configure(**config)
log = Logger.get_logger(__name__)


# Testing
class FunctionsMath:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        return self.x + self.y


num1 = 11
num2 = 35

fm = FunctionsMath(num1, num2)
add_result = fm.add()
log.info(f'Added {num1} and {num2}, and the result is {add_result}')
log.warning('Warning')
log.error('This is a custom error message')
log.critical('CRITICAL MAN')
log.debug('Debugging')
