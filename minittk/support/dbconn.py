# -*- encoding: utf-8 -*-
from functools import partial
from os.path import isfile

import pymysql

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

        if not isfile(cfgfile):
            raise FileNotFoundError(f'{cfgfile}, no such file')

        print('going through UserConnection.__init__()')
        self.__class__._init_flag = True
        super().__init__(**MyConfigParser(cfgfile).getSectionItems('MySQL'), autocommit=True)
        self.csr = self.cursor()
        self.tableDescription = [
            "create table if not exists ",
            "(`Name` char(255) not null primary key default '',"
            "`Value` bigint(255) not null,"
            "`Password` bigint(255) null,"
            "`Last Modified` date not null)"
        ]

    def create(self, ctype, name):
        match ctype:
            case 'table':
                self.run_query(self.tableDescription[0]+f"`{name}`"+self.tableDescription[1])
            case 'database' | 'db':
                self.run_query(f'create database `{name}`')
            case _:
                raise AttributeError(f'unresolved creating type {ctype}')

    def create_database(self, db) -> None: self.create('db', db)

    def create_table(self, table_name) -> None: self.create('table', table_name)

    def describe(self, table_name): return self.run_query(f'desc `{table_name}`')

    def drop(self, drop_type, name):
        match drop_type:
            case 'database' | 'db':
                self.run_query(f'drop database `{name}`')
            case 'table' | None:
                self.run_query(f'drop table `{name}`')
            case _:
                raise AttributeError(f'Unknown drop object {drop_type}')

    def drop_database(self, db) -> None: self.drop('db', db)

    def drop_table(self, table_name) -> None: self.drop('table', table_name)

    def insert(self, table_name, *values):
        """
        with Password: table_name, name, value, password
        without Pasword: table_name, name, value, ''
        """
        # may be select
        if len(values) == 1:
            return self.run_query(f'insert into `{table_name}` {values[0]}')

        name, value, password = values[:3]
        if str(value).isdigit():
            self.run_query(
                f"insert into `{table_name}` values('{name}', {value}, "
                f"{'NULL' if not password else password}, CURDATE())")

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

    def select(self, table_name, *args, condition=None):
        match args:
            case ('*', ) | ():
                return self.run_query(f'select * from `{table_name}` {condition}')
            case _:
                query_string = f'select {str(args)} from `{table_name}` {condition}'
                query_string = query_string.replace('(', '').replace(')', '').replace('\'', '`')
                return self.run_query(query_string)

    def use(self, db: str) -> None:
        self.run_query(f'use `{db}`')
        return self.show_tables()

    @staticmethod
    def usemysql(cfgfile=None):
        def inner(cls):
            cls.connection = UserConnection(cfgfile=cfgfile)
            cls.tupdate = cls.connection.update
            cls.show_filtered_databases = cls.connection.show_filtered_databases
            cls.cursor = cls.connection.csr
            cls.run_query = cls.connection.run_query
            cls.drop = cls.connection.drop
            cls.show_databases = cls.connection.show_databases
            cls.use = cls.connection.use
            cls.show_tables = cls.connection.show_tables
            cls.describe = cls.connection.describe
            cls.create_table = cls.connection.create_table
            cls.create_database = cls.connection.create_database
            cls.select = cls.connection.select
            cls.tinsert = cls.connection.insert
            print(f'{cls} runned usemysql()')
            return cls
        return inner

    def update(self, table_name, setvalues: dict, primaryKey: dict) -> None:
        set_string = self.__format_kv_items(setvalues)
        key_string = self.__format_kv_items(primaryKey)
        self.run_query(f"update `{table_name}` set {set_string} where {key_string}")

    def show_tables(self): return self.run_query('show tables')

    def show_databases(self): return self.run_query('show databases')

    def show_filtered_databases(self, restriction=None) -> list:
        """returns a list of filtered"""
        if restriction:
            return [db for (db, ) in self.show_databases() if db not in restriction]
        return [db[0] for (db, ) in self.show_databases()]

    @staticmethod
    def __format_kv_items(string: dict):
        thestring = ""
        for key, value in string.items():
            if (value.isalpha() or value.isalnum()) and value not in ('NULL', 'null'):
                thestring += f"`{key}`='{value}',"
                continue
            thestring += f"`{key}`={value},"
        return thestring.strip(',')
