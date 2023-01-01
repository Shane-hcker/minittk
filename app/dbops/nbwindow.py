# -*- encoding: utf-8 -*-
from minittk import *


class NotebookWindow(MyWindow):
    """
    Functions:
     - add_page()
     - add_pages()
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notebook = self.add(notebook)
        self.notebook.pack(expand=True, fill=BOTH, padx=10, pady=10)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mainloop()
        if exc_type is not None:
            raise exc_type()

    def add_page(self, header, **kwargs):
        """Add frame to notebook"""
        framepage = self.add(frame, self.notebook, **kwargs)
        self.notebook.add(framepage, text=header)
        return framepage

    def add_pages(self, *args, **kwargs):
        """add several pages to notebook"""
        return [self.add_page(i, **kwargs) for i in args]
