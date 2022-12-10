# -*- encoding: utf-8 -*-
from ttkbootstrap.constants import *
from collections import defaultdict
import ttkbootstrap as ttk

from minittk import *

# Vars
strvar = ttk.StringVar
intvar = ttk.IntVar
boolvar = ttk.BooleanVar

# Window
WINDOW = ttk.Window
TOPLEVEL = ttk.Toplevel

# Widget Variables
button = 'button'
combobox = 'combobox'
entry = 'entry'
label = 'label'
scrolledtext = 'scrolledtext'
frame = 'frame'
text = 'text'
treeview = 'treeview'
checkbutton = 'checkbutton'
radiobutton = 'radiobutton'
panedwindow = 'panedwindow'
labelframe = 'labelframe'

# TTK Widget Type
WType = defaultdict(lambda: ttk.Label, {
    'button': ttk.Button,
    'combobox': ttk.Combobox,
    'entry': ttk.Entry,
    'label': ttk.Label,
    'scrolledtext': ttk.ScrolledText,
    'frame': ttk.Frame,
    'text': ttk.Text,
    'treeview': ttk.Treeview,
    'checkbutton': ttk.Checkbutton,
    'radiobutton': ttk.Radiobutton,
    'panedwindow': ttk.PanedWindow,
    'labelframe': ttk.Labelframe,
})
