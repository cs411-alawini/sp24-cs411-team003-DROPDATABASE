import configparser

CONFIG_DIR = './sql_server.ini'


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_DIR)

        print(self.config.sections())
