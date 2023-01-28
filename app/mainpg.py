# -*- encoding: utf-8 -*-
from functools import wraps

from minittk import *

from user.setting import SettingPage
from operations.tableops import TableOperationMenu
from operations.dbops import DatabaseOperationMenu


@UserConnection.usemysql()
@MyConfigParser.useconfig()
class MainPage(MyWindow):
    def __init__(self):
        print(f'__init__(): {self}, id: {id(self)}')
        self.curr_theme = self.cfgParser.get('App', 'theme')
        startup_pos = (self.cfgParser.getint('App', 'startup.x'), self.cfgParser.getint('App', 'startup.y'))

        super().__init__('Title', '1200x700', (True, True), startup_pos, self.curr_theme)

        self.isRunningMeetingApp: bool = False
        self.isTableLengthOutOfRange: bool = False
        self.current_table: str = ...
        self.database_label: Label = ...
        self.themeCombobox: Combobox = ...
        self.databaseCombobox: Combobox = ...
        self.selectionCombobox: Combobox = ...
        self.uploadCheckbutton: Checkbutton = ...
        self.checkbuttonBooleanVar = boolvar()
        self.forbid_db_list = ['information_schema', 'performance_schema', 'mysql']

        tree_column = [
            {'text': 'Name', 'stretch': True},
            {'text': 'Value', 'stretch': True},
            {'text': 'Password', 'stretch': True},
            {'text': 'Last Modified', 'stretch': True}
        ]

        self.panedwin = self.add(panedwindow, orient=HORIZONTAL, bootstyle='default').rpack(fill=BOTH, expand=True)
        self.rightSideFrame = self.add(frame)
        self.rightSideTopFrame = self.add(frame, parent=self.rightSideFrame, height=5).rpack(fill=X)

        self.tree = self.add_tabview(parent=self.rightSideFrame, coldata=tree_column, paginated=True,
                                     searchable=True, pagesize=20).rpack(fill=BOTH, expand=True)

        self.createSidebar().createViewTab()
        DatabaseOperationMenu(self)
        TableOperationMenu(self)

    def createSidebar(self) -> "MainPage":
        lFrame = self.add(labelframe, text='我的数据库 My Database', padding=10,
                          bootstyle=SUCCESS).rpack(fill=X, padx=50, pady=50, side=TOP)

        self.__setupSideBarLabels(master=lFrame)
        self.__setupSideBarWidgets(master=lFrame)
        self.panedwin.add(lFrame)
        return self

    def createViewTab(self) -> "MainPage":
        self.__setupViewTabUpper()
        self.__setupViewTabLower()
        self.panedwin.add(self.rightSideFrame)
        return self

    def __setupSideBarLabels(self, master):
        self.database_label = self.add(text=self.cfgParser.get('MySQL', 'database'), wtype=label, parent=master)
        self.database_label.grid(column=0, row=1, columnspan=3)
        self.add(label, master, text='选择表格: ').grid(column=0, row=3)

    def __setupSideBarWidgets(self, master):
        addon = partial(self.add, parent=master)
        addon(button, text='输入SQL指令', command=None, width=25).grid(column=0, row=0, columnspan=3, ipady=2, pady=2)

        self.databaseCombobox = addon(combobox, width=25)
        self.selectionCombobox = addon(combobox, width=25)
        self.databaseCombobox.values = self.show_filtered_databases(restriction=self.forbid_db_list)
        self.selectionCombobox.values = [table[0] for table in self.show_tables()]

        self.databaseCombobox.dbind(self.__databaseComboboxSelected)
        self.selectionCombobox.dbind(self.__selectionComboboxSelected)

        self.databaseCombobox.grid(column=0, row=2, columnspan=3, pady=5)
        self.selectionCombobox.grid(column=0, row=4, columnspan=3, pady=5)
        addon(separator, bootstyle=SUCCESS).grid(sticky='ew', column=0, columnspan=3, row=5, pady=15)
        self.__setupTemporaryMeeting(master)

    def __setupTemporaryMeeting(self, master):
        addon = partial(self.add, parent=master)
        addon(label, text='临时入会: ').grid(column=0, row=6)

        addon(label, text='会议码:').grid(column=0, row=7, pady=5)
        id_entry = addon(entry, bootstyle=SUCCESS, width=20).rgrid(column=1, row=7, pady=5)

        addon(label, text='密码(如需):').grid(column=0, row=8)
        pwd_entry = addon(entry, bootstyle=SUCCESS, width=20).rgrid(column=1, row=8, pady=5)

        self.uploadCheckbutton = addon(checkbutton, text='保存会议数据到当前表格', bootstyle=(INFO, ROUND, TOGGLE),
                                       onvalue=True, offvalue=False, command=self.__uploadCheckbuttonTrigger,
                                       variable=self.checkbuttonBooleanVar)
        self.uploadCheckbutton.grid(column=0, row=9, columnspan=2, pady=5)

    def __setupViewTabUpper(self):
        addon = partial(self.add, parent=self.rightSideTopFrame)
        addon(button, bootstyle=(SUCCESS, OUTLINE), command=lambda: self.open(UIAutomation.openwithTX),
              text='启动腾讯会议').pack(padx=10, pady=10, side=LEFT)

        addon(button, text='启动Zoom', command=lambda: self.open(UIAutomation.openwithZoom),
              bootstyle=SUCCESS).pack(pady=10, side=LEFT)

        addon(button, text='设置', command=SettingPage).pack(padx=10, pady=10, side=RIGHT)

    def __setupViewTabLower(self):
        addon = partial(self.add, parent=self.rightSideFrame)
        addon(label, text='选择主题:').pack(padx=10, pady=10, side=LEFT)

        self.themeCombobox = addon(combobox, values=self.style.theme_names(),
                                   width=10).rpack(pady=10, side=LEFT).dbind(self.__themeComboboxSelected)

        theme_save_btn = addon(button, command=self.saveThemeChange, text='保存主题',
                               bootstyle=(INFO, OUTLINE)).rpack(padx=10, pady=10, side=LEFT)

        display_text = MessageCatalog.translate('保存后下次启动的默认主题将为你选定的')
        theme_save_btn.attach_tooltip(text=display_text, wraplength=150, bootstyle=(INFO, INVERSE))

    def open(self, app):
        if not self.isRunningMeetingApp:
            self.isRunningMeetingApp = True
            app(self.selectedOptionContent)
            self.isRunningMeetingApp = False

    def saveDatabaseChange(self):
        self.cfgParser.writeAfterSet('MySQL', 'database', self.database_label.value)

    def saveThemeChange(self):
        self.cfgParser.writeAfterSet('App', 'theme', self.curr_theme)

    def __uploadCheckbuttonTrigger(self):
        print(self.checkbuttonBooleanVar.get())

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
            return self.tree.load_table_data()

        self.selectionCombobox.clear()
        self.selectionCombobox.remove(self.current_table)

        if not self.isTableLengthOutOfRange:
            self.isTableLengthOutOfRange = True
            Messagebox.show_error(title='Error', message='该表格行长度>4，无法显示')

    def __themeComboboxSelected(self, event):
        self.curr_theme = self.themeCombobox.get() if self.themeCombobox.get() else 'litera'
        self.theme_use(self.curr_theme)
        self.themeCombobox.selection_clear()

    def __call__(self, *args, **kwargs):
        self.mainloop()
        self._connection.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mainloop()
        self._connection.close()
        if exc_type:
            raise exc_type()


if __name__ == '__main__':
    window = MainPage()
    window()
