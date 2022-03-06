import os
import time
import logging
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

USERNAME = config.get('electricity_service',"electricity_user")
PASSWORD = config.get('electricity_service',"electricity_pass")
BASE_URL = config.get('electricity_service','electricity_url')
DOWNLOAD_PATH = config.get('water_service','water_download')
DRIVER_PATH = config.get('base','driver_path')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class checarLuz():
    def login(self, driver):
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_txtUsuario")))
            TAG_USERNAME = driver.find_element_by_id('ctl00_MainContent_txtUsuario')
            TAG_USERNAME.send_keys(USERNAME)
            TAG_PASSWORD = driver.find_element_by_id('ctl00_MainContent_txtPassword')
            TAG_PASSWORD.send_keys(PASSWORD)
            logging.info("Filling login form")
            nextButton = driver.find_element_by_id('ctl00_MainContent_btnIngresar')
            nextButton.click()
            logging.info("Submiting form")
        except:
            driver.quit()

    def getReceiptInfo(self,driver):
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_lblMonto")))
            logging.info("Getting information")
            monto=driver.find_element_by_id('ctl00_MainContent_lblMonto')
            periodo=driver.find_element_by_id('ctl00_MainContent_lblPeriodoConsumo')
            num_servicio=driver.find_element_by_id('ctl00_MainContent_lblNumeroServicio')
            fecha_limitie=driver.find_element_by_id('ctl00_MainContent_lblFechaLimite')
            estado_recibo=driver.find_element_by_id('ctl00_MainContent_lblEstadoRecibo')
            logging.info("[+] Monto: " + monto.text)
            logging.info("[+] Periodo: " + periodo.text)
            logging.info("[+] Fecha Limite: " + fecha_limitie.text)
            logging.info("[+] Estado Recibo: " + estado_recibo.text)
            name_file = time.strftime("%Y%m%d-%H%M%S") + ".png"
            screen = driver.save_screenshot(DOWNLOAD_PATH+name_file)

            saldo = {
                'monto' : monto.text,
                'periodo' : periodo.text,
                'fecha_limitie' : fecha_limitie.text,
                'estado_recibo' : estado_recibo.text,
                'screen' : DOWNLOAD_PATH+name_file

            }
        except ValueError as err:
            driver.quit()
        
        return saldo

    def logout(self,driver):
        try:
            time.sleep(5)
            ##Log Out
            logOut = driver.find_element_by_id('ctl00_MenuLateral_lgSalir')
            logOut.click()
            logging.info("Loging Out!")
            #driver.quit()
        except ValueError as err:
            driver.quit()
    
    def consultarSaldoLuz(self):
        logger.info("Consultando Recibo de Luz ...")
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
                "download.default_directory": DOWNLOAD_PATH , "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

        driver.get(BASE_URL)
        logger.info("Opening " + BASE_URL)

        self.login(driver)
        saldoLuz  = self.getReceiptInfo(driver)
        self.logout(driver)

        logger.info("Done!")
        driver.quit()
        return saldoLuz

