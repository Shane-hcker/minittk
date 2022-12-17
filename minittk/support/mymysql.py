# -*- encoding: utf-8 -*-
from minittk import *


class UserDatabaseConnection(pymysql.Connection):
    def __init__(self, cfgfile):
        # TODO cfgfile加载引用DefaultConfigParser
        super().__init__(**DefaultConfigParser(cfgfile).get_mysql(), autocommit=True)

    # @classmethod
    # def new_conn(cls, cfg=None):
    #     return cls(cfg, **kwargs)
