# -*- encoding: utf-8 -*-
from minittk import *


@MyConfigParser.setupConfig(config_file)
@UserConnection.usemysql(config_file)
class DatabaseOperationMenu(Menu):
    """
    Features:
     - 创建数据库 x
     - 删除数据库 x
    """

    def __init__(self, cls):
        self.cls = cls
        self.master: Combobox = self.cls.databaseCombobox
        super().__init__(self.master)
        self.master.bind('<Button-3>', self.post_event)
        self.cls.window.bind('<Control-Shift-N>', self.create_db)
        self.build()

    def build(self):
        config = {
            'create_db': {
                'label': MessageCatalog.translate('创建数据库'),
                'command': self.create_db
            },
            'delete_db': {
                'label': MessageCatalog.translate('删除数据库'),
                'command': self.delete_db
            }
        }
        self.add_command(cnf=config.get('create_db'))
        self.add_command(cnf=config.get('delete_db'))

    def create_db(self, event=None):
        string_prompt = '-不能为纯数字\n  -不能包含字符" ` "'
        if not (db_name := Querybox.get_string(string_prompt, 'title')):
            return

        if not self.isTitleValid(db_name):
            raise ValueError('请检查数据库名称')

        self.create_database(db_name)
        self.master.add(db_name)
        self.master.set(db_name)
        print(f'created database {db_name}')

    def delete_db(self):
        if not self.master.get():
            return Messagebox.show_info(title='提示', message='你没有选择任何数据库')

        dropping_target = self.master.get()

        if Messagebox.yesno(f'删除{dropping_target}?', 'delete', parent=self.cls.window) == '确认':
            self.master.remove(dropping_target)
            self.drop(drop_type='db', name=dropping_target)
            print(f'database \'{dropping_target}\' is removed')
