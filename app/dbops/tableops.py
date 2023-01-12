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
    def __init__(self, cls):
        self.cls = cls
        selectionCombobox: Combobox = self.cls.selectionCombobox
        super().__init__(selectionCombobox)
        self.master: Combobox = selectionCombobox
        # build + bind right click menu
        self.build_rightClickMenu()
        self.master.bind('<Button-3>', self.post_event)
        # fixme missing positional argument 'event'
        self.cls.window.bind('<Control-n>', lambda self, event: self.__create_table())

    # building right click menu
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
        if not string or string.isdigit() or not string.isascii():
            raise ValueError('表名仅支持: ASCII字母(+数字)(+符号)')

    # All commands below
    def import_from_csv(self):
        filename = filedialog.askopenfilename(filetypes=[('CSV', 'csv')], parent=self.window, title='通过csv导入')
        removedext = filename.rstrip('.csv').rstrip('.CSV')
        self.__isTitleValid(tableName := removedext.split('/')[-1])

        # todo 表格数据不能为空
        with open(filename, newline='', encoding='utf-8') as f:
            csv_lines = csv.reader(f)
            self.create_table(tableName)
            for line in csv_lines:
                self.tinsert(tableName, line[0], line[1], line[2])

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

    def __create_table(self):
        self.__isTitleValid(string := Querybox.get_string(prompt='输入表格名称', title='Title'))
        self.create_table(string)
        print(f'created table \'{string}\'')
