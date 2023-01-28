# -*- encoding: utf-8 -*-
from types import FunctionType, LambdaType


class WidgetQueue(list):
    def __init__(self, *args):
        super().__init__()
        for item in args:
            self.enqueue(item)

    def release(self):
        for _ in self:
            self.dequeue()

    def getValue(self) -> list:
        """returns a list of widget.get() method results"""
        return [i.get() for i in self]

    def configure(self, index, **kwargs):
        self[index].configure(**kwargs)

    def bind(self, index, *args, **kwargs):
        self[index].bind(*args, **kwargs)

    def configureAll(self, filter_=None, **kwargs):
        """
        :param filter_: function that has an argument, for filtering items
        example: lambda x: ...
        :param kwargs: kw of configure()
        """
        if not filter_:
            for item in self:
                item.configure(**kwargs)
            return

        for item in self:
            if not filter_(item):
                continue
            item.configure(**kwargs)

    def bindAll(self, filter_=None, *args, **kwargs):
        if not filter_:
            for item in self:
                item.bind(*args, **kwargs)
            return

        for item in self:
            if not filter_(item):
                continue
            item.bind(*args, **kwargs)

    @property
    def empty(self):
        return not self

    def enqueue(self, item):
        self.append(item)
        return item

    def dequeue(self):
        return self.pop(0)
