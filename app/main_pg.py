# -*- encoding: utf-8 -*-
from minittk import *


class MainPage(MyWindow):
    def __init__(self, title, geometry):
        resize = (True, True)
        position = (700, 300)
        super().__init__(title, geometry, resize, position)

        self.add('Label', text='选择数据源', font=('Microsoft YaHei', 12))
        self.add('Combobox', textvariable=strvar(), values=[1, 2, 3])


if __name__ == '__main__':
    window = MainPage('Title', geometry='400x420')
    window.mainloop()
