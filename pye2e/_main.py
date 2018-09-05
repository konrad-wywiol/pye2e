from . import _config
from ._driver import Webdriver
from ._methods import Methods
from ._gherkin_parser import StepsQueue
from ._custom_exceptions import print_error, CustomException, DriverException


def start(config):
    try:
        _config.change_config(config)
        driver = Webdriver()
        driver.start_webdriver()
        methods = Methods()
        methods.load_all_methods()
        steps_queue = StepsQueue(methods, driver)
        steps_queue.prepare_steps()
        steps_queue.start()

    except CustomException as e:
        print_error(e)

    finally:
        try:
            driver.resolve_webdriver()

        except DriverException:
            pass
