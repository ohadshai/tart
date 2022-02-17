import os
from configparser import ConfigParser, ExtendedInterpolation
from colored import fore, style

from tart.utils.dictionary_representor import DictionaryRepresentor

HOME = os.path.expanduser('~')
CONFIG_PATH = os.path.join(HOME, '.tart', 'tart.cfg')
DEV_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tart.cfg')


class Singelton(type):
    _instances ={}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singelton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TartConfig(metaclass=Singelton):
    def __init__(self, path=CONFIG_PATH):
        self.parser = ConfigParser(interpolation=ExtendedInterpolation())
        self.path = path
        self.load()

    def load(self):
        if not os.path.exists(CONFIG_PATH):
            print(f"{fore.YELLOW}Development mode - config file is on: '{DEV_CONFIG_PATH}' {style.RESET}")
            self.path = DEV_CONFIG_PATH
        found = self.parser.read()
        if not found:
            raise ValueError(f"config file doesn't exists in path - {self.path}")
        for section in self.parser.sections():
            self.__dict__.update({section: DictionaryRepresentor(dict())})
            for key, value in self.parser.items(section):
                if '~' in value:
                    value = os.path.expanduser(value)
                try:
                    value = int(value)
                    self.parser._defaults[section][key] = value
                except:
                    pass
                self.__dict__[section][key] = value

    def write(self, section, key, value):
        self.parser[section][key] = value
        self.parser.write(open(self.path, 'w'))


def get_config(path: str = None):
    return TartConfig(path=path or CONFIG_PATH)
