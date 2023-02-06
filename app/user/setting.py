# -*- encoding: utf-8 -*-
from minittk import *


@MyConfigParser.setupConfig(r'D:\minittk\app\user\config.ini')
class SettingPage(MyWindow):
    """功能:
    - config文件修改(MySQL, App)
    """

    def __init__(self):
        print(f'__init__(): {self}, id: {id(self)}')
        posX, posY = self.cfgParser.getint('App', 'startup.x'), self.cfgParser.getint('App', 'startup.y')
        super().__init__('Title', '450x400', (False, False), (posX + 600, posY + 20))

        self.entryValueDict = {}  # Entry: original text
        self.entryBooleanDict = {}  # Entry: boolean(saved)
        self.configSaved = True
        self.focusEntry = None
        self.entryQueue = WidgetQueue[Entry]()
        self.labelQueue = WidgetQueue[Label]()

        self.save_btn = self.add(button, text='保存配置', command=self.save_config)
        self.save_btn.pack(ipadx=5, anchor='nw', padx=5, pady=5)
        self.mysql_config().app_config()

        self.entryQueue.bindAll('<FocusIn>', self.entry_focusIn, filter_=None)
        self.entryQueue.bindAll('<FocusOut>', self.entry_focusOut, filter_=None)
        self.protocol('WM_DELETE_WINDOW', self.release)

    def save_config(self):
        """save config action"""
        if self.configSaved:
            return

        if not all(entryVal := self.entryQueue.getValue()):
            self.entryQueue.configureAll(lambda x: not x.get(), bootstyle=DANGER)
            return Messagebox.show_error(title='错误', message='请保证每个输入框均有value', parent=self.window)

        self.entryQueue.configureAll(bootstyle=DEFAULT)
        labelVal = self.labelQueue.getValue()
        t: Final = 5
        for _ in range(t):
            self.cfgParser.writeAfterSet('MySQL', labelVal[_], entryVal[_], autocommit=False)
        for _ in range(t, t + 3):
            self.cfgParser.writeAfterSet('App', labelVal[_], entryVal[_], autocommit=False)

        self.cfgParser.commit()
        self.configSaved = True
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

    def entry_focusOut(self, event):
        if not self.focusEntry.get() == self.entryValueDict[self.focusEntry]:
            self.entryBooleanDict[self.focusEntry] = False  # not saved
            self.configSaved = False
            return

        self.entryBooleanDict[self.focusEntry] = True
        if all(self.entryBooleanDict.values()):
            self.configSaved = True

    def entry_focusIn(self, event):
        self.focusEntry = self.window.focus_get()
        if not self.entryValueDict.get(self.focusEntry) and self.entryBooleanDict.get(self.focusEntry) is None:
            self.entryValueDict[self.focusEntry] = self.focusEntry.get()  # init: original text
            self.entryBooleanDict[self.focusEntry] = True  # init: saved

    def release(self) -> None:
        if (self.configSaved or
                Messagebox.yesno('还没保存 确认退出?', 'Title', parent=self.window) == MessageCatalog.translate(
                    '确认')):
            self.entryQueue.release()
            self.labelQueue.release()
            self.destroy()
