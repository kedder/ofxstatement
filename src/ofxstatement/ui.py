import logging

log = logging.getLogger(__name__)


class UI(object):
    def status(self, message):
        log.info(message)

    def warning(self, message):
        log.warn(message)

    def error(self, message):
        log.error(message)
