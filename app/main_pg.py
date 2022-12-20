# -*- encoding: utf-8 -*-
import time

from minittk import *


class MainPage(MyWindow):
    def __init__(self, title, geometry):
        super().__init__(title, geometry, (True, True), (450, 200))
        self.cfgfile = './user/config.ini'
        self._connection = UserConnection(self.cfgfile)

        self.panedwin = self.add(panedwindow, orient=HORIZONTAL, bootstyle='info')
        self.panedwin.pack(fill=BOTH, expand=True)
        self.rightFrame = self.add(frame)  # Father of Right Part of Panedwindow
        # Child of rightFrame
        self.rightTopFrame = self.add(frame, parent=self.rightFrame, height=5)
        self.rightTopFrame.pack(fill=X)
        self.tree = self.add_trview(parent=self.rightFrame, columns=('#0', 'col1', 'col2', 'col3'),
                                    heads=('Name', 'Value1', 'Value2', 'Last Modified'), height=10)
        self.tree.pack(fill=BOTH, expand=True)

        self.selectionCombobox: combobox = None
        self.themeCombobox: combobox = None

    @property
    def cursor(self): return self._connection.csr
    def run_query(self, *args, **kwargs): return self._connection.run_query(*args, **kwargs)
    def show_tables(self): return self.run_query('show tables')
    def use(self, db): return self._connection.use(db)
    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mainloop()
        self._connection.close()
        if exc_type is not None:
            raise exc_type()

    @staticmethod
    def __waitForLocate(target):
        while pyautogui.locateCenterOnScreen(target) is None:
            sleep(1)
        return

    def selectionCode(self):
        get_selection = self.tree.focus()  # selection()
        return self.tree.set(get_selection)['col1']  # set() for getting the values of the row

    def openwithTX(self):
        waitfor = self.__waitForLocate
        locate = pyautogui.locateCenterOnScreen
        leftClick = pyautogui.leftClick
        startfile(r"C:\Program Files (x86)\Tencent\WeMeet\wemeetapp.exe")
        waitfor('./meetingapps/tx/join.png')
        leftClick(locate('./meetingapps/tx/join.png'))
        sleep(3.5)
        if locate('./meetingapps/tx/disabled_ch.png') is not None:
            print('go1')
            pyautogui.typewrite(self.selectionCode())
            sleep(1)
            leftClick(locate('./meetingapps/tx/join_ch.png'))
            print('okch')
            return
        elif locate('./meetingapps/tx/disabled_en.png') is not None:
            print('go2')
            pyautogui.typewrite(self.selectionCode())
            sleep(1)
            leftClick(locate('./meetingapps/tx/join_en.png'))
            print('oken')
            return
        raise InterruptedError('bruh.')

    def openwithZoom(self):
        locate = pyautogui.locateCenterOnScreen
        return self

    def __themeComboboxSelected(self, event):
        get_theme = self.themeCombobox.get()
        self.theme_use(get_theme)
        self.themeCombobox.selection_clear()

    def __selectionComboboxSelected(self, event):
        getval = self.selectionCombobox.get()
        # clear Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # restore Treeview
        for i in self.run_query(f'select * from {getval}'):
            try:
                self.tree.insert('', END, text=i[0], values=[i[1], i[2], i[3]])
            except Exception as e:
                pass

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
                    column=i, row=j, ipadx=5, ipady=2, padx=2, pady=2)
                t += 1
        # Combobox Placement
        self.add(label, lFrame, text='选择表格: ').grid(column=0, row=4, columnspan=2)
        self.selectionCombobox = self.add(combobox, lFrame, width=25)
        self.selectionCombobox['value'] = [i[0] for i in self.show_tables()]
        self.selectionCombobox.grid(column=0, row=5, columnspan=5, pady=5, ipady=5)
        self.selectionCombobox.bind('<<ComboboxSelected>>', self.__selectionComboboxSelected)
        self.panedwin.add(lFrame)

    def viewTab(self):
        self.add(button, self.rightTopFrame, text='用腾讯会议打开', command=
                 self.openwithTX).pack(padx=10, pady=10, side=LEFT)

        self.add(button, self.rightTopFrame, text='用Zoom会议打开', command=
                 self.openwithZoom).pack(pady=10, side=LEFT)

        self.add(button, self.rightTopFrame, text='设置').pack(padx=10, pady=10, side=RIGHT)
        self.add(label, self.rightFrame, text='选择主题:', font=('Microsoft YaHei', 9)).pack(
                 padx=10, pady=10, side=LEFT)
        self.themeCombobox = self.add(combobox, self.rightFrame, width=10, value=self.style.theme_names())
        self.themeCombobox.pack(pady=10, side=LEFT)
        self.themeCombobox.bind('<<ComboboxSelected>>', self.__themeComboboxSelected)
        theme_save = self.add(button, self.rightFrame, text='保存主题')
        theme_save.pack(padx=10, pady=10, side=LEFT)
        ToolTip(theme_save, text=f'保存后下次启动的默认主题将为你选定的', wraplength=150, bootstyle='info-reverse')
        self.panedwin.add(self.rightFrame)  # add frame to Panedwindow


if __name__ == '__main__':
    with MainPage('Title', '1200x700') as window:
        window.sidebar()
        window.viewTab()
