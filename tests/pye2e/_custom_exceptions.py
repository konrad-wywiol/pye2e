from config import project_config
from ._enums import Colours


class DriverException(Exception):
    def __init__(self, *args):
        pass


class ParserException(Exception):
    def __init__(self, *args):
        pass


class MethodsException(Exception):
    def __init__(self, *args):
        pass


def print_error(error):
    try:
        if "'NoneType' object is not callable" in error.args:
            error.args = ('No function was found for this step',)

        if project_config.debug:
            raise error

    finally:
        error_name = type(error).__name__
        print(Colours.RED + '\n' + str(error_name) + ':\n' + str(error) + Colours.DEFAULT)
