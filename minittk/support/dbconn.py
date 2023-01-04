# -*- encoding: utf-8 -*-
import pymysql

from .cfgparser import MyConfigParser


class UserConnection(pymysql.Connection):
    """User database connection
    TODO 添加装饰时将该类的方法(需要改写成被添加装饰器的类)全部导入(包括ConfigParser+UserConnection)
    """
    _instance = None
    _init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, cfgfile=None):
        """
        :param cfgfile: only necessary for first init
        """
        if self.__class__._init_flag:
            return
        self.__class__._init_flag = True
        self.cfgParser = MyConfigParser(cfgfile=cfgfile)
        super().__init__(**self.cfgParser.getSectionItems('MySQL'), autocommit=True)
        self.csr = self.cursor()

    def run_query(self, query, fetch=None):
        self.csr.execute(query)
        match fetch:
            case None | 'all':
                return self.csr.fetchall()
            case 'one':
                return self.csr.fetchone()
            case _:
                raise AttributeError(f'unknown value {fetch} for argument fetch')

    def use(self, db: str) -> None:
        self.run_query(f'use {db}')


def usemysql(cfgfile=None):
    def inner(cls):
        cls._connection = UserConnection(cfgfile=cfgfile)
        return cls
    return inner
