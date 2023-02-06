# -*- encoding: utf-8 -*-
from functools import partial
from os.path import isfile
from typing import *

import time
import asyncio
import aiomysql

from minittk.support.cfgparser import MyConfigParser


class AsyncConnection:
    _instance = None
    _init_flag = False
    _awaited = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AsyncConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, cfgfile):
        if self.__class__._init_flag:
            return

        if not isfile(cfgfile):
            raise FileNotFoundError(f'{cfgfile}, such file does not exist')

        self.connection = None
        self.cursor = None
        self.kwargs = MyConfigParser(cfgfile).getSectionItems('MySQL')
        self.tableDescription = ["create table if not exists ",
                                 "(`Name` char(255) not null primary key default '',"
                                 "`Value` bigint(255) not null,`Password` bigint(255) null,"
                                 "`Last Modified` date not null)"]
        self.__class__.__init_flag = True

        if db_value := self.kwargs.get('database'):
            self.kwargs['db'] = db_value
            self.kwargs.pop('database')

    def __await__(self):
        if self.__class__._awaited:
            return self
        connect = asyncio.create_task(self.connect(**self.kwargs))
        yield from connect
        self.__class__._awaited = True
        return self

    async def connect(self, **kwargs):
        self.connection = await aiomysql.connect(**kwargs or self.kwargs, autocommit=True)
        self.cursor = await self.connection.cursor()
        return self

    async def close(self):
        await self.cursor.close()
        self.connection.close()

    @staticmethod
    def clsAwait(self):
        connection = asyncio.create_task(AsyncConnection(self.cfgfile).connect())
        self._connection = yield from connection
        self.cursor = self._connection.cursor
        self.close = self._connection.close

        self.run_query = self._connection.run_query
        self.describe = self._connection.describe
        self.use = self._connection.use
        self.select = self._connection.select
        self.tinsert = self._connection.insert
        self.tupdate = self._connection.update

        self.drop = self._connection.drop
        self.drop_table = self._connection.drop_table
        self.drop_database = self._connection.drop_database

        self.create = self._connection.create
        self.create_table = self._connection.create_table
        self.create_database = self._connection.create_database

        self.show_tables = self._connection.show_tables
        self.show_databases = self._connection.show_databases
        self.show_filtered_databases = self._connection.show_filtered_databases
        return self

    @staticmethod
    def setupMySQL(cfgfile=None):
        def inner(cls):
            cls._connection = None
            cls.cfgfile = cfgfile
            cls.__await__ = AsyncConnection.clsAwait
            return cls
        return inner

    @staticmethod
    async def uselessFunc(delay):
        await asyncio.sleep(delay)
        print(f"uselessFunc {delay} executed")

    async def create(self, ctype, name):
        match ctype:
            case 'table':
                await self.run_query(self.tableDescription[0] + f"`{name}`" + self.tableDescription[1])
            case 'database' | 'db':
                await self.run_query(f'create database `{name}`')
            case _:
                raise AttributeError(f'unresolved creating type {ctype}')

    async def create_database(self, db) -> None:
        await self.create('db', db)

    async def create_table(self, table_name) -> None:
        await self.create('table', table_name)

    async def describe(self, table_name):
        return await self.run_query(f'desc `{table_name}`')

    async def drop(self, drop_type, name):
        match drop_type:
            case 'database' | 'db':
                await self.run_query(f'drop database `{name}`')
            case 'table' | None:
                await self.run_query(f'drop table `{name}`')
            case _:
                raise AttributeError(f'Unknown drop object {drop_type}')

    async def drop_database(self, db) -> None:
        await self.drop('db', db)

    async def drop_table(self, table_name) -> None:
        await self.drop('table', table_name)

    async def insert(self, table_name, *values):
        """
        with Password: table_name, name, value, password
        without Pasword: table_name, name, value, ''
        """
        # may be select
        if len(values) == 1:
            return await self.run_query(f'insert into `{table_name}` {values[0]}')

        name, value, password = values[:3]
        if str(value).isdigit():
            await self.run_query(
                f"insert into `{table_name}` values('{name}', {value}, "
                f"{'NULL' if not password else password}, CURDATE())")

    async def select(self, table_name, *args, condition=''):
        match args:
            case ('*', ) | ():
                return await self.run_query(f'select * from `{table_name}` {condition}')
            case _:
                query_string = f'select {str(args)} from `{table_name}` {condition}'
                query_string = query_string.replace('(', '').replace(')', '').replace('\'', '`')
                return await self.run_query(query_string)

    async def use(self, db: str) -> None:
        await self.run_query(f'use `{db}`')
        return await self.show_tables()

    async def run_query(self, query, fetch=None):
        await self.cursor.execute(query)
        match fetch:
            case 'all' | None:
                return await self.cursor.fetchall()
            case 'one':
                return await self.cursor.fetchone()
            case _:
                raise AttributeError(f'execute has no attribute {fetch}')

    async def update(self, table_name, setvalues: dict, primaryKey: dict) -> None:
        set_string = self.__format_dic_items(setvalues)
        key_string = self.__format_dic_items(primaryKey)
        await self.run_query(f"update `{table_name}` set {set_string} where {key_string}")

    async def show_tables(self):
        return await self.run_query('show tables')

    async def show_databases(self):
        return await self.run_query('show databases')

    async def show_filtered_databases(self, restriction=None) -> list:
        """returns a list of filtered"""
        if restriction:
            return [db for (db,) in await self.show_databases() if db not in restriction]
        return [db[0] for (db,) in await self.show_databases()]

    @staticmethod
    def __format_dic_items(string: dict):
        pending = ""
        for k, v in string.items():
            if not v.isdigit() and v not in ['NULL', 'null']:
                pending += f"`{k}`='{v}',"
                continue
            pending += f"`{k}`={v},"
        return pending.rstrip(',')


@AsyncConnection.setupMySQL('../../app/user/config.ini')
class DemoClass:
    # fixme add a "setConnectionAttribute" method to AConnection and complete the aenter/aexit method
    async def __aenter__(self):
        await self.__await__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._connection.close()


async def main():
    tasks = asyncio.gather(AsyncConnection.uselessFunc(1), AsyncConnection.uselessFunc(2))
    # conn_task = asyncio.create_task(AsyncConnection('../../app/user/config.ini').connect())
    t1 = time.perf_counter()
    async with DemoClass() as connection:
        pass

    await tasks
    # connection = await conn_task
    # print(await connection.run_query('show databases'))
    await connection.close()
    print(time.perf_counter() - t1)
    # print(connection)
    # await connection.close()  # 关闭连接

if __name__ == '__main__':
    asyncio.run(main())
