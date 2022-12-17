# -*- encoding: utf-8 -*-
from os.path import abspath
from minittk import *


class DefaultConfigParser(configparser.ConfigParser):
    def __init__(self, cfgfile=None):
        super().__init__()
        self.cfgfile = cfgfile
        if self.cfgfile is None:
            return
        self.read(self.cfgfile, encoding='utf-8')

    def get_mysql(self, section=None):
        if not self.has_section(sectionName := section if isinstance(section, str) else 'MySQL'):
            raise ValueError(f'Section \'{sectionName}\' does not exist in file \'{abspath(self.cfgfile)}\'')

        return {i[0]: i[1] for i in self.items(sectionName)}

    def load_from_ini(self, cfgfile): self.__init__(cfgfile)

    def ini_from_dict(self, savefile):
        with open(savefile, 'w') as f:
            for i in self.sections():
                f.write(f'[{i}]\n')
                f.writelines([f'{j} = {k}\n' for j, k in self.items(i)])
