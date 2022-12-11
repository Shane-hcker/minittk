# -*- encoding: utf-8 -*-
from minittk import *


class UserDBMixIn(pymysql.Connection):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cfg=None, **kwargs):
        # if any condition satisfied, load the .ini file
        if cfg is not None:
            return
        super().__init__(**kwargs, autocommit=True)

    @staticmethod
    def load_DBcfg(cfgdir):
        """load cfg file with a default format"""
        pass

    @classmethod
    def new_conn(cls, cfg=None, **kwargs):
        return cls(cfg, **kwargs)
