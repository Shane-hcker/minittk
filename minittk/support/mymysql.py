# -*- encoding: utf-8 -*-
from minittk import *


class MySQLMixIn(pymysql.Connection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type is not None:
            raise exc_type()

    @property
    def cursor(self):
        """Get Cursor"""
        return 1