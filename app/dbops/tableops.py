# -*- encoding: utf-8 -*-
import csv
from minittk import *


@UserConnection.usemysql(r'D:\minittk\app\user\config.ini')
class TableOperationMenu(Menu):
    """
    todo 实现tableoperations相关功能, 并集成到mainpg
    - 表格操作
      - 创建
        - 导入
        - 命名空表格
      - 删除
      - 创建副本表格(new name)
      - 重命名
    """
    def __init__(self, master):
        super().__init__(master)
        self.build_rightClickMenu()
        self.master.bind('<Button-3>', self.post_event)

    # building right click menu
    def build_rightClickMenu(self):
        config = {
            'export_table': {
                'label': MessageCatalog.translate('导出表格为csv'),
                'command': None
            },
            'import_table': {
                'label': MessageCatalog.translate('导入csv'),
                'command': self.import_from_csv
            },
            'create_table': {
                'label': MessageCatalog.translate('创建表格'),
                'command': self.create_table
            },
            'delete_table': {
                'label': MessageCatalog.translate('删除表格'),
                'command': self.drop_table
            }
        }
        self.add_command(cnf=config['import_table'])
        self.add_command(cnf=config['export_table'])
        self.add_separator()
        self.add_command(cnf=config['delete_table'])
        self.add_command(cnf=config['create_table'])

    # All commands below
    def import_from_csv(self):
        filename = filedialog.askopenfilename(filetypes=[('CSV', 'csv')], parent=self.window, title='通过csv导入')

        if ((tableName := filename.rstrip('.csv').rstrip('.CSV').split('/')[-1]).isdigit() or
           not tableName.isascii()):
            raise ValueError('tableName 仅支持字母/数字+字母+字符')

        # todo 表格数据不能为空
        with open(filename, newline='', encoding='utf-8') as f:
            csv_lines = csv.reader(f)
            self.create_table(tableName)
            for line in csv_lines:
                self.tinsert(tableName, line[0], line[1], line[2])

    def drop_table(self) -> None:
        table_name = self.master.get()
        yesno = Messagebox.yesno(title='delete', message='delete?', parent=self.master)
        print(MessageCatalog.translate(yesno))
        self.drop(drop_type='table', name=table_name)

    def create_table(self, table_name):
        # if not (tableTitle := self.tablecreateName.value):
        #     self.tablecreateName.configure(bootstyle=DANGER)
        #     self.createTableBtn.set_state('disabled')
        #     return
        # self.create_table(tableTitle)
        # print(f'created table \'{tableTitle}\'')
        pass

    def isTitleLegit(self):
        # if not (get_name_entry := self.tablecreateName.value):
        #     self.createTableBtn.set_state('disabled')
        #     self.tablecreateName.configure(bootstyle=DANGER)
        #     return
        #
        # if get_name_entry.isdigit():
        #     self.createTableBtn.set_state('disabled')
        #     self.tablecreateName.configure(bootstyle=DANGER)
        #     return
        #
        # self.createTableBtn.set_state('normal')
        # self.tablecreateName.configure(bootstyle=PRIMARY)
        pass
