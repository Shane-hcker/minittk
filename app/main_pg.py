# -*- encoding: utf-8 -*-
from minittk import *


class MainPage(MyWindow):
    def __init__(self, title, geometry):
        resize = (True, True)
        position = (450, 200)
        super().__init__(title, geometry, resize, position)
        self.widgetqueue = WidgetQueue()
        self.sidebar()

    def sidebar(self):
        """左侧边栏"""
        # PanedWindow
        pw = self.add(panedwindow, orient=HORIZONTAL, bootstyle='info')
        pw.pack(fill=BOTH, expand=True)

        # LabelFrame
        lFrame = self.add(labelframe, text='数据库表格', padding=10)
        lFrame.pack(fill=BOTH, padx=50, pady=50, anchor='center')

        # 添加LabelFrame上的组件
        self.add(combobox, lFrame, value=[1, 2, 3, 4], width=25).grid(
                 column=0, row=0, columnspan=5, pady=5, ipady=5)

        feat = ['创建', '复制', '迁移', '导出', '导入', '不到']
        t = 0
        for i in range(1, 4):
            for j in range(1, 3):
                self.add(button, lFrame, text=feat[t]).grid(column=i, row=j, ipadx=5, ipady=2, padx=2, pady=2)
                t += 1

        pw.add(lFrame)
        pw.add(self.add(label, text='dsadasdsadassadasd'))


if __name__ == '__main__':
    window = MainPage('Title', geometry='1200x700')
    window.mainloop()
