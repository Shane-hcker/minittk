# -*- encoding: utf-8 -*-
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from typing import *
from .widgets import *


# PyMySQL fetch methods
ONE: Final = 'one'
ALL: Final = 'all'
MANY: Final = 'many'

# Focuses
FOCUS: Final = 'focus'
FOCUSIN: Final = 'focusin'
FOCUSOUT: Final = 'focusout'

# Vars
strvar = ttk.StringVar
intvar = ttk.IntVar
boolvar = ttk.BooleanVar

# Window
WINDOW = ttk.Window
TOPLEVEL = ttk.Toplevel

# Widget Variables
button = Button
combobox = Combobox
entry = Entry
label = Label
scrolledtext = ScrolledText
frame = Frame
text = Text
treeview = Treeview
checkbutton = Checkbutton
radiobutton = Radiobutton
panedwindow = Panedwindow
labelframe = Labelframe
tableview = Tableview
notebook = Notebook
separator = Separator
menu = Menu
