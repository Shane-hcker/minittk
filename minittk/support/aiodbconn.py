# -*- encoding: utf-8 -*-
from typing import *
import time
import asyncio
import aiomysql
from minittk.support.cfgparser import MyConfigParser


class AsyncConnection:
    _instance = None
    __init_flag = False
    __awaited = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AsyncConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, cfgfile):
        if self.__class__.__init_flag:
            return
        self.connection = None
        self.cursor = None
        self.kwargs = MyConfigParser(cfgfile).getSectionItems('MySQL')
        self.kwargs['db'] = self.kwargs.get('database')
        self.kwargs.pop('database')
        self.__class__.__init_flag = True

    def __await__(self):
        # instance check -> singleton
        if self.__class__.__awaited:
            return self
        connect = asyncio.create_task(self.connect(**self.kwargs))
        yield from connect
        self.__class__.__awaited = True
        return self

    @staticmethod
    def setupMySQL(cls):
        cls._connection = None
        cls.cursor = None
        return cls

    async def connect(self, **kwargs):
        self.connection = await aiomysql.connect(**kwargs or self.kwargs, autocommit=True)
        self.cursor = await self.connection.cursor()
        return self

    async def run_query(self, query, fetch=None):
        await self.cursor.execute(query)
        match fetch:
            case 'all' | None:
                return await self.cursor.fetchall()
            case 'one':
                return await self.cursor.fetchone()
            case _:
                raise AttributeError(f'execute has no attribute {fetch}')

    async def close(self):
        await self.cursor.close()
        self.connection.close()

    @staticmethod
    async def uselessFunc(delay):
        await asyncio.sleep(delay)
        print(f"uselessFunc {delay} executed")


async def main():
    tasks = asyncio.gather(AsyncConnection.uselessFunc(1), AsyncConnection.uselessFunc(2))
    conn_task = asyncio.create_task(AsyncConnection('./app/user/config.ini').connect())

    t1 = time.perf_counter()

    await tasks
    connection = await conn_task
    print(await connection.run_query('show databases'))

    print(time.perf_counter() - t1)
    print(connection)
    await connection.close()  # 关闭连接

if __name__ == '__main__':
    asyncio.run(main())

