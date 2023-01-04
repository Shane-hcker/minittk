# -*- encoding: utf-8 -*-
from user.setting import SettingPage
from minittk import *


class MainPage(MyWindow):
    def __init__(self):
        self.cfgfile = './user/config.ini'
        self._connection = UserConnection(self.cfgfile)
        self.cfgParser = MyConfigParser()
        self.curr_theme = self.cfgParser.get('App', 'theme')
        posX, posY = self.cfgParser.getint('App', 'startup.x'), self.cfgParser.getint('App', 'startup.y')
        super().__init__('Title', '1200x700', (True, True), (posX, posY), self.curr_theme)
        self.panedwin = self.add(panedwindow, orient=HORIZONTAL, bootstyle='default').rpack(fill=BOTH, expand=True)
        self.rightSideFrame = self.add(frame)  # r < 右侧的 Panedwindow
        # Child of rightFrame
        self.rightSideTopFrame = self.add(frame, parent=self.rightSideFrame, height=5).rpack(fill=X)
        tree_column = [{'text': 'Name', 'stretch': True}, {'text': 'Val1', 'stretch': True},
                       {'text': 'Val2', 'stretch': True}, {'text': 'Last Modified', 'stretch': True}]
        self.tree = self.add_tabview(parent=self.rightSideFrame, coldata=tree_column, paginated=True,
                                     searchable=True, stripecolor=(self.style.colors.light, None),
                                     pagesize=20).rpack(fill=BOTH, expand=True)
        self.selectionCombobox: combobox = None
        self.themeCombobox: combobox = None

    def __call__(self, *args, **kwargs) -> None:
        self.mainloop()
        self._connection.close()

    def __enter__(self) -> "MainPage": return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mainloop()
        self._connection.close()
        if exc_type is not None:
            raise exc_type()

    @property
    def cursor(self) -> Cursor:
        return self._connection.csr

    def run_query(self, *args, **kwargs) -> tuple:
        return self._connection.run_query(*args, **kwargs)

    def show_tables(self) -> tuple:
        return self.run_query('show tables')

    def use(self, db) -> tuple:
        """TODO 可以用于切换数据库"""
        self._connection.use(db)
        return self.show_tables()

    @property
    def selectionCode(self):
        get_selection = self.tree.view.focus()  # selection()
        value = self.tree.view.set(get_selection)
        return None if not value else (value['1'], value['2'])  # set()获取当前row的值

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
                self.tree.insert_row(values=[data[0], data[1], data[2], data[3]])
                self.tree.load_table_data()
            except IndexError:
                raise IndexError(f'Each row of {getval} has to be in a length of 4')

    def createSidebar(self):
        lFrame = self.add(labelframe, text='我的数据库 My DataBase', padding=10, bootstyle='success').rpack(
                          fill=BOTH, padx=50, pady=50, anchor='center')  # LabelFrame
        # 功能按钮
        t = 0
        funcDict = {'表操作': None, '库操作': None, '命令行': None}
        for k, v in funcDict.items():
            self.add(button, lFrame, text=k, command=v).grid(column=t, row=0, ipadx=2, ipady=2, padx=2, pady=2)
            t += 1
        # Combobox
        self.add(label, lFrame, text='选择表格: ').grid(column=0, row=1)
        self.selectionCombobox = self.add(combobox, lFrame, width=25)
        self.selectionCombobox['value'] = [i[0] for i in self.show_tables()
                                           if len(self.run_query(f'desc {i[0]}')) == 4]
        self.selectionCombobox.grid(column=0, row=2, columnspan=3, pady=5)
        self.selectionCombobox.bind('<<ComboboxSelected>>', self.__selectionComboboxSelected)
        self.panedwin.add(lFrame)
        return self

    def createViewTab(self):
        self.add(button, self.rightSideTopFrame, text='用腾讯会议打开', bootstyle='SUCCESS',
                 command=lambda: UIAutomation.openwithTX(self.selectionCode)).pack(padx=10, pady=10, side=LEFT)
        self.add(button, self.rightSideTopFrame, text='用Zoom会议打开', bootstyle='INFO',
                 command=lambda: UIAutomation.openwithZoom(self.selectionCode)).pack(pady=10, side=LEFT)
        self.add(button, self.rightSideTopFrame, text='设置', command=SettingPage).pack(padx=10, pady=10, side=RIGHT)
        self.add(label, self.rightSideFrame, text='选择主题:', font=('Microsoft YaHei', 9)).pack(
                 padx=10, pady=10, side=LEFT)
        self.themeCombobox = self.add(combobox, self.rightSideFrame, width=10, value=self.style.theme_names()).rpack(
                                      pady=10, side=LEFT).rbind('<<ComboboxSelected>>', self.__themeComboboxSelected)
        theme_save = self.add(button, self.rightSideFrame, text='保存主题', command=self.saveThemeChange, bootstyle=LIGHT)
        theme_save.pack(padx=10, pady=10, side=LEFT)
        ToolTip(theme_save, text=f'保存后下次启动的默认主题将为你选定的', wraplength=150, bootstyle='info-reverse')
        self.panedwin.add(self.rightSideFrame)  # 添加到 Panedwindow
        return self


if __name__ == '__main__':
    with MainPage() as window:
        window.createSidebar().createViewTab()
