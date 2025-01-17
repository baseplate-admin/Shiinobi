from shiinobi.utilities import get_logger

__all__ = ["LogFacade"]


class LogFacade:
    def __init__(self):
        # Logger
        self.logger = get_logger()
