# -*- encoding: utf-8 -*-
import asyncio
import aiomysql

from minittk.support.cfgparser import MyConfigParser


class SQLHandler:
    """
    Handler => 处理器
    receives sql from queue and process them
    then drop the result if it's a query to the
    result queue
    """

    def __init__(self, send, recv, cfg, section='MySQL'):
        self.connection = self.cursor = None
        self.sender, self.receiver = send, recv
        self.__connected = False

        if isinstance(cfg, dict):
            self.kwargs = cfg
            return

        self.kwargs = MyConfigParser(cfg).getSectionItems(section)
        if db_value := self.kwargs.get('database'):
            self.kwargs['db'] = db_value
            self.kwargs.pop('database')

    def __await__(self):
        yield from asyncio.create_task(self.run_forever())
        return self

    async def __aenter__(self):
        return await self.run_forever()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()
        self.connection.close()

    async def run_forever(self, **kwargs):
        """Mainloop"""
        self.connection = await aiomysql.connect(**(self.kwargs or kwargs), autocommit=True)
        self.cursor = await self.connection.cursor()
        self.__connected = True
        await self.__run()
        await self.cursor.close()
        self.connection.close()

    async def modify(self, sql):
        await self.cursor.execute(sql)

    async def fetch(self, sql):
        return await self.cursor.execute(sql)

    async def __run(self):
        if not self.__connected:
            raise ConnectionAbortedError("MySQL database is not connected")
        while claimFromQueue := await self.sender.get():
            sql, mode = claimFromQueue
            if mode == 'terminate':
                print('SQLHandler ended!')
                break
            elif mode == 'modify':
                await self.modify(sql)
                print(f'executed CRUD SQL: {sql}')
            elif mode == 'query':
                result = await self.fetch(sql)
                self.receiver.put_nowait({hash(sql): result})
