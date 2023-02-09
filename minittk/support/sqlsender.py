# -*- encoding: utf-8 -*-
from typing import *
import asyncio


class SQLSender:
    """
    SQL types:
     - Q(query)
     - M(modify)
    """

    def __init__(self, queue):
        self.queue = queue

    def send(self, sql: Tuple[str, str]) -> None | int:
        if not isinstance(self.queue, asyncio.Queue):
            raise ValueError('please set AsyncConnection.queue correctly')
        try:
            self.queue.put_nowait(sql)
        except Exception as e:
            print(e)
            return

        # return the hash of the sql if sql is a query
        sql, mode = sql
        if mode == 'query':
            return hash(sql)

    def create(self, ctype, name):
        match ctype:
            case 'table':
                self.send((
                    f"create table if not exists `{name}`(`Name` char(255) not null primary key default '',"
                    "`Value` bigint(255) not null,`Password` bigint(255) null,"
                    "`Last Modified` date not null)", 'modify'))
            case 'database' | 'db':
                self.send((f'create database `{name}`', 'modify'))
            case _:
                raise AttributeError(f'unresolved creating type {ctype}')

    def create_database(self, db):
        self.create('db', db)

    def create_table(self, table_name):
        self.create('table', table_name)

    def describe(self, table_name):
        self.send((f'desc `{table_name}`', 'query'))

    def drop(self, drop_type, name):
        match drop_type:
            case 'database' | 'db':
                self.send((f'drop database `{name}`', 'modify'))
            case 'table' | None:
                self.send((f'drop table `{name}`', 'modify'))
            case _:
                raise AttributeError(f'Unknown drop object {drop_type}')

    def drop_database(self, db) -> None:
        self.drop('db', db)

    def drop_table(self, table_name) -> None:
        self.drop('table', table_name)

    def insert(self, table_name, *values):
        """
        with Password: table_name, name, value, password
        without Pasword: table_name, name, value, ''
        """
        # may be select
        if len(values) == 1:
            return self.send((f'insert into `{table_name}` {values[0]}', 'modify'))

        name, value, password = values[:3]
        if str(value).isdigit():
            self.send(
                (f"insert into `{table_name}` values('{name}', {value}, "
                 f"{'NULL' if not password else password}, CURDATE())", 'modify'))

    def select(self, table_name, *args, condition=''):
        match args:
            case ('*', ) | ():
                self.send((f'select * from `{table_name}` {condition}', 'query'))
            case _:
                query_string = f'select {str(args)} from `{table_name}` {condition}'
                query_string = query_string.replace('(', '').replace(')', '').replace('\'', '`')
                self.send((query_string, 'query'))

    def use(self, db: str):
        self.send((f'use `{db}`', 'modify'))
        return self.show_tables()

    def update(self, table_name, setvalues: dict, primaryKey: dict) -> None:
        set_string = self.__format_dic_items(setvalues)
        key_string = self.__format_dic_items(primaryKey)
        self.send((f"update `{table_name}` set {set_string} where {key_string}", 'modify'))

    def show_tables(self):
        return self.send(('show tables', 'query'))

    def show_databases(self):
        return self.send(('show databases', 'query'))

    def assignAttributesTo(self, obj):
        obj.send = self.send
        obj.describe = self.describe
        obj.use = self.use
        obj.select = self.select
        obj.tinsert = self.insert
        obj.tupdate = self.update

        obj.drop = self.drop
        obj.drop_table = self.drop_table
        obj.drop_database = self.drop_database

        obj.create = self.create
        obj.create_table = self.create_table
        obj.create_database = self.create_database

        obj.show_tables = self.show_tables
        obj.show_databases = self.show_databases
        return obj

    @staticmethod
    def __format_dic_items(string: dict):
        pending = ""
        for k, v in string.items():
            if not v.isdigit() and v not in ['NULL', 'null']:
                pending += f"`{k}`='{v}',"
                continue
            pending += f"`{k}`={v},"
        return pending.rstrip(',')
