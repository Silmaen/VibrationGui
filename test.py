#! /usr/bin/env python
# encoding: utf8
"""
Autre module principal ayant pour fonction de faire des tests
"""
import tkinter as tk
import tkinter.ttk as ttk
from GraphWidget import MyGraphWidget
import numpy as np


t = np.arange(0, 10, .01)
x = 2 * np.sin(2 * np.pi * t * np.random.rand())


class TestFrame(ttk.Frame):
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.figure = MyGraphWidget(self)
        self.figure.grid()
        self.btn = ttk.Button(self, command=self.redraw)
        self.btn.grid()

    def redraw(self):
        x = 2 * np.sin(2 * np.pi * t * np.random.rand())
        self.figure.replot_one_graph(t, x)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Analyse de vibration")
    root.geometry("800x600")
    w = TestFrame(master=root)
    w.pack(expand=True, fill='both')
    root.mainloop()
