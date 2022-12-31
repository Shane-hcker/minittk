# -*- encoding: utf-8 -*-
from ttkbootstrap import Label


class WidgetQueue(list):
    def __init__(self, *args):
        super().__init__()
        for _ in args:
            self.enqueue(_)

    def getList(self) -> list:
        """returns a list of widget.get() method results"""
        try:
            return [i.get() for i in self]
        except Exception:  # if a widget cannot be gotten
            raise Exception()  # raise Error

    def getLabelValue(self) -> list:
        """returns the `text` attribute of a group of labels"""
        try:
            return [i['text'] for i in self if isinstance(i, Label)]
        except Exception:
            raise Exception()

    @property
    def empty(self):
        return not self

    def enqueue(self, item):
        self.append(item)
        return item

    def dequeue(self):
        return self.pop(0)
