# -*- encoding: utf-8 -*-
import csv
from tkinter import TclError
from types import NoneType
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
    def __init__(self, cls):
        self.cls = cls
        super().__init__(selectionCombobox := self.cls.selectionCombobox)
        self.master: Combobox = selectionCombobox
        self.isRenameCommandAdded = False
        # build + bind right click menu
        self.build_rightClickMenu()
        self.master.bind('<Button-3>', self.post_event)

        self.cls.window.bind('<Control-n>', self.__create_table)
        self.cls.window.bind('<Control-i>', self.import_from_csv)
        self.cls.window.bind('<Control-m>', self.modifySelectedSlot)
        self.cls.add(button, self.cls.rightSideTopFrame, text='修改当前选中条目', bootstyle=DANGER,
                     command=self.modifySelectedSlot).pack(pady=10, side=RIGHT)

    def modifySelectedSlot(self, event=None):
        table = self.cls.tree
        print(table.get_selected_row())
        return

    def post_event(self, event=None):
        if self.master.get():
            if self.isRenameCommandAdded:
                super().post_event(event)
                return
            self.add_command(label='重命名')
            self.isRenameCommandAdded = True
        else:
            try:
                self.delete('重命名')
                self.isRenameCommandAdded = False
            except TclError:
                pass
        super().post_event(event)

    def build_rightClickMenu(self):
        config = {
            'export_table': {
                'label': MessageCatalog.translate('导出表格为csv'),
                'command': self.cls.tree.export_current_page
            },
            'import_table': {
                'label': MessageCatalog.translate('导入csv'),
                'command': self.import_from_csv
            },
            'create_table': {
                'label': MessageCatalog.translate('创建表格'),
                'command': self.__create_table
            },
            'delete_table': {
                'label': MessageCatalog.translate('删除表格'),
                'command': self.drop_table
            }
        }
        self.add_command(cnf=config['import_table'])
        self.add_command(cnf=config['export_table'])
        self.add_separator()
        self.add_command(cnf=config['create_table'])
        self.add_command(cnf=config['delete_table'])

    @staticmethod
    def __isTitleValid(string: str):
        if not string:
            return None
        return False if (len(string) < 2 or string.isdigit() or not string.isascii()) else True

    def drop_table(self) -> None:
        if not self.master.get():
            Messagebox.show_info(title='提示', message='你没有选择任何表格')
            return
        original = list(self.master.values)
        drop_table_name = self.master.get()

        match Messagebox.yesno(title='delete', message=f'删除{drop_table_name}?', parent=self.cls.window):
            case '确认':
                self.drop(drop_type='table', name=drop_table_name)
                print(f'table \'{drop_table_name}\' is removed from database')

        current = original.remove(drop_table_name)
        self.master.values = current

    def __create_table(self, event=None):
        if isinstance(string := Querybox.get_string(prompt='输入表格名称', title='Title'), NoneType):
            return

        if not self.__isTitleValid(string):
            raise ValueError('请检查表名')

        self.create_table(string)
        print(f'created table \'{string}\'')

    def import_from_csv(self, event=None):
        if not (filename := filedialog.askopenfilename(parent=self.cls.window, title='通过csv导入',
                filetypes=[('CSV', 'csv')])):
            return

        removed_ext = filename.rstrip('.csv').rstrip('.CSV')

        if not self.__isTitleValid(table_name := removed_ext.split('/')[-1]):
            raise ValueError('请检查表名')

        # todo 表格数据不能为空 如果为空则创建一个空表格(无需循环遍历
        with open(filename, newline='', encoding='utf-8') as f:
            csv_lines = csv.reader(f)
            self.create_table(table_name)
            [self.tinsert(table_name, line[0], line[1], line[2]) for line in csv_lines]
