# -*- encoding: utf-8 -*-
import asyncio

from minittk import *
from user.eventactions import EventActions


sendQueue, recvQueue = queues = (asyncio.Queue(), asyncio.Queue())
sender = SQLSender(sendQueue)


@sender.assignAttributesTo
@MyConfigParser.setupConfig(config_file)
class MainPage(MyWindow):
    def __init__(self):
        print(f'__init__(): {self}, id: {id(self)}')
        startup_pos = (self.cfgParser.getint('App', 'startup.x'), self.cfgParser.getint('App', 'startup.y'))

        self.isRunningMeetingApp: bool = False
        self.isTableLengthOutOfRange: bool = False

        self.curr_theme = self.cfgParser.get('App', 'theme')
        self.current_table: str = ...
        self.database_label: Label = ...
        self.uploadCheckbutton: Checkbutton = ...
        self.themeCombobox: Combobox = ...
        self.databaseCombobox: Combobox = ...
        self.selectionCombobox: Combobox = ...
        self.tempValueEntry: Entry = ...
        self.tempPwdEntry: Entry = ...

        self.eventActions = EventActions(self)

        self.forbid_db_list = ['information_schema', 'performance_schema', 'mysql']

        tree_column = [
            {'text': 'Name', 'stretch': True},
            {'text': 'Value', 'stretch': True},
            {'text': 'Password', 'stretch': True},
            {'text': 'Last Modified', 'stretch': True}
        ]

        super().__init__('Title', '1200x700', (True, True), startup_pos, self.curr_theme)

        self.checkbuttonBooleanVar = boolvar()
        self.panedwin = self.add(panedwindow, orient=HORIZONTAL, bootstyle='default').rpack(fill=BOTH, expand=True)
        self.rightSideFrame = self.add(frame)
        self.rightSideTopFrame = self.add(frame, parent=self.rightSideFrame, height=5).rpack(fill=X)

        self.tree = self.add_tabview(parent=self.rightSideFrame, coldata=tree_column, paginated=True,
                                     searchable=True, pagesize=20).rpack(fill=BOTH, expand=True)
        self.run = self.__call__
        # DatabaseOperationMenu(self)
        # TableOperationMenu(self)

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
        # self.show_databases(restriction=self.forbid_db_list)
        # self.databaseCombobox.values = recvQueue.get_nowait()
        # self.selectionCombobox.values = [table for (table, ) in await self.show_tables()]

        self.databaseCombobox.dbind()
        self.selectionCombobox.dbind()

        self.databaseCombobox.grid(column=0, row=2, columnspan=3, pady=5)
        self.selectionCombobox.grid(column=0, row=4, columnspan=3, pady=5)

        addon(separator, bootstyle=SUCCESS).grid(sticky='ew', column=0, columnspan=3, row=5, pady=15)

        # setupTemporaryMeeting
        addon(label, text='临时入会: ').grid(column=0, row=6)

        addon(label, text='会议码:').grid(column=0, row=7, pady=5)
        self.tempValueEntry = addon(entry, bootstyle=SUCCESS, width=20).rgrid(column=1, row=7, pady=5)

        addon(label, text='密码(如需):').grid(column=0, row=8)
        self.tempPwdEntry = addon(entry, bootstyle=SUCCESS, width=20).rgrid(column=1, row=8, pady=5)

        self.uploadCheckbutton = addon(checkbutton, text='保存会议数据到当前表格', variable=self.checkbuttonBooleanVar,
                                       command=self.__uploadCheckbuttonTrigger, bootstyle=(INFO, ROUND, TOGGLE))

        self.uploadCheckbutton.grid(column=0, row=9, columnspan=2, pady=10)

        self.uploadCheckbutton.invoke() if self.cfgParser.getboolean('Meeting', 'uploadable') else None
        self.uploadCheckbutton.set_state(DISABLED)

    def __setupViewTabUpper(self):
        addon = partial(self.add, parent=self.rightSideTopFrame)
        addon(button, bootstyle=(SUCCESS, OUTLINE), command=None,
              text='启动腾讯会议').pack(padx=10, pady=10, side=LEFT)

        addon(button, text='启动Zoom', command=None,
              bootstyle=SUCCESS).pack(pady=10, side=LEFT)

        addon(button, text='设置', command=None).pack(padx=10, pady=10, side=RIGHT)

    def __setupViewTabLower(self):
        addon = partial(self.add, parent=self.rightSideFrame)
        addon(label, text='选择主题:').pack(padx=10, pady=10, side=LEFT)

        self.themeCombobox = addon(combobox, values=self.style.theme_names(),
                                   width=10).rpack(pady=10, side=LEFT).dbind(EventActions.themeComboboxSelected(self))

        theme_save_btn = addon(button, command=self.saveThemeChange, text='保存主题',
                               bootstyle=(INFO, OUTLINE)).rpack(padx=10, pady=10, side=LEFT)

        display_text = MessageCatalog.translate('保存后下次启动的默认主题将为你选定的')
        theme_save_btn.attach_tooltip(text=display_text, wraplength=150, bootstyle=(INFO, INVERSE))

    def __uploadCheckbuttonTrigger(self):
        uploadable = str(self.checkbuttonBooleanVar.get())
        self.cfgParser.writeAfterSet('Meeting', 'uploadable', uploadable)

    def getTMeetingValues(self):
        """intervene temporary meeting slot to table"""
        value = self.tempValueEntry.value
        password = self.tempPwdEntry.value if self.tempPwdEntry.value else 'null'

        if not self.checkbuttonBooleanVar.get():
            return value, password

        if not (name := Querybox.get_string('请输入你要保存的条目的名称', 'Title')):
            return

        self.tinsert(self.current_table, name, value, password)
        self.tree.insert_row(values=self.select(self.current_table, '*',
                                                condition=f'where `Name`=\'{name}\'')[0])
        self.tree.load_table_data()
        return value, password

    async def open(self, app):
        if not self.isRunningMeetingApp:
            self.isRunningMeetingApp = True
            optionContent = self.getTMeetingValues() if self.tempValueEntry.value else self.selectedOptionContent

            if not optionContent:
                self.isRunningMeetingApp = False
                return Messagebox.show_error(message='你未选择任何数据', title='错误')

            app(optionContent)
            self.isRunningMeetingApp = False

    def saveDatabaseChange(self):
        self.cfgParser.writeAfterSet('MySQL', 'database', self.database_label.value)

    def saveThemeChange(self):
        self.cfgParser.writeAfterSet('App', 'theme', self.curr_theme)

    @property
    def selectedOptionContent(self) -> Tuple[Any, Any]:
        value = self.tree.get_selected_row()  # set()获取当前row的值
        return None if not value else (value['1'], value['2'])

    @classmethod
    async def generate(cls):
        cls().createSidebar().createViewTab().run()


async def main():
    # fixme mainloop => 多线程 / 上下文管理器块内 提供解决方案
    connect = asyncio.create_task(SQLHandler(sendQueue, recvQueue, config_file).connect())
    await MainPage.generate()
    await connect

if __name__ == '__main__':
    total_handler = 1
    asyncio.run(main())
