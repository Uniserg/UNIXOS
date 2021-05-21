import configparser
import os
from .exceptions import AccessDeniedException
from sys import platform


class Config(object):
    def __init__(self, home_dir=os.getcwd()):
        self.__home = str(home_dir)

    def __get_home(self):
        return self.__home

    def __set_home(self, path):
        if self.__home not in path:
            raise AccessDeniedException("Access denied")

        self.__home = path

    def read_from_cfg(self, cfg_file):
        config = configparser.ConfigParser()
        config.read(cfg_file)

        home_dir = config['properties']["HomeDir"].strip('"')
        if 'win' in platform:
            home_dir = home_dir.replace('/', '\\')
        elif 'ux' in platform:
            home_dir = home_dir.replace('\\', '/')

        # set_home = config['properties']["HomeDir"].strip('"')
        set_home = home_dir

        print(set_home[0])
        if self.__home not in set_home and set_home[0] != '.':
            raise AccessDeniedException("Access denied")

        if set_home[0] == '.':
            set_home = str(os.getcwd()) + set_home.replace(".", "", 1)

        self.__home = set_home

    home = property(__get_home, __set_home)




