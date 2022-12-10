# -*- encoding: utf-8 -*-
from minittk import *


class MainPage(MyWindow):
    def __init__(self, title, geometry):
        resize = (True, True)
        position = (450, 200)
        super().__init__(title, geometry, resize, position)

        # Panedwindow
        self.panedwin = self.add(panedwindow, orient=HORIZONTAL, bootstyle='info')
        self.panedwin.pack(fill=BOTH, expand=True)
        # Frame
        self.rightFrame = self.add(frame)  # Father of Right Part of Panedwindow
        # Frame for button placement
        self.rightTopFrame = self.add(frame, parent=self.rightFrame, height=5)
        self.rightTopFrame.pack(fill=X)

        # Treeview
        self.tree = self.add_trview(parent=self.rightFrame, columns=('#0', 'col1', 'col2', 'col3'),
                                    heads=('Name', 'Value1', 'Value2', 'Last Modified'), height=10)
        self.tree.pack(fill=BOTH, expand=True)

        # Combobox
        self.selectionCombobox: combobox = None
        self.themeCombobox: combobox = None
        self.__sidebar()
        self.__viewTab()

    def __selectionComboboxSelected(self, event):
        """Combobox trigger"""
        getval = self.selectionCombobox.get()
        # clear Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # restore Treeview
        for i in range(int(getval)):
            self.tree.insert('', END, text='21312', values=[1, 2, 3])

    def add_trview(self, columns, heads, height=None, parent=None):
        trview = self.add(treeview, parent, column=columns[1:], height=height, bootstyle='primary')
        for i in range(len(columns)):
            trview.column(columns[i], anchor=CENTER)
            trview.heading(columns[i], text=heads[i])
        return trview

    def __sidebar(self):
        """左侧边栏"""
        # PanedWindow
        lFrame = self.add(labelframe, text='我的数据库 My DataBase', padding=10)
        lFrame.pack(fill=BOTH, padx=50, pady=50, anchor='center')  # LabelFrame

        # LabelFrame Widgets
        # Functioned Buttons Placements
        t = 0
        funcs = ['创建', '复制', '迁移', '导出', '导入', '命令']
        for i in range(1, 4):
            for j in range(1, 3):
                self.add(button, lFrame, text=funcs[t], command=lambda: print(funcs[t-1])).grid(
                    column=i, row=j, ipadx=5, ipady=2, padx=2, pady=2)
                t += 1
        # Combobox Placement
        self.add(label, lFrame, text='选择表格: ').grid(column=0, row=4, columnspan=2)
        self.selectionCombobox = self.add(combobox, lFrame, value=[1, 2, 3, 4], width=25)
        self.selectionCombobox.grid(column=0, row=5, columnspan=5, pady=5, ipady=5)
        # Bind event
        self.selectionCombobox.bind('<<ComboboxSelected>>', self.__selectionComboboxSelected)

        self.panedwin.add(lFrame)

    def __viewTab(self):
        """similar to the editor tab of PyCharm"""
        # Buttons
        self.add(button, self.rightTopFrame, text='腾讯会议打开').pack(padx=10, pady=10, side=LEFT)
        self.add(button, self.rightTopFrame, text='Zoom会议打开').pack(pady=10, side=LEFT)
        self.add(button, self.rightTopFrame, text='账户').pack(padx=10, pady=10, side=RIGHT)
        # Theme Combobox
        self.add(label, self.rightFrame, text='选择主题:', font=('Microsoft YaHei', 9)).pack(
                 padx=10, pady=10, side=LEFT)
        self.themeCombobox = self.add(combobox, self.rightFrame, width=10, value=[1, 2, 3, 4])
        self.themeCombobox.pack(pady=10, side=LEFT)

        self.panedwin.add(self.rightFrame)  # add table to Panedwindow


if __name__ == '__main__':
    window = MainPage('Title', geometry='1200x700')
    window.mainloop()
