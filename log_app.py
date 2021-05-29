from log4py import Logger


def log():
    # Basic Config
    __name__ = "__main__"
    config = {
        "handlers": {"file_handler": {"class": "logging.FileHandler", 'filename': 'flask_app.log'}},
        "loggers": {'__main__': {"level": "INFO", "handlers": ["file_handler"], 'propagate': False}}
    }
    Logger.configure(**config)
    log_object = Logger.get_logger(__name__)
    return log_object
