# -*- encoding: utf-8 -*-
from ttkbootstrap.constants import *
from enum import unique, Enum


# TTK Widget Type
@unique
class WType(Enum):
    BUTTON = 'Button'
    COMBOBOX = "Combobox"
    ENTRY = "Entry"
    LABEL = "Label"
    SCROLLEDTEXT = 'ScrolledText'
    FRAME = 'Frame'
    TEXT = 'Text'
    TREEVIEW = 'Treeview'
    CHECKBUTTON = 'Checkbutton'
    RADIOBUTTON = 'Radiobutton'
