# -*- encoding: utf-8 -*-
from os.path import abspath, isfile
import configparser


class MyConfigParser(configparser.ConfigParser):
    _instance = None
    _init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyConfigParser, cls).__new__(cls)
        return cls._instance

    def __init__(self, cfgfile=None):
        if self.__class__._init_flag or not cfgfile:
            return

        if not isfile(cfgfile):
            raise FileNotFoundError(f'file {cfgfile} does not exist')

        print('going through MyConfigParser.__init__()')
        super().__init__()
        self.__class__._init_flag = True
        self.cfgfile = abspath(cfgfile)
        self.read(cfgfile, encoding='utf-8') if cfgfile is not None else ...

    @staticmethod
    def setupConfig(cfgfile=None):
        def inner(cls):
            cls.cfgParser = MyConfigParser(cfgfile=cfgfile)
            print(f'{cls} runned useconfig()')
            return cls
        return inner

    def commit(self) -> None: self.write(open(self.cfgfile, 'w'))

    def _set(self, section, option, value, autocommit) -> None:
        self.set(section, option, value)
        self.commit() if autocommit else None

    def writeAfterSet(self, *args, cnf=None, autocommit=True) -> None:
        """
        :param autocommit automatically commit after set()
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
            self._set(*args, autocommit=autocommit)
            return
        if not cnf:
            raise AttributeError('length of `cnf` needs to be >= 1')

        for dic in range(len(cnf)):
            self._set(**cnf[dic], autocommit=autocommit)

        self.commit() if autocommit else None

    def loadfromFile(self, cfgfile) -> None:
        self.__init__(cfgfile)

    def savefromDict(self, savefile) -> None:
        with open(savefile, 'w') as f:
            for section in self.sections():
                f.write(f'[{section}]\n')
                f.writelines([f'{k} = {v}\n' for k, v in self.items(section)])

    def getSectionItems(self, section) -> dict | None:
        if self.cfgfile is None:
            return

        if not self.has_section(section):
            raise ValueError(f'Section \'{section}\' does not exist')

        return {key: int(value) if key == 'port' else value for key, value in self.items(section)}
