# -*- encoding: utf-8 -*-
from minittk import *


class MyWindow:
    father_exist = False  # 父亲是否存在
    windowType = None

    def __new__(cls, *args, **kwargs) -> "MyWindow":
        """用于判断窗口类别(父/子)"""
        if not cls.father_exist:  # 是主窗口(第一次执行new)
            cls.father_exist = True
            cls.windowType = WINDOW
            return super(MyWindow, cls).__new__(cls)

        # 子窗口时，检查变量是否为Toplevel
        if cls.windowType is not TOPLEVEL:
            cls.windowType = TOPLEVEL

        return super(MyWindow, cls).__new__(cls)

    def __init__(self, title=None, geometry=None, resizable=None, position=None) -> None:
        """
        :param title: 窗口标题
        :param geometry: 窗口大小 XxY
        :param resizable: x,y轴可否调整大小(bool, bool)
        :param position: 窗口弹出位置 x, y
        """
        self.window_ = self.__class__.windowType()
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.resizable(True, True)

    def mainloop(self) -> None: self.window.mainloop()

    @property
    def window(self) -> ttk.Window | ttk.Toplevel: return self.window_

    @staticmethod
    def sql_run(): pass

    def add(self, *args, **kwargs):
        """
        :param args: args[0]=wtype, args[1]=parent
        :param kwargs: 组件参数
        :return: 返回组件对象
        """
        parent_ = self.window if args[1] is None else args[1].window
        widget = WType[args[0]](parent_, **kwargs)
        return widget
