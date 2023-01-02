# -*- encoding: utf-8 -*-
from abc import *
from minittk import *


class MyWindow(metaclass=ABCMeta):
    father_exists = False  # if father exists
    windowType = None

    def __new__(cls, *args, **kwargs) -> "MyWindow":
        """Determine type of window(father/toplevel)"""
        # To modify, must use MyWindow.xxx because children need
        # to share them in order to determine whether it is a root
        # or a toplevel
        if not MyWindow.father_exists:  # is father(1st time exec __new__())
            MyWindow.father_exists = True
            MyWindow.windowType = WINDOW
            return super(MyWindow, cls).__new__(cls)

        # If it is toplv, check whether var windowtype is TOPLEVEL
        if MyWindow.windowType is not TOPLEVEL:
            MyWindow.windowType = TOPLEVEL
        return super(MyWindow, cls).__new__(cls)

    def __init__(self, title=None, geometry='400x300', resizable=(True, True), position=None, theme='litera'):
        position = '' if not isinstance(position, Iterable) else f'+{position[0]}+{position[1]}'
        self._window = self.windowtype(themename=theme) if self.windowtype == ttk.Window else self.windowtype()
        self.window.title(title)
        self.window.geometry(geometry+position)
        self.window.resizable(*resizable)
        self._style = ttk.Style()

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, *args, **kwargs) -> None:
        self.mainloop()

    def add(self, wtype, parent=None, **kwargs):
        parent_ = parent.window if isinstance(parent, MyWindow) else parent
        parent_ = self.window if parent_ is None else parent_
        widget = WType[wtype](parent_, **kwargs)
        return widget

    def add_trview(self, columns, heads, height=None, parent=None) -> ttk.Treeview:
        trview = self.add(treeview, parent, column=columns[1:], height=height, bootstyle='primary')
        for i in range(len(columns)):
            trview.column(columns[i], anchor=CENTER)
            trview.heading(columns[i], text=heads[i])
        return trview

    def add_tabview(self, parent=None, **kwargs) -> Tableview:
        return self.add(tableview, parent, **kwargs)

    @property
    def windowtype(self):
        return self.__class__.windowType

    @property
    def window(self) -> ttk.Window | ttk.Toplevel:
        return self._window

    @property
    def style(self) -> ttk.Style:
        return self._style

    def theme_use(self, themename) -> ttk.Style:
        self.style.theme_use(themename)
        return self.style

    def mainloop(self) -> None:
        self.window.mainloop()
