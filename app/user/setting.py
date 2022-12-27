# -*- encoding: utf-8 -*-
from minittk import *


class SettingPage(MyWindow):
    def __init__(self):
        self.cfgParser = MyConfigParser()
        posX, posY = self.cfgParser.getint('App', 'startupX'), self.cfgParser.getint('App', 'startupY')
        super().__init__('Title', '600x400', (False, False), (posX+600, posY+20))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise exc_type()
