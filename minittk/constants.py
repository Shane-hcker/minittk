# -*- encoding: utf-8 -*-
from ttkbootstrap.constants import *
from collections import defaultdict
import ttkbootstrap as ttk
from .widgets import *


# PyMySQL fetch methods
ONE = 'one'
ALL = 'all'

# Focuses
FOCUS = 'focus'
FOCUSIN = 'focusin'
FOCUSOUT = 'focusout'

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
