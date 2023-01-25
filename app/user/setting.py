# -*- encoding: utf-8 -*-
from minittk import *


@MyConfigParser.useconfig(r'D:\minittk\app\user\config.ini')
class SettingPage(MyWindow):
    """功能:
    - config文件修改(MySQL, App)
    """
    def __init__(self):
        print(f'__init__(): {self}, id: {id(self)}')
        posX, posY = self.cfgParser.getint('App', 'startup.x'), self.cfgParser.getint('App', 'startup.y')
        super().__init__('Title', '450x400', (False, False), (posX+600, posY+20))
        self.entryQueue = self.labelQueue = WidgetQueue()
        self.save_btn = self.add(button, text='保存配置', command=self.save_config).rpack(
                                 ipadx=5, anchor='nw', padx=5, pady=5)
        self.mysql_config().app_config()

    def save_config(self):
        if not all(entryVal := self.entryQueue.getValue()):
            self.entryQueue.configureAll(lambda x: not x.get(), bootstyle=DANGER)
            return Messagebox.show_error(title='错误', message='请保证每个输入框均有value', parent=self.window)

        self.entryQueue.configureAll(bootstyle=DEFAULT)
        labelVal = self.labelQueue.getValue()
        t: Final = 5
        for _ in range(t):
            self.cfgParser.writeAfterSet('MySQL', labelVal[_], entryVal[_], autocommit=False)
        for _ in range(t, t+3):
            self.cfgParser.writeAfterSet('App', labelVal[_], entryVal[_], autocommit=False)
        self.cfgParser.commit()
        Messagebox.show_info(title='Success', message='保存成功, 部分配置需要重启生效', parent=self.window)

    def place(self, parent, dic: dict):
        for row, (k, v) in enumerate(dic.items()):
            label_ = self.add(label, parent, text=k).rgrid(column=0, row=row, pady=2, padx=45)
            self.labelQueue.enqueue(label_)

            input_ = self.add(entry, parent).rgrid(column=1, row=row, pady=2, padx=5)
            input_.set(v)
            self.entryQueue.enqueue(input_)

    def mysql_config(self) -> "SettingPage":
        """MySQL Config Labelframe"""
        lFrame = self.add(labelframe, style='text:数据库配置; padding:5').rpack(fill=X, padx=5, side=TOP)
        self.place(lFrame, self.cfgParser.getSectionItems('MySQL'))
        return self

    def app_config(self) -> "SettingPage":
        """App Config Labelframe"""
        lFrame = self.add(labelframe, style='text:软件配置; padding:5').rpack(fill=X, padx=5, pady=5, side=TOP)
        self.place(lFrame, self.cfgParser.getSectionItems('App'))
        return self
