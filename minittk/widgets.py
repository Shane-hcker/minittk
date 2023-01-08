# -*- encoding: utf-8 -*-
from typing import *
from ttkbootstrap.tableview import Tableview as ttkTableView
import ttkbootstrap as ttk
import tkinter.ttk


__all__ = ['Button', 'Combobox', 'Entry', 'Label', 'ScrolledText', 'Frame',
           'Text', 'Treeview', 'Checkbutton', 'Radiobutton', 'Panedwindow', 'Labelframe',
           'Notebook', 'Tableview', 'Separator']


class MyWidget(tkinter.ttk.Widget):
    def rpack(self, *args, **kwargs):
        """returned pack"""
        self.pack(*args, **kwargs)
        return self

    def rgrid(self, *args, **kwargs):
        self.grid(*args, **kwargs)
        return self

    def rplace(self, *args, **kwargs):
        """returned place"""
        self.place(*args, **kwargs)
        return self

    def rbind(self, *args, **kwargs):
        """returned bind"""
        self.bind(*args, **kwargs)
        return self


class Button(MyWidget, ttk.Button):
    pass


class Separator(MyWidget, ttk.Separator):
    pass


class Combobox(MyWidget, ttk.Combobox):
    @property
    def values(self): return self['values']

    @values.setter
    def values(self, values: List[Any]):
        self['values'] = values


class Entry(MyWidget, ttk.Entry):
    @property
    def value(self): return self.get()


class Label(MyWidget, ttk.Label):
    @property
    def value(self): return self['text']

    @value.setter
    def value(self, text): self['text'] = text


class ScrolledText(MyWidget, ttk.ScrolledText):
    pass


class Frame(MyWidget, ttk.Frame):
    pass


class Text(MyWidget, ttk.Text):
    pass


class Treeview(MyWidget, ttk.Treeview):
    pass


class Checkbutton(MyWidget, ttk.Checkbutton):
    pass


class Radiobutton(MyWidget, ttk.Radiobutton):
    pass


class Panedwindow(MyWidget, ttk.Panedwindow):
    pass


class Labelframe(MyWidget, ttk.Labelframe):
    pass


class Notebook(MyWidget, ttk.Notebook):
    pass


class Tableview(MyWidget, ttkTableView):
    pass
