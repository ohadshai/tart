from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil

PACKAGE_NAME = 'tart-tatin'

PACKAGES = [p for p in find_packages() if not p.startswith('tests')]
BASE_DIR = os.path.realpath((os.path.dirname(__file__)))
HOME = os.path.expanduser('~')
TART_CACHE_DIR = os.path.join(HOME, '.tart')
CONFIG_RELATIVE_PATH = os.path.join('tart', 'config', 'tart.cfg')


class TartInstall(install):
    def run(self):
        super().run()
        os.makedirs(TART_CACHE_DIR, exist_ok=True)
        shutil.copy(CONFIG_RELATIVE_PATH, TART_CACHE_DIR)


def parse_requirements():
    reqs = []
    with open(os.path.join(BASE_DIR, 'requirements.txt')) as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                reqs.append(line)
    return reqs


def readfile(filenname):
    with open(filenname) as f:
        text = f.read().strip()
    return text


setup(
    name=PACKAGE_NAME,
    version=readfile('VERSION'),
    description='Python Library for IOS device controller',
    long_description=readfile('README.md'),
    author='ohads',
    author_mail='shai.ohad@gmail.com',
    cmdclass={"install": TartInstall},
    install_requires=parse_requirements(),
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'itart = tart.scripts:main',
            'tart = tart.cli_main:cli'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        ],
    tests_require=['pytest']
)
