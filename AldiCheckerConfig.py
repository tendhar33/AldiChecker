import logging
from configparser import ConfigParser
class AldiCheckerConfig:
    __DEFAULT_CONFIG = "Config/Config.ini"

    def __init__(self, config=None):

        if config is None:
            self.config = __class__.__DEFAULT_CONFIG
        else:
            self.config = config

        self._configparser = ConfigParser()
        self._configparser.read(self.config)

    @property
    def url(self):
        return self._configparser.get('product', 'product_url')

    @property
    def basePrice(self):
        return self._configparser.get('product', 'base_price')

    @property
    def token(self):
        return self._configparser.get('telegram', 'bot_token')

    @property
    def chatId(self):
        return self._configparser.get('telegram', 'chat_id')
    
    @property
    def screenshot(self):
        return 'screenshot.png'

    @property
    def logger(self):
        #logging.basicConfig(filename='Logs/AldiChecker.log', filemode='w', )
        logger = logging.getLogger(__name__)

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler("Checker.log")
        c_handler.setFormatter(logging.WARNING)
        f_handler.setLevel(logging.ERROR)

        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger