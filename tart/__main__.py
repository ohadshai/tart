from tart.config.config import get_config
from tart.device import Device
from tart.log import configure_logger, get_logger

logger = get_logger()

class Tart(object):
    def __init__(self):
        self.config = get_config()

    def __repr__(self):
        return f"<Tart>"

    def __str__(self):
        return self.__repr__()

    def method_1(self):
        logger.info(f"This is method 1 for {self.__class__.__name__}")

    def method_2(self):
        logger.info(f"This is method 2 for {self.__class__.__name__}")


def get_tart() -> Tart:
    return Tart()
