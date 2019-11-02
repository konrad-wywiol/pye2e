from enum import Enum


class Type(Enum):
    FEATURE = 1
    SCENARIO = 2
    STEP = 3
    TAG = 4


class Status:
    FAILED = 'Failed'
    SUCCESS = 'Passed'
    SKIPPED = 'Skipped'
    PENDING = 'Pending'


class Colours:
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    DEFAULT = '\033[0m'
    GREY = '\033[90m'


class Browsers:
    CHROME = 'Chrome'
    EDGE = 'Edge'
    FIREFOX = 'Firefox'
    INTERNETEXPLORER = 'IE'
    OPERA = 'Opera'
    PHANTOMJS = 'PhantomJS'
    SAFARI = 'Safari'


class Tags:
    WIP = '@wip'
    DISABLED = '@disabled'
