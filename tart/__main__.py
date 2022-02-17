from pymobiledevice3.usbmux import list_devices

from tart.config.config import get_config
from tart.device import Device
from tart.exceptions import NoDeviceError, MissingDevice
from tart.log import configure_logger, get_logger


class Tart(object):
    def __init__(self):
        self.config = get_config()

    @staticmethod
    def list_udids():
        return [d.serial for d in list_devices()]

    @staticmethod
    def get_device(udid: str = None, enable_random: bool = True):
        udids = Tart.list_udids()
        if len(udids) == 0:
            raise NoDeviceError("No devices connected")
        if not udid:
            # Get Random Device
            if enable_random or len(udids) == 1:
                device = Device(udids[0])
            else:
                raise NoDeviceError("More than one device connected and enable_random=False")
        else:
            if udid in udids:
                device = Device(udid)
            else:
                raise MissingDevice(f"missing {udid} in {udids}")
        return device

    @staticmethod
    def get_devices():
        udids = Tart.list_udids()
        if len(udids) == 0:
            raise NoDeviceError("No devices connected")
        return [Device(udid) for udid in udids]

    @staticmethod
    def configure_logger(level):
        configure_logger(level=level)

    @staticmethod
    def get_logger(name='Tart'):
        return get_logger(name=name)