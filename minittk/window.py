# -*- encoding: utf-8 -*-
from minittk import *


class Window:
    def __init__(self, title=None, geometry=None, resizable=None):
        self.window_ = ttk.Window()
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.resizable(resizable)

    @property
    def window(self):
        return self.window_

    @staticmethod
    def sql_run():
        pass

    def add(self, wtype: WType, **kwargs):
        wtype = eval(f'ttk.{wtype.value}')
        widget = wtype(self.window, **kwargs)
        widget.pack()
        return widget

    def mainloop(self): self.window.mainloop()
