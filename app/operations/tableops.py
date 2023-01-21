# -*- encoding: utf-8 -*-
import csv
from tkinter import TclError
from types import NoneType
from minittk import *


@UserConnection.usemysql(r'D:\minittk\app\user\config.ini')
class TableOperationMenu(Menu):
    """
    - 表格操作
      - 创建 x
        - 导入 x
        - 命名空表格 x
      - 删除 x
      - 创建副本表格(new name) x
      - 重命名 x
    """

    def __init__(self, cls):
        self.cls = cls
        self.master: Combobox = self.cls.selectionCombobox
        super().__init__(self.master)
        self.tableview: Tableview = self.cls.tree
        self.selected_row: TableRow = ...
        self.isRenameCommandAdded = False

        self.build()
        self.master.bind('<Button-3>', self.post_event)
        self.cls.window.bind('<Control-n>', self.__create_table)
        self.cls.window.bind('<Control-i>', self.import_from_csv)

        for key in ['<Double-1>', '<Return>']:
            self.tableview.view.bind(key, self.fill_modification_entries)

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

    def build(self):
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
            },
            'create_copy': {
                'label': MessageCatalog.translate('创建表格副本'),
                'command': self.create_copy
            }
        }
        self.add_command(cnf=config.get('import_table'))
        self.add_command(cnf=config.get('export_table'))
        self.add_separator()
        self.add_command(cnf=config.get('create_table'))
        self.add_command(cnf=config.get('delete_table'))
        self.add_separator()
        self.add_command(cnf=config.get('create_copy'))

    def post_event(self, event=None):
        if self.master.get():
            if self.isRenameCommandAdded:
                super().post_event(event)
                return
            self.add_command(label='重命名', command=self.rename_table)
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
            return

        print(f'selected tablerow iid: {selected_iid}')
        self.selected_row = self.tableview.get_row(iid=selected_iid)
        row_items = {
            'name': self.selected_row.values[0],
            'value': self.selected_row.values[1],
            'password': '' if not self.selected_row.values[2] else self.selected_row.values[2]
        }
        print(f'tablerow {selected_iid}\'s row items: {row_items}')
        self.saveSlotBtn.set_state(NORMAL)
        [self.entry_dict[key].reset(row_items[key]) for key in self.entry_dict.keys()]

    def update_slot_changes(self) -> None:
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
        self.tupdate(self.cls.current_table, pending_update, update_condition)
        print('finished updating tablerow and db')

    def save_as_csv(self, event=None) -> None:
        if not self.tableview.tablerows:
            return Messagebox.show_error(title='', message='no table is selected')
        self.tableview.export_all_records()

    def import_from_csv(self, event=None) -> None:
        if not (filename := filedialog.askopenfilename(parent=self.cls.window, filetypes=[('CSV', 'csv')],
                                                       title='通过csv导入')):
            return

        removed_extension = filename.rstrip('.csv').rstrip('.CSV')

        if not self.__isTitleValid(table_name := removed_extension.split('/')[-1]):
            raise ValueError('请检查表名')

        with open(filename, newline='', encoding='utf-8') as f:
            self.create_table(table_name)
            [self.tinsert(table_name, line[0], line[1], line[2]) for line in csv.reader(f)]
            self.master.add(table_name)

    def create_copy(self):
        copied_target = self.master.get()
        copy_name = Querybox.get_string(f'{copied_target}副本名称', f'为{copied_target}创建副本')

        if not self.__isTitleValid(copy_name):
            raise ValueError('请检查表名')

        self.create_table(copy_name)
        self.tinsert(copy_name, f'select * from {copied_target}')
        self.master.add(copy_name)
        self.master.clear()
        print('successfully copied table')

    def __create_table(self, event=None) -> None:
        if isinstance(string := Querybox.get_string(prompt='输入表格名称', title='Title'), NoneType):
            return

        if not self.__isTitleValid(string):
            raise ValueError('请检查表名')

        self.create_table(string)
        print(f'created table \'{string}\'')
        self.master.add(string)

    def delete_table(self) -> None:
        if not self.master.get():
            Messagebox.show_info(title='提示', message='你没有选择任何表格')
            return

        dropping_target = self.master.get()

        if Messagebox.yesno(title='delete', message=f'删除{dropping_target}?', parent=self.cls.window) == '确认':
            self.master.remove(dropping_target)
            self.drop(drop_type='table', name=dropping_target)
            print(f'table \'{dropping_target}\' is removed from database')

    def rename_table(self) -> None:
        if isinstance(new_name := Querybox.get_string(prompt='重命名表格', title='Title'), NoneType):
            return

        if not self.__isTitleValid(new_name):
            raise ValueError('请检查表名')

        self.run_query(f'rename table {self.cls.current_table} to {new_name}')
        self.master.reset(self.cls.current_table, new_name)
        print(f'renamed table \'{self.cls.current_table}\' to \'{new_name}\' successfully')

        self.master.clear()
        if self.tableview.get_rows():
            self.tableview.delete_rows()

    @staticmethod
    def __isTitleValid(string: str) -> bool:
        if not string:
            return False
        return False if (len(string) < 2 or string.isdigit() or not string.isascii()) else True
