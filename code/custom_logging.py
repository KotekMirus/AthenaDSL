import logging
import js


class CustomWebLogHandler(logging.Handler):
    def __init__(self, prefix="LOG: "):
        super().__init__()
        self.prefix = prefix

    def emit(self, record):
        js.document.log(record.levelname, record.getMessage())
