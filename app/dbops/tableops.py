# -*- encoding: utf-8 -*-
from nbwindow import NotebookWindow
from minittk import *
import csv


@UserConnection.usemysql(r'D:\minittk\app\user\config.ini')
@MyConfigParser.useconfig()
class TableOperations(NotebookWindow):
    def __init__(self):
        self.cfgParser.loadfromFile(r'D:\minittk\app\user\config.ini')
        super().__init__(f"当前数据库: {self.cfgParser.get('MySQL', 'database').title()}", "600x500", (True, True))
        self.tableops, self.dataops = self.add_pages(("表格操作", "表格数据"))
        self.tablecreateName = None
        self.createTableBtn = None
        self.__default_header = ['Name', 'Value', 'Password']
        self.pageCreate_table().pageCreate_data()

    def open(*args, **kwargs):
        return partial(open, newline='')(*args, **kwargs)

    def __import_from_csv(self):
        filename = filedialog.askopenfilename(filetypes=[('CSV', 'csv')], parent=self.window, title='通过csv导入')

        if ((tableName := filename.rstrip('.csv').rstrip('.CSV').split('/')[-1]).isdigit() or
           not tableName.isascii()):
            raise ValueError('tableName 仅支持字母/数字+字母+字符')
        # todo 表格数据不能为空

        with self.open(filename, encoding='utf-8') as f:
            csv_lines = csv.DictReader(f, self.__default_header)
            self.create_table(tableName)
            for line in csv_lines:
                self._connection.insert(tableName, line['Name'], line['Value'], line['Password'])

    def __export_as_csv(self):
        filename = filedialog.asksaveasfilename(initialfile='Untitled.csv', defaultextension='.csv',
                                                filetypes=[('CSV', 'csv')], parent=self.window, title='导出为csv')
        # with self.open(filename, 'w', encoding='utf-8') as f:
        #     dictWriter = csv.DictWriter(f, self.__default_header)
        #     dictWriter.writeheader()
        # todo userconnection select() *args改成可以放到sql_dialect里面的
        data_list = [{'Name': name.title(), 'Value': value, 'Password': password}
                     for name, value, password, _ in self._connection.select(table_name='tencenttable1')]
        print(data_list)
        # dictWriter.writerows(data_list)

    def create_table(self, table_name):
        self._connection.create_table(table_name)

    def __createTable(self):
        if not (tableTitle := self.tablecreateName.value):
            return
        self.create_table('haha')
        print(f'created table \'{tableTitle}\'')

    def __isTitleLegit(self, x):
        if not x:
            self.createTableBtn['state'] = DISABLED
            return False
        if x.isdigit():
            self.createTableBtn['state'] = DISABLED
            return False

        self.createTableBtn['state'] = NORMAL
        return True

    def pageCreate_table(self) -> "TableOperations":
        # todo 完成表格操作
        lFrame = self.add(labelframe, self.tableops, text="创建表格", padding=10).rpack(fill=BOTH, padx=5, side=TOP)
        add = partial(self.add, parent=lFrame)

        add(label, text="表格名称:").pack(side=LEFT, padx=5,)
        isTitleLegit = self.window.register(self.__isTitleLegit)
        add(button, text='检查表名', bootstyle=SECONDARY).pack(side=LEFT, padx=5)
        self.tablecreateName = add(entry, bootstyle=SUCCESS, validate=FOCUS,
                                   validatecommand=(isTitleLegit, '%P')).rpack(side=LEFT, padx=5)
        self.tablecreateName.focus_set()
        self.createTableBtn = add(button, state=DISABLED, bootstyle=SUCCESS, command=self.__createTable,
                                  text='创建').rpack(side=LEFT, padx=5)
        add(button, text='导入', command=self.__import_from_csv).pack(side=RIGHT, padx=5)
        add(button, text='导出', command=self.__export_as_csv).pack(side=RIGHT)
        return self

    def pageCreate_data(self) -> "TableOperations":
        return self


if __name__ == "__main__":
    window = TableOperations()
    window()
