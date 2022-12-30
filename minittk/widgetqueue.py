# -*- encoding: utf-8 -*-
class WidgetQueue(list):
    def __init__(self, *args):
        super().__init__()
        for _ in args:
            self.enqueue(_)

    def getList(self):
        """returns a list of widget.get() method results"""
        try:
            return [i.get() for i in self]
        except Exception:  # if a widget cannot be gotten
            raise Exception()  # raise Error

    @property
    def empty(self):
        return not self

    def enqueue(self, item):
        self.append(item)
        return item

    def dequeue(self):
        return self.pop(0)
