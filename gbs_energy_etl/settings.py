import os
import configparser


config = configparser.ConfigParser()
config.read(os.environ.get('CFG_PATH',
                           'gbs_energy_etl/gbs_energy_etl/aws.cfg'))
