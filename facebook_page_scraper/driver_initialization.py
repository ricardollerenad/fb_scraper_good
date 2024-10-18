#!/usr/bin/env python3
"""""" 
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import logging
from pymongo import MongoClient

# Configuración de logging
logger = logging.getLogger(__name__)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(format)
logger.addHandler(ch)

class Initializer:
    def __init__(self, browser_name, proxy=None, headless=True, mongo_uri=None, db_name=None, collection_name=None):
        self.browser_name = browser_name
        self.proxy = proxy
        self.headless = headless
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        if mongo_uri and db_name and collection_name:
            self.connect_to_mongodb(mongo_uri, db_name, collection_name)

    def connect_to_mongodb(self, mongo_uri, db_name, collection_name):
        """Conecta a MongoDB y asigna la colección."""
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name][collection_name]
        logger.info("Conectado a MongoDB en la colección: {}".format(collection_name))

    def set_properties(self, browser_option):
        """Agrega capacidades al driver."""
        if self.headless:
            browser_option.add_argument('--headless')
        browser_option.add_argument('--no-sandbox')
        browser_option.add_argument("--disable-dev-shm-usage")
        browser_option.add_argument('--ignore-certificate-errors')
        browser_option.add_argument('--disable-gpu')
        browser_option.add_argument('--log-level=3')
        browser_option.add_argument('--disable-notifications')
        browser_option.add_argument('--disable-popup-blocking')
        return browser_option

    def set_driver_for_browser(self, browser_name):
        """Espera un nombre de navegador y devuelve una instancia de driver."""
        logger.setLevel(logging.INFO)
        if browser_name.lower() == "chrome":
            browser_option = ChromeOptions()
            if self.proxy is not None:
                options = {
                    'https': 'https://{}'.format(self.proxy.replace(" ", "")),
                    'http': 'http://{}'.format(self.proxy.replace(" ", "")),
                    'no_proxy': 'localhost, 127.0.0.1'
                }
                logger.info("Usando proxy: {}".format(self.proxy))

            try:
                service = ChromeService(ChromeDriverManager(version="129.0.6668").install())
                ## service = ChromeService(ChromeDriverManager().install()) --> el valor a cambiar
                return webdriver.Chrome(service=service, options=self.set_properties(browser_option), seleniumwire_options=options if self.proxy else {})
            except Exception as e:
                logger.error("Error al iniciar el driver de Chrome: {}".format(e))
                raise

        elif browser_name.lower() == "firefox":
            browser_option = FirefoxOptions()
            if self.proxy is not None:
                options = {
                    'https': 'https://{}'.format(self.proxy.replace(" ", "")),
                    'http': 'http://{}'.format(self.proxy.replace(" ", "")),
                    'no_proxy': 'localhost, 127.0.0.1'
                }
                logger.info("Usando proxy: {}".format(self.proxy))

            try:
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=self.set_properties(browser_option), seleniumwire_options=options if self.proxy else {})
            except Exception as e:
                logger.error("Error al iniciar el driver de Firefox: {}".format(e))
                raise

        else:
            raise Exception("¡Navegador no soportado!")

    def init(self):
        """Devuelve una instancia del driver."""
        driver = self.set_driver_for_browser(self.browser_name)
        return driver

    def save_data_to_mongodb(self, data):
        """Guarda datos en MongoDB."""
        if self.collection:
            if isinstance(data, list):
                self.collection.insert_many(data)
            else:
                self.collection.insert_one(data)
            logger.info("Datos guardados en MongoDB.")
        else:
            logger.warning("No hay conexión a la colección de MongoDB.")
