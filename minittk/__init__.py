# -*- encoding: utf-8 -*-
from configparser import ConfigParser
from functools import partial
import ttkbootstrap as ttk
from typing import *
import pymysql

from minittk.support.mymysql import MySQLMixIn
from .widgetqueue import WidgetQueue
from .constants import *
from .window import *
