# -*- encoding: utf-8 -*-
from minittk import *


@UserConnection.usemysql(r'D:\minittk\app\user\config.ini')
class DatabaseOperationMenu(Menu):
    """
    Features:
     - 创建数据库
     - 删除数据库
     - 重命名
    """

    def __init__(self, cls):
        self.cls = cls
        self.master: Combobox = self.cls.databaseCombobox
        super().__init__(self.master)
        self.master.bind('<Button-3>', self.post_event)
        self.build()

    def build(self):
        config = {
            '': {
                'label': None,
                'command': None,
            }
        }

    def post_event(self, event):
        super().post_event(event)
    