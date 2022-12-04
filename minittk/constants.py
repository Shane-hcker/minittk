# -*- encoding: utf-8 -*-
from ttkbootstrap.constants import *
import ttkbootstrap as ttk

# Vars
strvar = ttk.StringVar
intvar = ttk.IntVar
boolvar = ttk.BooleanVar

# Window
WINDOW = ttk.Window
TOPLEVEL = ttk.Toplevel

# TTK Widget Type
WType = {
    'Button': ttk.Button,
    'Combobox': ttk.Combobox,
    'Entry': ttk.Entry,
    'Label': ttk.Label,
    'ScrolledText': ttk.ScrolledText,
    'Frame': ttk.Frame,
    'Text': ttk.Text,
    'Treeview': ttk.Treeview,
    'Checkbutton': ttk.Checkbutton,
    'Radiobutton': ttk.Radiobutton,
}
