import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from ._custom_exceptions import DriverException
from ._enums import Browsers
from . import _config


def _method_decorator(method):
    def method_wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)

        except DriverException as e:
            raise DriverException(e)

    return method_wrapper


def _class_decorator(cls):
    class WrapperClass:
        def __init__(self, *args, **kwargs):
            self.instance = cls(*args, **kwargs)

        def __getattribute__(self, attrib):
            try:
                obj = super().__getattribute__(attrib)
                return obj

            except AttributeError:
                obj = self.instance.__getattribute__(attrib)
                if callable(obj):
                    return _method_decorator(obj)

                else:
                    return obj
    return WrapperClass


@_class_decorator
class Webdriver:
    def __init__(self):
        self.driver = None
        self.parent_driver = None

    def start_webdriver(self, url=None):
        try:
            if url is None:
                url = _config.project_config['main_url']

            self.driver, capabilities = self._get_browser_data(_config.project_config['browser'])
            if _config.project_config['selenium_host'] != 'localhost':
                self.driver = webdriver.Remote(
                    command_executor=_config.project_config['selenium_host'],
                    desired_capabilities=capabilities)

            else:
                self.driver = self.driver()

            if _config.project_config['fullscreen']:
                self.driver.maximize_window()

            self.open_url(url, add_base_url=False)

        except AttributeError:
            raise DriverException('Wrong browser name\n')

        except KeyboardInterrupt as e:
            raise DriverException(str(e) + 'Interrupted by keyboard')

        except DriverException as e:
            raise DriverException(str(e) + 'Problem with initializing driver\n')

    def _get_browser_data(self, browser_name):
        if browser_name.lower() == Browsers.CHROME:
            return webdriver.Chrome, DesiredCapabilities.CHROME

        elif browser_name.lower() == Browsers.EDGE:
            return webdriver.Edge, DesiredCapabilities.EDGE

        elif browser_name.lower() == Browsers.FIREFOX:
            return webdriver.Firefox, DesiredCapabilities.FIREFOX

        elif browser_name.lower() == Browsers.INTERNETEXPLORER:
            return webdriver.Ie, DesiredCapabilities.INTERNETEXPLORER

        elif browser_name.lower() == Browsers.OPERA:
            return webdriver.Opera, DesiredCapabilities.OPERA

        elif browser_name.lower() == Browsers.PHANTOMJS:
            return webdriver.PhantomJS, DesiredCapabilities.PHANTOMJS

        elif browser_name.lower() == Browsers.SAFARI:
            return webdriver.Safari, DesiredCapabilities.SAFARI

        else:
            raise DriverException('Browser ' + browser_name + ' not supported\n')

    def _wait_for_element_be_visible(self, xpath):
        try:
            if _config.project_config['custom_wait']['active']:
                self._custom_wait()

            return WebDriverWait(self.driver, _config.project_config['timeout']).until(
                ec.visibility_of_element_located((By.XPATH, xpath))
            )

        except TimeoutException:
            raise DriverException('Timeout, element ' + xpath + ' not found\n')

    def _wait_for_element_be_present(self, xpath):
        try:
            if _config.project_config['custom_wait']['active']:
                self._custom_wait()

            return WebDriverWait(self.driver, _config.project_config['timeout']).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )

        except TimeoutException:
            raise DriverException('Timeout, element ' + xpath + ' not found\n')

    def _wait_for_element_be_not_present(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
            return WebDriverWait(self.driver, _config.project_config['timeout']).until(
                ec.staleness_of(element)
            )

        except NoSuchElementException:
            return True

        except TimeoutException:
            raise DriverException('Timeout, element is still present\n')

    def _wait_for_element_be_not_visible(self, xpath, timeout=None):
        try:
            if timeout is None:
                timeout = _config.project_config['timeout']

            self.driver.find_element_by_xpath(xpath)
            return WebDriverWait(self.driver, timeout).until(
                ec.invisibility_of_element_located((By.XPATH, xpath))
            )

        except NoSuchElementException:
            return True

        except TimeoutException:
            raise DriverException('Timeout, element is still visible\n')

    def _wait_for_element_be_clickable(self, xpath):
        try:
            if _config.project_config['custom_wait']['active']:
                self._custom_wait()
            return WebDriverWait(self.driver, _config.project_config['timeout']).until(
                ec.element_to_be_clickable((By.XPATH, xpath))
            )

        except TimeoutException:
            raise DriverException('Timeout, element is not clickable\n')

    def _custom_wait(self):
        try:
            timeout = _config.project_config['custom_wait']['custom_timeout']
            for loading_XP in _config.project_config['custom_wait']['loading_object_XP']:
                self._wait_for_element_be_not_visible(loading_XP, timeout=timeout)

        except DriverException as e:
            raise DriverException(e)

    def _url_compare(self, url_compare_method, url):
        try:
            return WebDriverWait(self.driver, _config.project_config['timeout']).until(
                url_compare_method(url)
            )
        except TimeoutException:
            raise DriverException('Timeout, URLs do not match\n')

    def _read_attribute_status(self, attribute_name, attribute_xp):
        try:
            attribute_element = self.driver.find_element_by_xpath(attribute_xp)
            status = attribute_element.get_attribute(attribute_name)
            if status == 'false':
                return False
            elif status == 'true':
                return True

        except DriverException as e:
            raise DriverException(str(e) + 'read attribute failed\n')

    def _javascript_click(self, xpath):
        try:
            script = 'document.evaluate("' + xpath + '", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)' +\
                     '.singleNodeValue.click();'
            self.driver.execute_script(script)

        except DriverException as e:
            raise DriverException(str(e) + 'JS click failed\n')

    def element_is_visible(self, xpath):
        try:
            self._wait_for_element_be_visible(xpath)
            return True

        except DriverException as e:
            raise DriverException(e)

    def element_is_present(self, xpath):
        try:
            self._wait_for_element_be_present(xpath)
            return True

        except DriverException as e:
            raise DriverException(e)

    def element_is_not_visible(self, xpath):
        try:
            self._wait_for_element_be_not_visible(xpath)
            return True

        except DriverException as e:
            raise DriverException(e)

    def element_is_not_present(self, xpath):
        try:
            self._wait_for_element_be_not_present(xpath)
            return True

        except DriverException as e:
            raise DriverException(e)

    def __click_on_checkbox(self, xpath, attribute_name=None, diff_attribute_xp=None): # todo
        try:
            status = None
            attribute_xp = xpath

            element = self._wait_for_element_be_clickable(xpath)
            if attribute_name is not None:
                if diff_attribute_xp is not None:
                    attribute_xp = diff_attribute_xp
                status = self._read_attribute_status(attribute_name, attribute_xp)

            element.click()
            if status is not None:
                tmp = not status
                while tmp is not status:
                    status = self._read_attribute_status(attribute_name, attribute_xp)
            return True

        except DriverException as e:
            raise DriverException(str(e) + 'checkbox failed\n')

    def click(self, xpath):
        try:
            element = self._wait_for_element_be_clickable(xpath)
            element.click()
            return True

        except DriverException as e:
            raise DriverException(str(e) + 'click failed\n')

        except Exception as e:
            print(e)
            print('Other element would receive the click')  # todo
            self._javascript_click(xpath)
            print('JS click used for element: ' + xpath)

    def fill_element(self, xpath, text, enter=False, clear=False):
        try:
            element = self._wait_for_element_be_visible(xpath)
            if clear:
                element.clear()

            element.send_keys(text)
            if not element.get_attribute('value') == text:
                raise DriverException('element can\'t have value\n')

            if enter:
                element.send_keys(Keys.ENTER)

            return True

        except DriverException as e:
            raise DriverException(str(e) + 'filling element has failed\n')

    def open_url(self, url, add_base_url=True):
        try:
            if add_base_url:
                url = _config.project_config['main_url'] + url
            self.driver.get(url)
            self.check_url(url, add_base_url=False)
            return True

        except WebDriverException as e:
            raise DriverException(str(e) + 'url: ' + url + ' is incorrect\n')

        except DriverException as e:
            raise DriverException(str(e) + 'failed to open website\n')

    def check_url(self, url, add_base_url=True, check_exactly=False):
        try:
            if add_base_url:
                url = _config.project_config['main_url'] + url
            if check_exactly:
                self._url_compare(ec.url_to_be, url)
            else:
                self._url_compare(ec.url_contains, url)
            return True

        except DriverException as e:
            raise DriverException(str(e) +
                                  'Current url: ' + self.driver.current_url + '\n' +
                                  'Given url: ' + url + '\n')

    def get_text(self, xpath):
        try:
            return self._wait_for_element_be_visible(xpath).text

        except DriverException as e:
            raise DriverException(str(e) + 'getting text failed\n')

    def open_new_window(self, url):
        try:
            self.parent_driver = self.driver
            world = Webdriver()
            self.driver = world.driver
            self.start_webdriver(url)

        except DriverException as e:
            raise DriverException(str(e) + 'opening new window failed\n')

    def close_new_window(self):
        try:
            self.resolve_webdriver()
            self.driver = self.parent_driver

        except DriverException as e:
            raise DriverException(str(e) + 'closing new window failed\n')

    def upload_file(self, xpath, file_path):
        try:
            element = self._wait_for_element_be_visible(xpath)
            element.send_keys(file_path)

        except DriverException as e:
            raise DriverException(str(e) + 'uploading file failed\n')

    def wait(self, seconds):
        try:
            time.sleep(seconds)

        except DriverException as e:
            raise DriverException(str(e) + 'sleep failed\n')

    def resolve_webdriver(self):
        try:
            self.driver.quit()

        except DriverException as e:
            raise DriverException(str(e) + 'resolve webdriver failed\n')

        except TypeError as e:
            raise DriverException(str(e) + 'QUIT\n')

    def refresh_webdriver(self):
        try:
            self.resolve_webdriver()
            self.start_webdriver()

        except DriverException as e:
            raise DriverException(str(e) + 'refresh webdriver failed\n')

    def refresh_page(self):
        try:
            self.driver.refresh()

        except DriverException as e:
            raise DriverException(str(e) + 'refresh page failed\n')
