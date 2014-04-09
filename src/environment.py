"""
Created on 12.10.2013
@author: Jan Jakubcik
@description: Initializes all enviroment settings.
"""


import os
import sys
import logging
import common.constant.Folders as FOLDER
from common.utils.JsonUtils import load_json_from_file

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Environment:
    __metaclass__ = Singleton

    def __init__(self):
        """"Inits the applications and later loads enviroment. First take enviroment variables, if not aviable set it to defaults."""
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(self.app_path, FOLDER.ENVIRONMENT)
        self.init_logger()

    def init_logger(self):
        """Initialize job logger"""
        logger = logging.getLogger('')
        logging.FileHandler(os.path.join(self.app_path,FOLDER.LOGS,"job.log"))
        formatter = logging.Formatter('%(message)s')
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

    def get_property(self, key, default="Not Specified."):
        if(key in self.properties):
            return self.properties[key]
        else:
            return default

    def load_properties(self):
        """Load enviroment variables."""
        data = load_json_from_file(os.path.join(self.path,"default.json"))
        self.properties = data['environment']
        for env_item in self.properties:
            if os.environ.has_key(env_item):
                self.properties[env_item] = os.environ[env_item]

env = Environment()
