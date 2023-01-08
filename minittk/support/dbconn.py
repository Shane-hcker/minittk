# -*- encoding: utf-8 -*-
import pymysql

from minittk.support.cfgparser import MyConfigParser


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
        self.mysqlConfigParser = MyConfigParser(cfgfile=cfgfile)
        super().__init__(**self.mysqlConfigParser.getSectionItems('MySQL'), autocommit=True)
        self.csr = self.cursor()
        self.tableDescription = [f"create table if not exists ",
                                 " (`Name` char(255) not null primary key default '', "
                                 "`Value` bigint(255) not null, "
                                 "`Password` bigint(255) null, "
                                 "`Last Modified` date null default CURDATE())"]

    @staticmethod
    def usemysql(cfgfile=None):
        def inner(cls):
            cls._connection = UserConnection(cfgfile=cfgfile)
            cls.run_query = lambda self, *args, **kwargs: cls._connection.run_query(*args, **kwargs)
            cls.show_databases = lambda self: cls._connection.show_databases()
            cls.show_tables = lambda self: cls._connection.show_tables()
            cls.cursor = property(lambda self: cls._connection.csr)
            print(f'{cls} runned usemysql()')
            return cls

        return inner

    def create_table(self, table_name):
        self.run_query(self.tableDescription[0]+table_name+self.tableDescription[1])

    def insert(self, table, *values):
        self.run_query(f'insert into {table} values{values}')
        return values

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

    def show_tables(self):
        return self.run_query('show tables')

    def show_databases(self):
        return self.run_query('show databases')
