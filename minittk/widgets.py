# -*- encoding: utf-8 -*-
from typing import *
from ttkbootstrap.tableview import Tableview as ttkTableView
import ttkbootstrap as ttk
import tkinter.ttk


__all__ = ['MyWidget', 'Button', 'Combobox', 'Entry', 'Label', 'ScrolledText',
           'Text', 'Treeview', 'Checkbutton', 'Radiobutton', 'Panedwindow', 'Labelframe',
           'Notebook', 'Tableview', 'Separator', 'Menu', 'Frame']


class MyWidget(tkinter.ttk.Widget):
    def set_state(self, state):
        self['state'] = state

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

    def rfocus_set(self):
        self.focus_set()
        return self


class Button(MyWidget, ttk.Button):
    pass


class Separator(MyWidget, ttk.Separator):
    pass


class Combobox(MyWidget, ttk.Combobox):
    def remove(self, target_value) -> None:
        if not self.values:
            raise IndexError("Empty combobox list")

        original = list(self.values)
        try:
            original.remove(target_value)
            self.values = original
        except IndexError:
            raise IndexError(f'{target_value} does not exist in current combobox list')

    @property
    def values(self):
        return self['values']

    @values.setter
    def values(self, values: Iterable[Any]):
        self['values'] = values

    def clear(self):
        self.set('')

    def dbind(self, *args, **kwargs):
        self.bind("<<ComboboxSelected>>", *args, **kwargs)

    def rbind(self, *args, **kwargs):
        super().rbind('<<ComboboxSelected>>', *args, **kwargs)


class Entry(MyWidget, ttk.Entry):
    @property
    def value(self):
        return self.get()


class Label(MyWidget, ttk.Label):
    @property
    def value(self):
        return self['text']

    @value.setter
    def value(self, text):
        self['text'] = text


class Menu(ttk.Menu):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

    def post_event(self, event):
        self.post(event.x_root, event.y_root)


class Tableview(MyWidget, ttkTableView):
    def forInsert(self, iterable, length):
        """
        :param iterable: [[...], ...]
        :param length: length of iterable[index]
        """
        inserted_value = '['
        for _ in range(length):
            inserted_value += f'item[{_}], '
        inserted_value.strip(', ')
        inserted_value += ']'

        for item in iterable:
            self.insert_row(values=eval(inserted_value))

    def get_selected_row(self):
        # focus() & selection() => iid
        print(self.view.focus())
        return self.view.set(self.view.focus())

    def get_selected_row_iid(self):
        return self.view.focus()


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
