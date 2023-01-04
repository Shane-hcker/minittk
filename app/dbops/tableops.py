# -*- encoding: utf-8 -*-
from nbwindow import NotebookWindow
from minittk import *


@usemysql(r'D:\minittk\app\user\config.ini')
class TableOperations(NotebookWindow):
    def __init__(self):
        super().__init__("Title", "600x500", (True, True))
        self.opsList = ("表格操作", "表格数据")  # Operation Lists
        self.tableops, self.dataops = self.add_pages(self.opsList)
        self.tablecreateName = None
        self.createTableBtn = None
        self.pageGenerate_table().pageCreate_data()

    def __isTitleLegit(self, x):
        if not x:
            self.createTableBtn['state'] = DISABLED
            return False
        x = str(x)
        if x.isdigit():
            self.createTableBtn['state'] = DISABLED
            return False
        self.createTableBtn['state'] = NORMAL
        return True

    def __createTable(self):
        if not (tableTitle := self.tablecreateName.value):
            return
        createFormat = f"create table if not exists {tableTitle} (" \
                       "`Name` char(255) not null primary key default '', " \
                       "`Value` bigint(255) not null, `Password` bigint(255) null, " \
                       "`Last Modified` date not null)"

    def pageGenerate_table(self) -> "TableOperations":
        lFrame = self.add(labelframe, self.tableops, text="创建表格").rpack(fill=BOTH, padx=5, side=TOP)
        add = partial(self.add, parent=lFrame)

        add(label, text="表格名称:").pack(side=LEFT, padx=5, pady=15)
        isTitleLegit = self.window.register(self.__isTitleLegit)
        add(button, text='检查表名', bootstyle=SECONDARY).pack(side=LEFT, padx=5, pady=15)
        self.tablecreateName = add(entry, bootstyle=SUCCESS, validate=FOCUS,
                                   validatecommand=(isTitleLegit, '%P')).rpack(side=LEFT, padx=5, pady=15)
        self.createTableBtn = add(button, text='创建', state=DISABLED, bootstyle=SUCCESS)
        self.createTableBtn.pack(side=LEFT, padx=5, pady=15)
        return self

    def pageCreate_data(self) -> "TableOperations":
        return self


if __name__ == "__main__":
    with TableOperations() as window:
        pass
