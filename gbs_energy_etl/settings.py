import os
import configparser


config = configparser.ConfigParser()
config.read(os.environ.get('CFG_PATH', os.path.dirname(__file__) + '/aws.cfg'))
