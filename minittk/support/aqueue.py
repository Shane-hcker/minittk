# -*- encoding: utf-8 -*-
from typing import *
import asyncio


class AioQueue(asyncio.Queue):
    def get_default(self):
        try:
            return self.get_nowait()
        except asyncio.QueueEmpty as e:
            print('queue empty, return nothing')
