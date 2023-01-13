# -*- encoding: utf-8 -*-
from minittk import *
from operations.tableops import TableOperationMenu
from user.setting import SettingPage


# D:\minittk\app\user\config.ini
@UserConnection.usemysql()
@MyConfigParser.useconfig()
class MainPage(MyWindow):
    def __init__(self):
        print(f'__init__(): {self}, id: {id(self)}')
        self.curr_theme = self.cfgParser.get('App', 'theme')
        super().__init__('Title', '1200x700', (True, True), (self.cfgParser.getint('App', 'startup.x'),
                         self.cfgParser.getint('App', 'startup.y')), self.curr_theme)

        self.isTableLengthOutOfRange: bool = False
        self.current_database = None
        self.databaseCombobox = None
        self.selectionCombobox = None
        self.themeCombobox = None

        self.panedwin = self.add(panedwindow, orient=HORIZONTAL, bootstyle='default').rpack(fill=BOTH, expand=True)
        self.rightSideFrame = self.add(frame)  # r < 右侧的 Panedwindow

        self.rightSideTopFrame = self.add(frame, parent=self.rightSideFrame, height=5).rpack(fill=X)
        tree_column = [
            {'text': 'Name', 'stretch': True},
            {'text': 'Value', 'stretch': True},
            {'text': 'Password', 'stretch': True},
            {'text': 'Last Modified', 'stretch': True}
        ]
        self.tree = self.add_tabview(parent=self.rightSideFrame, coldata=tree_column, paginated=True,
                                     searchable=True, pagesize=20).rpack(fill=BOTH, expand=True)
        # TODO database rcm(右键菜单)
        self.window.bind('<Control-Shift-N>', lambda event: print('created 2 files'))

    def __call__(self, *args, **kwargs):
        self.mainloop()
        self._connection.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        TableOperationMenu(self)
        self.mainloop()
        self._connection.close()
        if exc_type:
            raise exc_type()

    @property
    def selectedOptionContent(self) -> Tuple[Any, Any]:
        # focus() & selection()
        value = self.tree.get_selected_row()
        return None if not value else (value['1'], value['2'])  # set()获取当前row的值

    def __databaseComboboxSelected(self, event):
        get_selected = self.databaseCombobox.get()
        self.selectionCombobox.values = [table[0] for table in self.use(get_selected)]
        self.selectionCombobox.clear()

        self.current_database.value = get_selected
        if self.current_database.value != self.cfgParser.get('MySQL', 'database'):
            self.cfgParser.writeAfterSet('MySQL', 'database', self.current_database.value)

        if self.tree.get_rows():
            self.tree.delete_rows()

    def __selectionComboboxSelected(self, event):
        getval = self.selectionCombobox.get()
        self.tree.delete_rows()

        if len(self.describe(table_name=getval)) == 4:
            for data in self.select('*', table_name=getval):
                self.tree.insert_row(values=[data[0], data[1], data[2], data[3]])
            self.tree.load_table_data()
            return

        # 如果长度>4就从combobox列表中删除该表格
        self.selectionCombobox.clear()
        tableslist = list(self.selectionCombobox.values)

        try:
            tableslist.remove(getval)
            self.selectionCombobox.values = tableslist
        except ValueError as e:
            print(e)

        if not self.isTableLengthOutOfRange:
            self.isTableLengthOutOfRange = True
            Messagebox.show_error(title='Error', message='该表格行长度>4，无法显示')

    def __themeComboboxSelected(self, event):
        self.curr_theme = self.themeCombobox.get()
        self.theme_use(self.curr_theme)
        self.themeCombobox.selection_clear()

    def saveThemeChange(self):
        self.cfgParser.writeAfterSet('App', 'theme', self.curr_theme)

    def createSidebar(self) -> "MainPage":
        lFrame = self.add(labelframe, text='我的数据库 My DataBase', padding=10, bootstyle='success').rpack(
                          fill=X, padx=50, pady=50, side=TOP)  # LabelFrame

        column = 0
        funcDict = {'表操作': None, '库操作': None, '命令行': None}
        for k, v in funcDict.items():
            self.add(button, lFrame, text=k, command=v).grid(column=column, row=0, ipadx=2, ipady=2, padx=2, pady=2)
            column += 1

        self.current_database = self.add(text=self.cfgParser.get('MySQL', 'database'),
                                         wtype=label, parent=lFrame,).rgrid(column=0, row=1, columnspan=3)
        self.databaseCombobox = self.add(combobox, lFrame, width=25).rgrid(column=0, row=2, columnspan=3, pady=5)
        forbid_db_list = ['information_schema', 'performance_schema', 'mysql']
        self.databaseCombobox.values = [db[0] for db in self.show_databases() if db[0] not in forbid_db_list]
        self.databaseCombobox.dbind(self.__databaseComboboxSelected)

        self.add(label, lFrame, text='选择表格: ').grid(column=0, row=3)
        self.selectionCombobox = self.add(combobox, lFrame, width=25).rgrid(column=0, row=4, columnspan=3, pady=5)
        self.selectionCombobox.values = [table[0] for table in self.show_tables()]
        self.selectionCombobox.dbind(self.__selectionComboboxSelected)

        self.panedwin.add(lFrame)
        return self

    def createViewTab(self) -> "MainPage":
        self.add(button, self.rightSideTopFrame, text='用腾讯会议打开', bootstyle='SUCCESS',
                 command=lambda: UIAutomation.openwithTX(self.selectedOptionContent)).pack(padx=10, pady=10, side=LEFT)
        self.add(button, self.rightSideTopFrame, text='用Zoom会议打开', bootstyle='INFO',
                 command=lambda: UIAutomation.openwithZoom(self.selectedOptionContent)).pack(pady=10, side=LEFT)

        self.add(button, self.rightSideTopFrame, text='设置', command=SettingPage).pack(padx=10, pady=10, side=RIGHT)

        self.add(label, self.rightSideFrame, text='选择主题:', font=('Microsoft YaHei', 9)).pack(
                 padx=10, pady=10, side=LEFT)

        self.themeCombobox = self.add(combobox, self.rightSideFrame, width=10, values=self.style.theme_names()).rpack(
                                      pady=10, side=LEFT).rbind(self.__themeComboboxSelected)

        theme_save = self.add(button, self.rightSideFrame, text='保存主题',
                              command=self.saveThemeChange, bootstyle=LIGHT)
        theme_save.pack(padx=10, pady=10, side=LEFT)
        ToolTip(theme_save, text=f'保存后下次启动的默认主题将为你选定的', wraplength=150, bootstyle='info-reverse')

        self.panedwin.add(self.rightSideFrame)  # 添加到 Panedwindow
        return self


if __name__ == '__main__':
    from ttkbootstrap.icons import Icon
    with MainPage() as window:
        window.createSidebar().createViewTab()
