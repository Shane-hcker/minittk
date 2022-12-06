# -*- encoding: utf-8 -*-
from minittk import *


class WidgetQueue(list):
    def __init__(self, *args):
        super().__init__()
        for _ in args:
            self.enqueue(_)

    def pack_one(self, index, **kwargs):
        if not isinstance(self[index], Widget):
            raise AttributeError('Element has to be type \'ttk.Widget\'')
        self[index].pack(**kwargs)

    def pack_all(self, **kwargs):
        for i in self:
            if not isinstance(self[i], Widget):
                raise AttributeError('Element has to be type \'ttk.Widget\'')
            i.pack(**kwargs)

    @property
    def empty(self): return len(self) == 0
    def enqueue(self, item): self.append(item)
    def dequeue(self): self.pop(0)
