from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ._enums import Browsers as BROWSERS
from ._custom_exceptions import DriverException


class _Browser:
    def __init__(self):
        self.headless = False
        self.selenium_host = ''
        self.fullscreen = True

    def run_and_return_driver(self):
        if self.selenium_host and self.selenium_host != 'localhost':
            return webdriver.Remote(
                command_executor=self.selenium_host,
                desired_capabilities=self.capabilities)

        if self.headless:
            return self.run_headless_mode() 

        return self.run_normal_mode()

    def run_normal_mode(self):
        self.driver = self.driver()
        if self.fullscreen:
            self.driver.maximize_window()

        return self.driver

    def run_headless_mode(self):
        raise DriverException('Headless mode for browser ' + browser_name + ' is not supported yet\n')

def get_browser(browser_name):
    class _Browsers:
        class Chrome(_Browser):
            def __init__(self):
                self.driver = webdriver.Chrome
                self.capabilities = DesiredCapabilities.CHROME
            
            def run_headless_mode(self):
                options = webdriver.chrome.options.Options()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')

                return webdriver.Chrome(chrome_options=options)

        class Edge(_Browser):
            def __init__(self):
                self.driver = webdriver.Edge
                self.capabilities = DesiredCapabilities.EDGE

        class Firefox(_Browser):
            def __init__(self):
                self.driver = webdriver.Firefox
                self.capabilities = DesiredCapabilities.FIREFOX

            def run_headless_mode(self):
                options = webdriver.firefox.options.Options()
                options.headless = True

                return webdriver.Firefox(options=option)

        class IE(_Browser):
            def __init__(self):
                self.driver = webdriver.Ie
                self.capabilities = DesiredCapabilities.INTERNETEXPLORER

        class Opera(_Browser):
            def __init__(self):
                self.driver = webdriver.Opera
                self.capabilities = DesiredCapabilities.OPERA

        class PhantomJS(_Browser):
            def __init__(self):
                self.driver = webdriver.PhantomJS
                self.capabilities = DesiredCapabilities.PHANTOMJS

        class Safari(_Browser):
            def __init__(self):
                self.driver = webdriver.Safari
                self.capabilities = DesiredCapabilities.SAFARI

    try:
        browser_class_name = getattr(BROWSERS, browser_name.upper())
        browser_class = getattr(_Browsers, browser_class_name)
        browser_obj = browser_class()

        return browser_obj

    except AttributeError:
        raise DriverException('Browser ' + browser_name + ' not supported\n')
