# -*- encoding: utf-8 -*-
from minittk import *


class UserDBMixIn(pymysql.Connection):
    def __init__(self, cfg=None, **kwargs):
        # if any condition satisfied, load the .ini file
        if not cfg:
            super().__init__(**kwargs, autocommit=True)
            return

    @staticmethod
    def load_DBcfg(cfgdir):
        """load cfg file with a default format"""
        pass

    @classmethod
    def new_conn(cls, cfg=None, **kwargs):
        return cls(cfg, **kwargs)


class DefaultDBMixIn(UserDBMixIn):
    """可以在多个类中创建，单例模式可以保证他们都指向一个MySQL类"""
    _instance = None
    _init_flag = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, cfg=None, **kwargs):
        if self.__class__._init_flag:
            return
        self.__class__._init_flag = True
        if cfg:
            pass
        super().__init__(cfg, **kwargs)
