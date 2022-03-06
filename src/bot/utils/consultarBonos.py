import os
import time
import logging
import datetime
import requests
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config/config.ini')
config = ConfigParser()
config.read(initfile)

BASE_URL = config.get('bonos','bond_url')
DRIVER_PATH = config.get('base','driver_path')
DOWNLOAD_PATH = config.get('water_service','water_download')
BOND_HISTORY = config.get('bonos','bond_history')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class checadorBonos():

    def __init__(self):
        #Configuracion inicial
        logger.info("Sin configuración Inicial ...")


    def login(self, driver,user, password):
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Email"]')))
            TAG_USERNAME = driver.find_element(by=By.XPATH, value='//*[@id="Email"]')
            TAG_USERNAME.send_keys(user)
            TAG_PASSWORD = driver.find_element(by=By.XPATH, value='//*[@id="Password"]')
            TAG_PASSWORD.send_keys(password)
            logger.info("Filling login form")
            nextButton = driver.find_element(by=By.XPATH, value='//*[@id="btnLogIn"]')
            nextButton.click()
            logger.info("Submiting form")
        except ValueError as err:
            logger.error("Error in login")
            driver.quit()

    def getBalanceInfo(self, driver):
        try:
            check = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-balance')))
            logger.info("Getting debt Info")
            balance = driver.find_element(by=By.CLASS_NAME, value='card-balance')
            while balance.text == "$--.--":
                balance = driver.find_element(by=By.CLASS_NAME, value='card-balance')
                logger.info("Esperando tiempo de carga" + balance.text)
            logger.info("Saldo de Bonos:" + balance.text)

        except ValueError as err:
            logger.error("Error in getReceiptInfo")
            driver.quit()

        return balance.text

    def logout(self, driver):
        try:
            ##Log Out
            time.sleep(5)
            close = driver.find_element(by=By.XPATH, value='//*[@id="div-sidebar-wrapper"]/ul/li[4]/ul/li[13]/a')
            close.click()
            logger.info("Log Out!")
        except ValueError as err:
            logger.error("Error in logout")
            driver.quit()

    def consultarSaldoBonos(self, user, password):
        logger.info("Running Bond Script ...")
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
                "download.default_directory": DOWNLOAD_PATH , "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

        driver.get(BASE_URL)
        logger.info("Opening " + BASE_URL)

        self.login(driver,user, password)
        saldo = self.getBalanceInfo(driver)
        self.logout(driver)

        logger.info("Done!")
        driver.quit()
        return saldo