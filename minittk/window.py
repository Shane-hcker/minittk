# -*- encoding: utf-8 -*-
from minittk import *


class MyWindow:
    father_exists = False  # if father exists
    windowType = None

    def __new__(cls, *args, **kwargs) -> "MyWindow":
        """Determine type of window(father/toplevel)"""
        # ? To modify, must use MyWindow.xxx because children need
        # ? to share them in order to determine whether it is a root
        # ? or a toplevel
        if not MyWindow.father_exists:  # is father(1st time exec __new__())
            MyWindow.father_exists = True
            MyWindow.windowType = WINDOW
            return super(MyWindow, cls).__new__(cls)

        # If it is toplv, check whether var windowtype is TOPLEVEL
        if MyWindow.windowType is not TOPLEVEL:
            MyWindow.windowType = TOPLEVEL
        return super(MyWindow, cls).__new__(cls)

    def __init__(self, title=None, geometry=None, resizable=None, position=None, theme='litera') -> None:
        resizable_ = (True, True) if not isinstance(resizable, Iterable) else resizable
        position_ = '' if not isinstance(resizable, Iterable) else f'+{position[0]}+{position[1]}'
        geometry_ = '400x300' if not isinstance(geometry, str) else geometry
        self._window = self.windowtype(themename=theme) if self.windowtype == ttk.Window else self.windowtype()
        self.window.title(title)
        self.window.geometry(geometry_+position_)
        self.window.resizable(*resizable_)
        self._style = ttk.Style()

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mainloop()
        if exc_type is not None:
            raise exc_type()

    def add(self, wtype, parent=None, **kwargs):
        parent_ = parent.window if isinstance(parent, MyWindow) else parent
        parent_ = self.window if parent_ is None else parent_
        widget = WType[wtype](parent_, **kwargs)
        return widget

    def add_trview(self, columns, heads, height=None, parent=None):
        trview = self.add(treeview, parent, column=columns[1:], height=height, bootstyle='primary')
        for i in range(len(columns)):
            trview.column(columns[i], anchor=CENTER)
            trview.heading(columns[i], text=heads[i])
        return trview

    @property
    def windowtype(self): return self.__class__.windowType
    @property
    def window(self) -> ttk.Window | ttk.Toplevel: return self._window
    @property
    def style(self) -> ttk.Style: return self._style
    def theme_use(self, themename) -> None: self.style.theme_use(themename)
    def mainloop(self) -> None: self.window.mainloop()
