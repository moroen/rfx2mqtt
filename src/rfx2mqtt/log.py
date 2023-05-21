import logging
from django.core.management.color import color_style

from django.conf import settings


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;1m"
    reset = "\x1b[0m"

    style = color_style

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = color_style()
        self.fmt = "%(name)15s | %(levelname)8s | %(message)s"
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_log(module: str) -> logging.Logger:
    if settings.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    log = logging.getLogger(module)
    if not log.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(CustomFormatter())
        log.addHandler(handler)
        log.propagate = False

    return log


# daphne = logging.getLogger("daphne")
# daphne.propagate = False

# server = logging.getLogger("django.channels.server")
# server.propagate = False

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# handler.setFormatter(CustomFormatter())
# daphne.addHandler(handler)

# root = logging.getLogger()
# root.addHandler(handler)

# root.setLevel(logging.WARN)
# root.propagate = False

# print(logging.root.manager.loggerDict)
