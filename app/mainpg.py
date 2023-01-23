# -*- encoding: utf-8 -*-
from minittk import *
from operations.tableops import TableOperationMenu
from operations.dbops import DatabaseOperationMenu
from user.setting import SettingPage


@UserConnection.usemysql()
@MyConfigParser.useconfig()
class MainPage(MyWindow):
    def __init__(self):
        print(f'__init__(): {self}, id: {id(self)}')
        self.curr_theme = self.cfgParser.get('App', 'theme')
        startup_pos = (self.cfgParser.getint('App', 'startup.x'), self.cfgParser.getint('App', 'startup.y'))

        super().__init__('Title', '1200x700', (True, True), startup_pos, self.curr_theme)

        self.isTableLengthOutOfRange: bool = False
        self.isRunningMeetingApp: bool = False
        self.current_table: str = ...
        self.database_label: Label = ...
        self.databaseCombobox: Combobox = ...
        self.selectionCombobox: Combobox = ...
        self.themeCombobox: Combobox = ...

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
        self.forbid_db_list = ['information_schema', 'performance_schema', 'mysql']

    def createSidebar(self) -> "MainPage":
        lFrame = self.add(labelframe, text='我的数据库 My DataBase', padding=10, bootstyle='success').rpack(
            fill=X, padx=50, pady=50, side=TOP)  # LabelFrame

        column = 0
        funcDict = {'表操作': None, '库操作': None, '命令行': None}
        for k, v in funcDict.items():
            self.add(button, lFrame, text=k, command=v).grid(column=column, row=0, ipadx=2, ipady=2, padx=2, pady=2)
            column += 1

        self.database_label = self.add(text=self.cfgParser.get('MySQL', 'database'),
                                       wtype=label, parent=lFrame, ).rgrid(column=0, row=1, columnspan=3)
        self.databaseCombobox = self.add(combobox, lFrame, width=25).rgrid(column=0, row=2, columnspan=3, pady=5)
        self.databaseCombobox.values = self.show_filtered_databases(restriction=self.forbid_db_list)
        self.databaseCombobox.dbind(self.__databaseComboboxSelected)

        self.add(label, lFrame, text='选择表格: ').grid(column=0, row=3)
        self.selectionCombobox = self.add(combobox, lFrame, width=25).rgrid(column=0, row=4, columnspan=3, pady=5)
        self.selectionCombobox.values = [table[0] for table in self.show_tables()]
        self.selectionCombobox.dbind(self.__selectionComboboxSelected)

        self.panedwin.add(lFrame)
        return self

    def createViewTab(self) -> "MainPage":
        self.add(button, self.rightSideTopFrame, text='启动腾讯会议', bootstyle=(SUCCESS, OUTLINE),
                 command=self.openTX).pack(padx=10, pady=10, side=LEFT)
        self.add(button, self.rightSideTopFrame, text='启动Zoom', bootstyle=SUCCESS,
                 command=self.openZoom).pack(pady=10, side=LEFT)

        self.add(button, self.rightSideTopFrame, text='设置', command=SettingPage).pack(padx=10, pady=10, side=RIGHT)

        self.add(label, self.rightSideFrame, text='选择主题:', font=('Microsoft YaHei', 9)).pack(
                 padx=10, pady=10, side=LEFT)

        self.themeCombobox = self.add(combobox, self.rightSideFrame, width=10, values=self.style.theme_names()).rpack(
                                      pady=10, side=LEFT).dbind(self.__themeComboboxSelected)

        theme_save = self.add(button, self.rightSideFrame, text='保存主题',
                              command=self.saveThemeChange, bootstyle=(INFO, OUTLINE))
        theme_save.pack(padx=10, pady=10, side=LEFT)
        ToolTip(theme_save, text=f'保存后下次启动的默认主题将为你选定的', wraplength=150, bootstyle='info-inverse')

        self.panedwin.add(self.rightSideFrame)  # 添加到 Panedwindow
        return self

    def __call__(self, *args, **kwargs):
        self.mainloop()
        self._connection.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        DatabaseOperationMenu(self)
        TableOperationMenu(self)
        self.mainloop()
        self._connection.close()
        if exc_type:
            raise exc_type()

    def openTX(self):
        if self.isRunningMeetingApp:
            return
        self.isRunningMeetingApp = True
        UIAutomation.openwithTX(self.selectedOptionContent)
        self.isRunningMeetingApp = False

    def openZoom(self):
        if self.isRunningMeetingApp:
            return
        self.isRunningMeetingApp = True
        UIAutomation.openwithZoom(self.selectedOptionContent)
        self.isRunningMeetingApp = False

    @property
    def selectedOptionContent(self) -> Tuple[Any, Any]:
        value = self.tree.get_selected_row()
        return None if not value else (value['1'], value['2'])  # set()获取当前row的值

    def __databaseComboboxSelected(self, event):
        get_selected = self.databaseCombobox.get()
        self.selectionCombobox.values = [table for (table,) in self.use(get_selected)]
        self.selectionCombobox.clear()

        self.database_label.value = get_selected
        if self.database_label.value != self.cfgParser.get('MySQL', 'database'):
            self.saveDatabaseChange()

        if self.tree.get_rows():
            self.tree.delete_rows()

    def __selectionComboboxSelected(self, event):
        self.current_table = self.selectionCombobox.get()
        self.tree.delete_rows()

        if len(self.describe(table_name=self.current_table)) == 4:
            self.tree.forInsert(4, self.select('*', table_name=self.current_table))
            self.tree.load_table_data()
            return

        # 如果长度>4就从combobox列表中删除该表格
        self.selectionCombobox.clear()
        self.selectionCombobox.remove(self.current_table)

        if not self.isTableLengthOutOfRange:
            self.isTableLengthOutOfRange = True
            Messagebox.show_error(title='Error', message='该表格行长度>4，无法显示')

    def __themeComboboxSelected(self, event):
        self.curr_theme = self.themeCombobox.get() if self.themeCombobox.get() else 'litera'
        self.theme_use(self.curr_theme)
        self.themeCombobox.selection_clear()

    def saveDatabaseChange(self):
        self.cfgParser.writeAfterSet('MySQL', 'database', self.database_label.value)

    def saveThemeChange(self):
        self.cfgParser.writeAfterSet('App', 'theme', self.curr_theme)


if __name__ == '__main__':
    with MainPage() as window:
        window.createSidebar().createViewTab()
