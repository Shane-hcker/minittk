# -*- encoding: utf-8 -*-
import csv
from tkinter import TclError
from types import NoneType
from minittk import *


@UserConnection.usemysql(r'D:\minittk\app\user\config.ini')
class TableOperationMenu(Menu):
    """
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
        self.tableview: Tableview = self.cls.tree
        self.selected_row: TableRow = ...
        self.isRenameCommandAdded = False
        super().__init__(selectionCombobox := self.cls.selectionCombobox)
        self.master: Combobox = selectionCombobox

        # build + bind right click menu
        self.build_rightClickMenu()
        self.master.bind('<Button-3>', self.post_event)

        self.cls.window.bind('<Control-n>', self.__create_table)
        self.cls.window.bind('<Control-i>', self.import_from_csv)
        # todo 选择tableview可以即时刷新修改条目输入框
        self.cls.window.bind('<Control-m>', self.fill_modification_entries)

        self.saveSlotBtn: Button = self.cls.add(button, self.cls.rightSideFrame, command=self.update_slot_changes,
                                                state=DISABLED, text='保存修改').rpack(padx=10, pady=10, side=RIGHT)

        self.password_entry: Entry = self.cls.add(entry, self.cls.rightSideFrame, bootstyle=WARNING,
                                                  width=10).rpack(pady=10, side=RIGHT)
        self.value_entry: Entry = self.cls.add(entry, self.cls.rightSideFrame, bootstyle=INFO,
                                               width=15).rpack(padx=10, pady=10, side=RIGHT)
        self.name_entry: Entry = self.cls.add(entry, self.cls.rightSideFrame, bootstyle=SUCCESS,
                                              width=15).rpack(pady=10, side=RIGHT)
        self.header = ['Name', 'Value', 'Password']
        self.entry_dict = {
            'name': self.name_entry,
            'value': self.value_entry,
            'password': self.password_entry
        }

    def build_rightClickMenu(self):
        config = {
            'export_table': {
                'label': MessageCatalog.translate('导出表格为csv'),
                'command': self.save_as_csv
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
                'command': self.delete_table
            }
        }
        self.add_command(cnf=config['import_table'])
        self.add_command(cnf=config['export_table'])
        self.add_separator()
        self.add_command(cnf=config['create_table'])
        self.add_command(cnf=config['delete_table'])

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

    def fill_modification_entries(self, event=None) -> None:
        if not (selected_iid := self.tableview.get_selected_row_iid()):
            return Messagebox.show_error(title='', message='no tablerow is selected')

        print(f'selected tablerow iid: {selected_iid}')
        self.selected_row = self.tableview.get_row(iid=selected_iid)
        row_items = {
            'name': self.selected_row.values[0],
            'value': self.selected_row.values[1],
            'password': '' if not self.selected_row.values[2] else self.selected_row.values[2]
        }
        print(f'tablerow {selected_iid}\'s row items: {row_items}')
        for key in self.entry_dict.keys():
            self.entry_dict[key].delete(0, END)
            self.entry_dict[key].insert(END, row_items[key])
        self.saveSlotBtn.set_state(NORMAL)

    def update_slot_changes(self):
        if not (self.name_entry.get() and self.value_entry.get().isdigit()):
            return ToastNotification('Warning', 'check your fillings', duration=3000).show_toast()

        pending_update = {"Last Modified": "CURDATE()"}
        update_condition = {"Name": self.selected_row.values[0]}

        for ndx, entry_item in enumerate(self.entry_dict.values()):
            value = entry_item.get()
            self.selected_row.values[ndx] = None if ndx == 2 and not value else value

            pending_update.update(
                {self.header[ndx]: self.selected_row.values[ndx] if self.selected_row.values[ndx] else 'null'}
            )

        self.selected_row.refresh()
        # fixme invalid int value 'null' for column password
        self.tupdate(self.cls.current_table, pending_update, update_condition)
        print('finished updating tablerow and db')

    def save_as_csv(self, event=None) -> None:
        if not self.tableview.tablerows:
            return Messagebox.show_error(title='', message='no table is selected')
        self.tableview.export_all_records()

    def import_from_csv(self, event=None):
        if not (filename := filedialog.askopenfilename(parent=self.cls.window, title='通过csv导入',
                filetypes=[('CSV', 'csv')])):
            return

        removed_extension = filename.rstrip('.csv').rstrip('.CSV')

        if not self.__isTitleValid(table_name := removed_extension.split('/')[-1]):
            raise ValueError('请检查表名')

        with open(filename, newline='', encoding='utf-8') as f:
            self.create_table(table_name)
            [self.tinsert(table_name, line[0], line[1], line[2]) for line in csv.reader(f)]

    def __create_table(self, event=None):
        if isinstance(string := Querybox.get_string(prompt='输入表格名称', title='Title'), NoneType):
            return

        if not self.__isTitleValid(string):
            raise ValueError('请检查表名')

        self.create_table(string)
        print(f'created table \'{string}\'')

    def delete_table(self) -> None:
        if not self.master.get():
            Messagebox.show_info(title='提示', message='你没有选择任何表格')
            return

        original = list(self.master.values)
        drop_table_name = self.master.get()

        match Messagebox.yesno(title='delete', message=f'删除{drop_table_name}?', parent=self.cls.window):
            case '确认':
                self.drop(drop_type='table', name=drop_table_name)
                print(f'table \'{drop_table_name}\' is removed from database')

        self.master.values = original.remove(drop_table_name)

    @staticmethod
    def __isTitleValid(string: str):
        if not string:
            return None
        return False if (len(string) < 2 or string.isdigit() or not string.isascii()) else True
