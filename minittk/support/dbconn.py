# -*- encoding: utf-8 -*-
import pymysql
from functools import partial
from minittk.support.cfgparser import MyConfigParser


class UserConnection(pymysql.Connection):
    """User database connection"""
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
        print('going through UserConnection.__init__()')
        self.__class__._init_flag = True
        self.mysqlConfigParser = MyConfigParser(cfgfile=cfgfile)
        super().__init__(**self.mysqlConfigParser.getSectionItems('MySQL'), autocommit=True)
        self.csr = self.cursor()
        self.tableDescription = ["create table if not exists ",
                                 "(`Name` char(255) not null primary key default '', "
                                 "`Value` bigint(255) not null, "
                                 "`Password` bigint(255) null, "
                                 "`Last Modified` date not null)"]

    @staticmethod
    def usemysql(cfgfile=None):
        def inner(cls):
            cls._connection = UserConnection(cfgfile=cfgfile)
            cls.cursor = property(cls._connection.csr)
            cls.run_query = partial(cls._connection.run_query)
            cls.drop = partial(cls._connection.drop)
            cls.show_databases = partial(cls._connection.show_databases)
            cls.use = partial(cls._connection.use)
            cls.show_tables = partial(cls._connection.show_tables)
            cls.describe = partial(cls._connection.describe)
            cls.create_table = partial(cls._connection.create_table)
            cls.select = partial(cls._connection.select)
            cls.tinsert = partial(cls._connection.insert)
            print(f'{cls} runned usemysql()')
            return cls
        return inner

    def run_query(self, query, fetch=None):
        self.csr.execute(query)
        match fetch:
            case None | 'all':
                return self.csr.fetchall()
            case 'one':
                return self.csr.fetchone()
            case 'many':
                raise AttributeError('does not fucking support many')
            case _:
                raise AttributeError(f'unknown value {fetch} for argument fetch')

    def describe(self, table_name):
        return self.run_query(f'desc {table_name}')

    def drop(self, drop_type=None, *, name):
        match drop_type:
            case 'database' | 'db':
                self.run_query(f'drop database {name}')
            case 'table' | None:
                self.run_query(f'drop table {name}')
            case _:
                self.run_query(f'drop table {name}')

    def create_table(self, table_name):
        self.run_query(self.tableDescription[0]+table_name+self.tableDescription[1])

    def insert(self, table_name, *values):
        if not str(values[1]).isdigit():
            return

        self.run_query(
            f"insert into {table_name} values('{values[0]}', {values[1]}, "
            f"{'NULL' if not values[2] else values[2]}, "
            f"{values[3] if len(values) == 4 else 'CURDATE()'})"
        )

    def select(self, *args, table_name):
        match args:
            case ('*', ) | ():
                return self.run_query(f'select * from {table_name}')
            case _:
                query_string = f'select {str(args)} from {table_name}'
                query_string = query_string.replace('(', '').replace(')', '').replace('\'', '').replace('\"', '')
                return self.run_query(query_string)

    def drop_table(self, table_name):
        self.run_query(f'drop table {table_name}')

    def use(self, db: str) -> None:
        self.run_query(f'use {db}')
        return self.show_tables()

    def show_tables(self):
        return self.run_query('show tables')

    def show_databases(self):
        return self.run_query('show databases')
