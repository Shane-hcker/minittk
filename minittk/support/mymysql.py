# -*- encoding: utf-8 -*-
from minittk import *


class MySQLMixIn(pymysql.Connection):
    _instance = None
    __init_flag = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__()
        return cls._instance

    def __init__(self, cfgdir=None, loadcfg=False, **kwargs):
        if self.__class__.__init_flag:
            return
        self.__class__.__init_flag = True
        # if any condition satisfied, load the .ini file
        if loadcfg or cfgdir or not kwargs:
            pass
        super().__init__(**kwargs)
