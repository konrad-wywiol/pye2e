import os
from os.path import dirname as up
from enum import Enum


class Directories:
    ROOT = up(up(up(os.path.abspath(__file__)))) + '/'
    MAIN = ROOT + 'tests/'
    CONFIG = MAIN + 'config/'
    DATA = MAIN + 'data/'
    FILES = DATA + 'files/'
    FEATURES = MAIN + 'features/'
    PAGES = MAIN + 'pages/'
    PYE2E = MAIN + 'pye2e/'
    PRIVATE = PYE2E + 'private/'


class Type(Enum):
    FEATURE = 1
    SCENARIO = 2
    STEP = 3
    TAG = 4


class Status(Enum):
    FAILED = 1
    SUCCESS = 2


class Colours:
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    DEFAULT = '\033[0m'
