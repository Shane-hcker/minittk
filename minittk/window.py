# -*- encoding: utf-8 -*-
from minittk import *


class MyWindow:
    father_exists = False  # 父亲是否存在
    windowType = None

    def __new__(cls, *args, **kwargs) -> "MyWindow":
        """用于判断窗口类别(父/子)"""
        if not cls.father_exists:  # 是主窗口(第一次执行new)
            cls.father_exists = True
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
        :param position: 窗口弹出位置 (x, y)
        """
        resizable_ = (True, True) if not isinstance(resizable, Iterable) else resizable
        position_ = '' if not isinstance(resizable, Iterable) else f'+{position[0]}+{position[1]}'

        self.window_ = self.__class__.windowType()
        self.window.title(title)
        self.window.geometry(geometry+position_)
        self.window.resizable(*resizable_)

    def mainloop(self) -> None:
        self.window.mainloop()

    @property
    def window(self) -> ttk.Window | ttk.Toplevel:
        return self.window_

    @staticmethod
    def sql_run(): pass

    def add(self, wtype, parent=None, **kwargs):
        """
        :param wtype 组件 String
        :param parent 依附对象
        :param kwargs: 组件参数
        :return: 返回组件对象
        """
        parent_ = self.window if parent is None else parent.window
        widget = WType[wtype](parent_, **kwargs)
        return widget
