# -*- encoding: utf-8 -*-
from minittk import *


class MyWindow:
    father_exists = False  # if father exists
    windowType = None

    def __new__(cls, *args, **kwargs) -> "MyWindow":
        """Determine type of window(father/toplevel)"""
        if not cls.father_exists:  # is father(1st time exec __new__())
            cls.father_exists = True
            cls.windowType = WINDOW
            return super(MyWindow, cls).__new__(cls)

        # If it is toplv, check whether var windowtype is TOPLEVEL
        if cls.windowType is not TOPLEVEL:
            cls.windowType = TOPLEVEL

        return super(MyWindow, cls).__new__(cls)

    def __init__(self, title=None, geometry=None, resizable=None, position=None, theme='litera') -> None:
        resizable_ = (True, True) if not isinstance(resizable, Iterable) else resizable
        position_ = '' if not isinstance(resizable, Iterable) else f'+{position[0]}+{position[1]}'
        self.window_ = self.__class__.windowType(themename=theme)
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

    def add_trview(self, columns, heads, height=None, parent=None):
        trview = self.add(treeview, parent, column=columns[1:], height=height, bootstyle='primary')
        for i in range(len(columns)):
            trview.column(columns[i], anchor=CENTER)
            trview.heading(columns[i], text=heads[i])
        return trview

    def add(self, wtype, parent=None, **kwargs):
        """
        :param wtype: Widget String
        :param parent: Attached Object(Father)
        :param kwargs: Widget Kw arguments
        :return: return: Widget Obj
        """
        if isinstance(parent, MyWindow):
            parent_ = parent.window
        else:
            parent_ = parent

        parent_ = self.window if parent_ is None else parent_
        widget = WType[wtype](parent_, **kwargs)
        return widget
