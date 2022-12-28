# -*- encoding: utf-8 -*-
from minittk import *


class SettingPage(MyWindow):
    """功能:
    - config文件修改(MySQL, App)
    """
    def __init__(self):
        self.cfgParser = MyConfigParser('./config.ini')
        posX, posY = self.cfgParser.getint('App', 'startupX'), self.cfgParser.getint('App', 'startupY')
        super().__init__('Title', '450x350', (False, False), (posX+600, posY+20))
        self.add(button, command=self.save_config,
                 text='保存配置').pack(ipadx=5, anchor='nw', padx=5, pady=5)
        self.mysql_config()
        self.app_config()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mainloop()
        if exc_type is not None:
            raise exc_type()

    def mysql_config(self):
        """MySQL Config Labelframe"""
        lFrame = self.add(labelframe, text='数据库配置', padding=5)
        lFrame.pack(fill=X, padx=5, side=TOP)
        addon = partial(self.add, parent=lFrame)
        if not self.cfgParser.has_section('MySQL'):
            raise LookupError('Cannot not find section MySQL')
        mysql_dic = self.cfgParser.getSectionItems('MySQL')
        row = column = 0
        for k, v in mysql_dic.items():
            addon(label, text=k.capitalize()).grid(column=0, row=row, pady=2, padx=45)
            addon(entry, show=None).grid(column=1, row=row, pady=2, padx=5)
            row += 1

    def app_config(self):
        """App Config Labelframe"""
        pass

    def save_config(self):
        pass


if __name__ == '__main__':
    with SettingPage() as window:
        pass
