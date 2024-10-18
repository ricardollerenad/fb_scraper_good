#!/usr/bin/env python3
"""""" 
from seleniumwire import webdriver
# to add capabilities for chrome and firefox, import their Options with different aliases
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# import webdriver for downloading respective driver for the browser
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import logging

logger = logging.getLogger(__name__)
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(format)
logger.addHandler(ch)

class Initializer:

    def __init__(self, browser_name, proxy=None, headless=True):
        self.browser_name = browser_name
        self.proxy = proxy
        self.headless = headless

    def set_properties(self, browser_option):
        """adds capabilities to the driver"""
        if self.headless:
            browser_option.add_argument('--headless')  # runs browser in headless mode
        browser_option.add_argument('--no-sandbox')
        browser_option.add_argument("--disable-dev-shm-usage")
        browser_option.add_argument('--ignore-certificate-errors')
        browser_option.add_argument('--disable-gpu')
        browser_option.add_argument('--log-level=3')
        browser_option.add_argument('--disable-notifications')
        browser_option.add_argument('--disable-popup-blocking')
        return browser_option

    def set_driver_for_browser(self, browser_name):
        """expects browser name and returns a driver instance"""
        logger.setLevel(logging.INFO)
        # if browser is supposed to be chrome
        if browser_name.lower() == "chrome":
            browser_option = ChromeOptions()
            # automatically installs chromedriver and initialize it and returns the instance
            if self.proxy is not None:
                options = {
                    'https': 'https://{}'.format(self.proxy.replace(" ", "")),
                    'http': 'http://{}'.format(self.proxy.replace(" ", "")),
                    'no_proxy': 'localhost, 127.0.0.1'
                }
                logger.info("Using: {}".format(self.proxy))
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=self.set_properties(browser_option), seleniumwire_options=options)

            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=self.set_properties(browser_option))
        
        elif browser_name.lower() == "firefox":
            browser_option = FirefoxOptions()
            if self.proxy is not None:
                options = {
                    'https': 'https://{}'.format(self.proxy.replace(" ", "")),
                    'http': 'http://{}'.format(self.proxy.replace(" ", "")),
                    'no_proxy': 'localhost, 127.0.0.1'
                }
                logger.info("Using: {}".format(self.proxy))
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=self.set_properties(browser_option), seleniumwire_options=options)

            # automatically installs geckodriver and initialize it and returns the instance
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=self.set_properties(browser_option))
        
        else:
            # if browser_name is not chrome nor firefox then raise an exception
            raise Exception("Browser not supported!")

    def init(self):
        """returns driver instance"""
        driver = self.set_driver_for_browser(self.browser_name)
        return driver
