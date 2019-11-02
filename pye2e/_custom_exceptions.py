from ._enums import Colours
from ._project_config import config


class CustomException(Exception):
    def __init__(self, *args):
        pass


class DriverException(CustomException):
    def __init__(self, *args):
        pass


class ParserException(CustomException):
    def __init__(self, *args):
        pass


class MethodsException(CustomException):
    def __init__(self, *args):
        pass


class KeyErrorException(CustomException):
    def __init__(self, *args):
        pass


def print_error(error):
    try:
        if "'NoneType' object is not callable" in error.args:
            error.args = ('No function was found for this step',)

        if config['debug']:
            raise error

    finally:
        error_name = type(error).__name__
        print(Colours.RED + '\n' + str(error_name) + ':\n' + str(error) + Colours.DEFAULT)
