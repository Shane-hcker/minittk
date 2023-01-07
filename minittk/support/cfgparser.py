# -*- encodingss: utf-8 -*-
import configparser


class MyConfigParser(configparser.ConfigParser):
    _instance = None
    _init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyConfigParser, cls).__new__(cls)
        return cls._instance

    def __init__(self, cfgfile=None):
        if self.__class__._init_flag:
            return
        super().__init__()
        self.__class__._init_flag = True
        self.cfgfile = cfgfile
        self.read(cfgfile, encoding='utf-8') if cfgfile is not None else ...

    @staticmethod
    def useconfig(cfgfile=None):
        def inner(cls):
            cls.cfgParser = MyConfigParser(cfgfile=cfgfile)
            print(f'{cls} runned useconfig()')
            return cls
        return inner

    def loadfromFile(self, cfgfile) -> None:
        self.__init__(cfgfile)

    def savefromDict(self, savefile) -> None:
        with open(savefile, 'w') as f:
            for i in self.sections():
                f.write(f'[{i}]\n')
                f.writelines([f'{j} = {k}\n' for j, k in self.items(i)])

    def getSectionItems(self, section) -> dict | None:
        if self.cfgfile is None:
            return
        if not self.has_section(section):
            raise ValueError(f'Section \'{section}\' does not exist')
        return {i[0]: int(i[1]) if i[0] == 'port' else i[1] for i in self.items(section)}
