from tart.utils.func_utils import cached_property
from tart.log import get_logger


logger = get_logger()


class Device(object):
    def __init__(self, udid):
        self.udid = udid

    def __repr__(self):
        return f"<Device '{self.udid}'>"

    def __str__(self):
        return self.__repr__()

    def method_1(self):
        logger.info(f"This is method 1 for udid: {self.udid}")

    def method_2(self):
        logger.info("This is method 2 for udid: {self.udid}")


def get_device(udid: str) -> Device:
    return Device(udid)
