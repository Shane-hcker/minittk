# -*- encoding: utf-8 -*-
import asyncio
import threading

from minittk import *


class EventActions:
    def __init__(self, obj):
        self.obj = obj

    def databaseComboboxSelected(self, event):
        get_selected = self.obj.databaseCombobox.get()
        self.obj.selectionCombobox.values = [table for (table,) in self.obj.use(get_selected)]
        self.obj.selectionCombobox.clear()

        self.obj.database_label.value = get_selected
        if self.obj.database_label.value != self.obj.cfgParser.get('MySQL', 'database'):
            self.obj.saveDatabaseChange()
        self.obj.tree.delete_rows() if self.obj.tree.get_rows() else None

    def selectionComboboxSelected(self, event):
        self.obj.current_table = self.obj.selectionCombobox.get()
        self.obj.tree.delete_rows()

        if len(self.obj.describe(table_name=self.obj.current_table)) == 4:
            self.obj.tree.forInsert(4, self.obj.select(self.obj.current_table, '*'))
            self.obj.tree.load_table_data()
            return self.obj.uploadCheckbutton.set_state(NORMAL)

        self.obj.selectionCombobox.clear()
        self.obj.selectionCombobox.remove(self.obj.current_table)

        if not self.obj.isTableLengthOutOfRange:
            self.obj.isTableLengthOutOfRange = True
            Messagebox.show_error(title='Error', message='该表格行长度>4，无法显示')

    @staticmethod
    def themeComboboxSelected(self):
        def inner(event):
            self.curr_theme = self.themeCombobox.get() if self.themeCombobox.get() else 'litera'
            self.theme_use(self.curr_theme)
            self.themeCombobox.selection_clear()
        return inner
