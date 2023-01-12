# -*- encoding: utf-8 -*-
from minittk import *


@UserConnection.usemysql(r'D:\minittk\app\user\config.ini')
class DatabaseOperationMenu(Menu):
    pass