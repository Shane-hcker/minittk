# -*- encoding: utf-8 -*-
from minittk import *


class MainPage(MyWindow):
    def __init__(self, title, geometry):
        self.cfgfile = './user/config.ini'
        self._connection = UserConnection(self.cfgfile)
        self.cfgParser = MyConfigParser()
        self.curr_theme = self.cfgParser.get('App', 'theme')
        posX, posY = self.cfgParser.getint('App', 'startupX'), self.cfgParser.getint('App', 'startupY')

        super().__init__(title, geometry, (True, True), (posX, posY), self.curr_theme)

        self.panedwin = self.add(panedwindow, orient=HORIZONTAL, bootstyle='default')
        self.panedwin.pack(fill=BOTH, expand=True)
        self.rightFrame = self.add(frame)  # Father of Right Part of Panedwindow
        # Child of rightFrame
        self.rightTopFrame = self.add(frame, parent=self.rightFrame, height=5)
        self.rightTopFrame.pack(fill=X)
        tree_column = [
            dict(text='Name', stretch=True),
            dict(text='Value1', stretch=True),
            dict(text='Value2', stretch=True),
            dict(text='Last Modified', stretch=True),
        ]
        self.tree = self.add_tabview(parent=self.rightFrame, coldata=tree_column, paginated=True,
                                     searchable=True, stripecolor=(self.style.colors.light, None),
                                     pagesize=20)
        self.tree.pack(fill=BOTH, expand=True)
        self.selectionCombobox: combobox = None
        self.themeCombobox: combobox = None

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mainloop()
        self._connection.close()
        if exc_type is not None:
            raise exc_type()

    @property
    def selectionCode(self):
        get_selection = self.tree.view.focus()  # selection()
        value = self.tree.view.set(get_selection)
        return None if not value else (value['1'], value['2'])  # set() for getting the values of the row

    @staticmethod
    def __waitForLocate(target):
        t = 0
        while pyautogui.locateCenterOnScreen(target) is None:
            t += 1
            if t >= 15:
                raise LookupError('Location not found')
            sleep(1)
            print(f'going {t}')
        return pyautogui.locateCenterOnScreen(target)

    def openLangTX(self, lang=None):
        print(f'goto {lang} v')
        code, pwd = self.selectionCode
        pyautogui.typewrite(code)
        sleep(1)
        pyautogui.leftClick(self.__waitForLocate(f'./meetingapps/tx/join_{lang}.png'))
        if pwd != 'None':
            print(f'{lang} ui runned')
            return
        self.__waitForLocate('./meetingapps/tx/hide_pwd.png')
        pyautogui.typewrite(pwd)
        pyautogui.press('enter')
        print(f'{lang} ui runned')
        return

    def openwithTX(self):
        if not self.selectionCode:
            Messagebox.show_error(message='你未选择任何数据', title='错误')
            return
        startfile(r"C:\Program Files (x86)\Tencent\WeMeet\wemeetapp.exe")
        try:
            join = self.__waitForLocate('./meetingapps/tx/join.png')
            pyautogui.leftClick(join)
            down = self.__waitForLocate('./meetingapps/tx/down.png')
            pyautogui.leftClick(down)
            sleep(.5)
            pyautogui.leftClick(down)
            pyautogui.hotkey('ctrl', 'a')  # ensure that no code history remained
            pyautogui.press('backspace')
            print('ok')
            if pyautogui.locateCenterOnScreen('./meetingapps/tx/disabled_ch.png') is not None:
                self.openLangTX('ch')
            elif pyautogui.locateCenterOnScreen('./meetingapps/tx/disabled_en.png') is not None:
                self.openLangTX('en')
        except LookupError:
            raise LookupError('failure you mother fucker.')

    def openwithZoom(self):
        startfile(r'C:\Users\shane\AppData\Roaming\Zoom\bin\Zoom.exe')
        pyautogui.leftClick(self.__waitForLocate('./meetingapps/zoom/join_meeting_zh.png'))
        pyautogui.typewrite(self.selectionCode)
        pyautogui.leftClick(self.__waitForLocate('./meetingapps/zoom/join_zh.png'))

    def saveThemeChange(self):
        self.cfgParser.set('App', 'theme', self.curr_theme)
        self.cfgParser.write(open(self.cfgParser.cfgfile, 'w'))

    def __themeComboboxSelected(self, event):
        self.curr_theme = self.themeCombobox.get()
        self.theme_use(self.curr_theme)
        self.themeCombobox.selection_clear()

    def __selectionComboboxSelected(self, event):
        getval = self.selectionCombobox.get()
        self.tree.delete_rows()
        for data in self.run_query(f'select * from {getval}'):
            try:
                self.tree.insert_row(END, values=[data[0], data[1], data[2], data[3]])
                self.tree.load_table_data()
            except IndexError:
                raise IndexError(f'Each row of {getval} has to be in a length of 4')

    def sidebar(self):
        # PanedWindow
        lFrame = self.add(labelframe, text='我的数据库 My DataBase', padding=10)
        lFrame.pack(fill=BOTH, padx=50, pady=50, anchor='center')  # LabelFrame
        # Functioned Buttons Placements
        t = 0
        funcName = ['创建表', '复制表', '迁移表', '导出表', '导入表', '创建库']
        for i in range(1, 4):
            for j in range(1, 3):
                self.add(button, lFrame, text=funcName[t]).grid(
                    column=i, row=j, ipadx=2, ipady=2, padx=2, pady=2)
                t += 1
        # Combobox Placement
        self.add(label, lFrame, text='选择表格: ').grid(column=0, row=4, columnspan=2)
        self.selectionCombobox = self.add(combobox, lFrame, width=25)
        self.selectionCombobox['value'] = [i[0] for i in self.show_tables()
                                           if len(self.run_query(f'desc {i[0]}')) == 4]
        self.selectionCombobox.grid(column=0, row=5, columnspan=5, pady=5, ipady=5)
        self.selectionCombobox.bind('<<ComboboxSelected>>', self.__selectionComboboxSelected)
        self.panedwin.add(lFrame)

    def viewTab(self):
        self.add(button, self.rightTopFrame, text='用腾讯会议打开', bootstyle='SUCCESS',
                 command=self.openwithTX).pack(padx=10, pady=10, side=LEFT)
        self.add(button, self.rightTopFrame, text='用Zoom会议打开', bootstyle='INFO',
                 command=self.openwithZoom).pack(pady=10, side=LEFT)
        self.add(button, self.rightTopFrame, text='设置').pack(padx=10, pady=10, side=RIGHT)
        self.add(label, self.rightFrame, text='选择主题:', font=('Microsoft YaHei', 9)).pack(
                 padx=10, pady=10, side=LEFT)

        self.themeCombobox = self.add(combobox, self.rightFrame, width=10, value=self.style.theme_names())
        self.themeCombobox.pack(pady=10, side=LEFT)
        self.themeCombobox.bind('<<ComboboxSelected>>', self.__themeComboboxSelected)
        theme_save = self.add(button, self.rightFrame, text='保存主题', command=self.saveThemeChange)
        theme_save.pack(padx=10, pady=10, side=LEFT)
        ToolTip(theme_save, text=f'保存后下次启动的默认主题将为你选定的', wraplength=150, bootstyle='info-reverse')
        self.panedwin.add(self.rightFrame)  # add frame to Panedwindow

    @property
    def cursor(self): return self._connection.csr
    def run_query(self, *args, **kwargs): return self._connection.run_query(*args, **kwargs)
    def show_tables(self): return self.run_query('show tables')
    def use(self, db): return self._connection.use(db)


if __name__ == '__main__':
    with MainPage('Title', '1200x700') as window:
        window.sidebar()
        window.viewTab()
