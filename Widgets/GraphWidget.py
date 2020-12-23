import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class MyGraphWidget(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)
        self.figure = Figure()
        self.subplots = []
        # Espace de dessin
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # Espace de control
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.get_tk_widget().place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
        self.draw()

    def add_subplot(self, *args: int, **kwargs):
        self.subplots.append(self.figure.add_subplot(*args, *kwargs))
        self.draw()
        return self.subplots[-1]

    def plot(self, x, y, idx: int = -1, **kwargs):
        self.subplots[idx].plot(x, y, **kwargs)
        self.draw()

    def draw(self):
        self.canvas.draw()
        self.toolbar.update()
