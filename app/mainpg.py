# -*- encoding: utf-8 -*-
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process
from time import perf_counter as pc

from minittk import *
from user.eventactions import EventActions


total_handler = 1
sendQueue, recvQueue = (asyncio.Queue(), asyncio.Queue())
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
        self.ok = False
        self.window.bind('<Motion>', self.__init_widgets)
        self.checkbuttonBooleanVar = boolvar()
        self.panedwin = self.add(panedwindow, orient=HORIZONTAL, bootstyle='default').rpack(fill=BOTH, expand=True)
        self.rightSideFrame = self.add(frame)
        self.rightSideTopFrame = self.add(frame, parent=self.rightSideFrame, height=5).rpack(fill=X)

        self.tree = self.add_tabview(parent=self.rightSideFrame, coldata=tree_column, paginated=True,
                                     searchable=True, pagesize=20).rpack(fill=BOTH, expand=True)
        # DatabaseOperationMenu(self)
        # TableOperationMenu(self)

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)

    def createSidebar(self) -> "MainPage":
        lFrame = self.add(labelframe, text='??????????????? My Database', padding=10,
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
        self.add(label, master, text='????????????: ').grid(column=0, row=3)

    def __setupSideBarWidgets(self, master):
        addon = partial(self.add, parent=master)
        addon(button, text='??????SQL??????', command=None, width=25).grid(column=0, row=0, columnspan=3, ipady=2, pady=2)

        self.databaseCombobox = addon(combobox, width=25)
        self.selectionCombobox = addon(combobox, width=25)

        # self.databaseCombobox.dbind()
        # self.selectionCombobox.dbind()

        self.databaseCombobox.grid(column=0, row=2, columnspan=3, pady=5)
        self.selectionCombobox.grid(column=0, row=4, columnspan=3, pady=5)

        addon(separator, bootstyle=SUCCESS).grid(sticky='ew', column=0, columnspan=3, row=5, pady=15)

        # setupTemporaryMeeting
        addon(label, text='????????????: ').grid(column=0, row=6)

        addon(label, text='?????????:').grid(column=0, row=7, pady=5)
        self.tempValueEntry = addon(entry, bootstyle=SUCCESS, width=20).rgrid(column=1, row=7, pady=5)

        addon(label, text='??????(??????):').grid(column=0, row=8)
        self.tempPwdEntry = addon(entry, bootstyle=SUCCESS, width=20).rgrid(column=1, row=8, pady=5)

        self.uploadCheckbutton = addon(checkbutton, text='?????????????????????????????????', variable=self.checkbuttonBooleanVar,
                                       command=self.__uploadCheckbuttonTrigger, bootstyle=(INFO, ROUND, TOGGLE))

        self.uploadCheckbutton.grid(column=0, row=9, columnspan=2, pady=10)

        self.uploadCheckbutton.invoke() if self.cfgParser.getboolean('Meeting', 'uploadable') else None
        self.uploadCheckbutton.set_state(DISABLED)

    def __setupViewTabUpper(self):
        addon = partial(self.add, parent=self.rightSideTopFrame)
        addon(button, bootstyle=(SUCCESS, OUTLINE), command=None,
              text='??????????????????').pack(padx=10, pady=10, side=LEFT)

        addon(button, text='??????Zoom', command=None,
              bootstyle=SUCCESS).pack(pady=10, side=LEFT)

        addon(button, text='??????', command=None).pack(padx=10, pady=10, side=RIGHT)

    def __setupViewTabLower(self):
        addon = partial(self.add, parent=self.rightSideFrame)
        addon(label, text='????????????:').pack(padx=10, pady=10, side=LEFT)

        self.themeCombobox = addon(combobox, values=self.style.theme_names(),
                                   width=10).rpack(pady=10, side=LEFT).dbind(EventActions.themeComboboxSelected(self))

        theme_save_btn = addon(button, command=self.saveThemeChange, text='????????????',
                               bootstyle=(INFO, OUTLINE)).rpack(padx=10, pady=10, side=LEFT)

        display_text = MessageCatalog.translate('??????????????????????????????????????????????????????')
        theme_save_btn.attach_tooltip(text=display_text, wraplength=150, bootstyle=(INFO, INVERSE))

    def __init_widgets(self, event):
        if self.ok:
            return
        self.ok = True
        print(sendQueue.get_nowait())

    def __uploadCheckbuttonTrigger(self):
        uploadable = str(self.checkbuttonBooleanVar.get())
        self.cfgParser.writeAfterSet('Meeting', 'uploadable', uploadable)

    def getTMeetingValues(self):
        """intervene temporary meeting slot to table"""
        value = self.tempValueEntry.value
        password = self.tempPwdEntry.value if self.tempPwdEntry.value else 'null'

        if not self.checkbuttonBooleanVar.get():
            return value, password

        if not (name := Querybox.get_string('???????????????????????????????????????', 'Title')):
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
                return Messagebox.show_error(message='????????????????????????', title='??????')

            app(optionContent)
            self.isRunningMeetingApp = False

    def saveDatabaseChange(self):
        self.cfgParser.writeAfterSet('MySQL', 'database', self.database_label.value)

    def saveThemeChange(self):
        self.cfgParser.writeAfterSet('App', 'theme', self.curr_theme)

    @property
    def selectedOptionContent(self) -> Tuple[Any, Any]:
        value = self.tree.get_selected_row()  # set()????????????row??????
        return None if not value else (value['1'], value['2'])

    @staticmethod
    def join(process: Process):
        process.start()
        process.join()
        [sendQueue.put_nowait(terminate) for _ in range(total_handler)]

    @staticmethod
    def generate():
        app = MainPage().createSidebar().createViewTab()
        app()


async def main():
    # fixme not sending anything
    loop = asyncio.get_running_loop()
    handler = [SQLHandler(sendQueue, recvQueue, config_file).run_forever() for _ in range(total_handler)]
    window_proc = Process(target=MainPage.generate)
    connect = asyncio.gather(*handler)
    await loop.run_in_executor(None, MainPage.join, window_proc)
    await connect


if __name__ == '__main__':
    asyncio.run(main())
