from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from AldiCheckerConfig import AldiCheckerConfig

class AldiChecker:
    def __init__(self):
        self.config = AldiCheckerConfig()
        self.logger = self.config.logger

    def getPrice(self, url):
        self.logger.info(f"Checking url {url}")
        svc = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument("start-maximized")

        driver = webdriver.Chrome(service=svc, options=options)
        
        driver.get(url)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
        except Exception as e:
            print(f"Error Occured. Error={e}")
        else:
            driver.find_element_by_id("onetrust-accept-btn-handler").click()

            source_code = BeautifulSoup(driver.page_source, 'html.parser')
            name = source_code.find('h1', {'class': 'product-details__name'}).text
            price = source_code.find('span', {'class' : 'product-price__value'}).text
            driver.save_screenshot(self.config.screenshot)
            return (name, price)
        finally:
            driver.quit()
    
    def send_alert(self, msg):
        self.logger.info('Sending alert')
        photo_file = {'photo': open(self.config.screenshot, 'rb')}
        send_text = f"https://api.telegram.org/bot{self.config.token}/sendPhoto?chat_id={self.config.chatId}&caption={msg}"
        try:
            response = requests.post(send_text, files=photo_file,)
            response.raise_for_status()
        except HTTPError as http_err:
            self.logger.error(f'HTTP error occurred: {http_err}')
        else:
            self.logger.info('Alert sent to telegram chat.')

    def main(self):
        name, str_price  = self.getPrice(self.config.url)
        price = self.getNum(str_price)
        base_price = self.getNum(self.config.basePrice)

        if isinstance(price, (int, float)):
            if price == base_price:
                msg = f"NO CHANGE:\nProduct Name: {name}.\nThe current price is same as base price of {base_price}"
            elif price < base_price:
                msg = f"BARGAIN:\nProduct Name: {name}.\nThe current price is lower than base price.\nBase price: {base_price}\nCurrent price: {price}"
            elif price > base_price:
                msg = f"INFLATION ALERT:\nProduct Name: {name}.\nThe price just went up.\nBase price: {base_price}\nCurrent price: {price}"
        else:
            msg = f"Product Name: {name}.\n {price}"

        try:
            self.send_alert(msg)
        except Exception as e:
            self.logger.error(f"Failed to send notification. Erro={e}")
    
    @staticmethod
    def getNum(n: str):
        if "£" in n:
            n = n.replace("£", "")

        if n.isdigit():
            number = int(n)
        else:
            try:
                number = float(n)
            except ValueError:
                number = n
        return number

if __name__ == "__main__":
    p = AldiChecker()
    p.main()



