import pathlib
import logging
from datetime import datetime
from configparser import ConfigParser

class AldiCheckerConfig:
    __DEFAULT_CONFIG = "Config/Config.ini"

    def __init__(self, config=None):

        if config is None:
            self.config = __class__.__DEFAULT_CONFIG
        else:
            self.config = config

        self._configparser = ConfigParser(interpolation=None)
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
        pathlib.Path("Logs").mkdir(parents=True, exist_ok=True)
        date = datetime.utcnow().strftime("%d-%b-%Y")
        
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler()
        stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_format)

        file_handler = logging.FileHandler(f"Logs/Checker_{date}.log")
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        return logger