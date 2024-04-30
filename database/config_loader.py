import configparser
import os

CONFIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'sql_server.ini')


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_DIR)

        print(self.config.sections())
