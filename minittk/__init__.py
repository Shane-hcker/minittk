# -*- encoding: utf-8 -*-
from typing import *
from functools import partial
# import pymysql
import asyncio
import aiomysql
# from pymysql.cursors import Cursor
import ttkbootstrap as ttk
from ttkbootstrap.tableview import TableRow
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.localization.msgcat import MessageCatalog
from ttkbootstrap.dialogs.dialogs import Messagebox, Querybox
from ttkbootstrap.tooltip import ToolTip
import tkinter.filedialog as filedialog
from tkinter import TclError


from minittk.widgetqueue import WidgetQueue
from minittk.constants import *
from minittk.window import MyWindow
from minittk.widgets import *
from minittk.support.sqlsender import SQLSender
from minittk.support.sqlhandler import SQLHandler
from minittk.support.cfgparser import MyConfigParser
from minittk.support.uiautomation import UIAutomation


config_file = r'D:\minittk\app\user\config.ini'
