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
        self.entryQueue = WidgetQueue()
        self.labelQueue = WidgetQueue()
        self.save_btn = self.add(button, text='保存配置', command=self.save_config).rpack(
                                 ipadx=5, anchor='nw', padx=5, pady=5)
        self.mysql_config().app_config()

    def save_config(self):
        if not all(getList := self.entryQueue.getList()):
            [i.configure(bootstyle=DANGER) for i in self.entryQueue if not i.get()]
            Messagebox.show_error(title='错误', message='请保证每个输入框均有value', parent=self.window)
            return

        [i.configure(bootstyle=DEFAULT) for i in self.entryQueue]
        labelVal = self.labelQueue.getLabelValue()
        t = 0
        for _ in range(5):
            self.cfgParser.set('MySQL', labelVal[t], getList[t])
            t += 1
        for _ in range(3):
            self.cfgParser.set('App', labelVal[t], getList[t])
            t += 1
        self.cfgParser.write(open(self.cfgParser.cfgfile, 'w'))
        Messagebox.show_info(title='Success', message='保存成功, 部分配置需要重启生效', parent=self.window)

    def grid(self, parent, dic: dict):
        row = 0
        for k, v in dic.items():
            label_ = self.add(label, parent, text=k).rgrid(column=0, row=row, pady=2, padx=45)
            self.labelQueue.enqueue(label_)
            input_ = self.add(entry, parent).rgrid(column=1, row=row, pady=2, padx=5)
            input_.insert(END, v)
            self.entryQueue.enqueue(input_)
            row += 1

    def mysql_config(self) -> "SettingPage":
        """MySQL Config Labelframe"""
        lFrame = self.add(labelframe, text='数据库配置', padding=5).rpack(fill=X, padx=5, side=TOP)
        self.grid(lFrame, self.cfgParser.getSectionItems('MySQL'))
        return self

    def app_config(self) -> "SettingPage":
        """App Config Labelframe"""
        lFrame = self.add(labelframe, text='软件配置', padding=5).rpack(fill=X, padx=5, pady=5, side=TOP)
        self.grid(lFrame, self.cfgParser.getSectionItems('App'))
        return self
