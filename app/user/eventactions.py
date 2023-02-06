# -*- encoding: utf-8 -*-
from minittk import *


class EventActions:
    @staticmethod
    def databaseComboboxSelected(self):
        def inner(event):
            get_selected = self.databaseCombobox.get()
            self.selectionCombobox.values = [table for (table,) in self.use(get_selected)]
            self.selectionCombobox.clear()

            self.database_label.value = get_selected
            self.saveDatabaseChange() if self.database_label.value != self.cfgParser.get('MySQL', 'database') else None
            self.tree.delete_rows() if self.tree.get_rows() else None
        return inner

    @staticmethod
    def selectionComboboxSelected(self):
        def inner(event):
            self.current_table = self.selectionCombobox.get()
            self.tree.delete_rows()

            if len(self.describe(table_name=self.current_table)) == 4:
                self.tree.forInsert(4, self.select(self.current_table, '*'))
                self.tree.load_table_data()
                return self.uploadCheckbutton.set_state(NORMAL)

            self.selectionCombobox.clear()
            self.selectionCombobox.remove(self.current_table)

            if not self.isTableLengthOutOfRange:
                self.isTableLengthOutOfRange = True
                Messagebox.show_error(title='Error', message='该表格行长度>4，无法显示')
        return inner

    @staticmethod
    def themeComboboxSelected(self):
        def inner(event):
            self.curr_theme = self.themeCombobox.get() if self.themeCombobox.get() else 'litera'
            self.theme_use(self.curr_theme)
            self.themeCombobox.selection_clear()
        return inner
