import logging

log = logging.getLogger(__name__)


class UI:
    def status(self, message: str) -> None:
        log.info(message)

    def warning(self, message: str) -> None:
        log.warn(message)

    def error(self, message: str) -> None:
        log.error(message)
