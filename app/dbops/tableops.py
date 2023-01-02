# -*- encoding: utf-8 -*-
from nbwindow import NotebookWindow
from minittk import *


class TableOperations(NotebookWindow):
    def __init__(self):
        super().__init__('Title', '600x500', (True, True), theme='cosmo')
        self.opsList = ('表格操作', '表格数据')  # Operation Lists
        self.tableops, self.tabdata = self.add_pages(self.opsList)
        self.pageGenerate_table().pageCreate_data()

    def pageGenerate_table(self) -> "TableOperations":
        return self

    def pageCreate_data(self) -> "TableOperations":
        return self


if __name__ == '__main__':
    with TableOperations() as window:
        pass
