# -*- encoding: utf-8 -*-
from os.path import abspath
import configparser


class MyConfigParser(configparser.ConfigParser):
    _instance = None
    _init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyConfigParser, cls).__new__(cls)
        return cls._instance

    def __init__(self, cfgfile=None):
        if not cfgfile:
            return

        if self.__class__._init_flag:
            return
        print('going through MyConfigParser.__init__()')
        super().__init__()
        self.__class__._init_flag = True
        self.cfgfile = abspath(cfgfile)
        self.read(cfgfile, encoding='utf-8') if cfgfile is not None else ...

    def commit(self):
        self.write(open(self.cfgfile, 'w'))
        return self

    @staticmethod
    def useconfig(cfgfile=None):
        def inner(cls):
            cls.cfgParser = MyConfigParser(cfgfile=cfgfile)
            print(f'{cls} runned useconfig()')
            return cls
        return inner

    def writeAfterSet(self, *args, cnf=None):
        """
        :param cnf: [
            {
                "section": section,
                "option": option,
                "value": value,
            },
            ...
        ]
        """
        if args:
            self.set(*args)
            self.commit()
            return

        if not cnf:
            raise AttributeError('length of `cnf` needs to be >= 1')

        # cnf=list
        if (cnf_length := len(cnf)) == 1:
            section, option, value = cnf[0]
            self.set(section, option, value)
            self.commit()
            return

        for dic in range(cnf_length):
            section, option, value = cnf[dic]
            self.set(section, option, value)

        self.commit()

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

        return {key: int(value) if key == 'port' else value for key, value in self.items(section)}
