from time import time
from ._driver import Webdriver
from ._methods import Methods
from ._gherkin_parser import StepsQueue
from ._custom_exceptions import print_error
from ._enums import Colours


def start():
    try:
        start = time()
        driver = Webdriver()
        driver.start_webdriver()
        methods = Methods()
        methods.load_all_methods()
        steps_queue = StepsQueue(methods, driver)
        steps_queue.prepare_steps()
        steps_queue.start()

    except KeyboardInterrupt as e:
        e.args = ('Interrupted by keyboard', )
        print_error(e)

    except Exception as e:
        print_error(e)

    finally:
        result = '%.2f' % (time() - start)
        print()
        print(Colours.GREEN + 'Finished in: ' + result + 'sec' + Colours.DEFAULT)
        driver.resolve_webdriver()
