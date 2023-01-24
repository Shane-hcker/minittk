# -*- encoding: utf-8 -*-
from minittk import *


class MyWindow:
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

    def __enter__(self) -> "MyWindow":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mainloop()
        if exc_type is not None:
            raise exc_type()

    def __call__(self, *args, **kwargs) -> None:
        self.mainloop()

    def add(self, wtype, parent=None, **kwargs):
        parent_ = parent.window if isinstance(parent, MyWindow) else parent
        parent_ = self.window if parent_ is None else parent_

        if not (wstyle := kwargs.get('style', None)):
            return wtype(parent_, **kwargs)

        parsed_style = self.__parse(wstyle)
        kwargs.pop('style')
        return wtype(parent_, **kwargs, **parsed_style)

    def add_trview(self, parent=None, *, columns, heads, height=None) -> ttk.Treeview:
        trview = self.add(treeview, parent, column=columns[1:], height=height, bootstyle='primary')
        for i in range(len(columns)):
            trview.column(columns[i], anchor=CENTER)
            trview.heading(columns[i], text=heads[i])
        return trview

    def __parse(self, styles: str) -> dict:
        """
        example:
        initial: w:25; h:250; state:disabled; style:SUCCESS;
        after parsing: {"width": 25, "height": 50, 'state': "Disabled", "style": "SUCCESS"}
        fixme lambda: 分号解决
        """
        options = {}
        styles = [item.strip() for item in styles.split(';')]
        for style in [_.replace(':', ': ').replace(' ', '') for _ in styles]:
            if 'w:' in style:
                self.str2dict(options, style.replace('w', '\'width\''))
            elif 'h:' in style:
                self.str2dict(options, style.replace('h', '\'height\''))
            elif not (other := style.split(':'))[-1].isdigit() and 'command:' not in style:
                self.str2dict(options, f'\'{other[0]}\':\'{other[-1]}\'')
            else:
                self.str2dict(options, f'\'{other[0]}\':{other[-1]}')
        return options

    @staticmethod
    def str2dict(dic: dict, string: str) -> dict:
        dic.update(eval(f"{{{string}}}"))
        return dic

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
        if themename not in self.style.theme_names():
            return self.style
        self.style.theme_use(themename)
        return self.style

    def mainloop(self) -> None:
        self.window.mainloop()
