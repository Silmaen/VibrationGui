# encoding: utf8
"""
Module de définition d'un widget intégrant tout ce qu'il faut pour tracer des graph dans Tk
"""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

class MyGraphWidget(tk.Frame):
    """
    Widget de dessin d'un graph
    """
    def __init__(self, master=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)
        self.figure = Figure()
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_title("Time Domain Signal")
        self.subplot.set_xlabel("Time")
        self.subplot.set_ylabel("Amplitude")
        # Espace de dessin
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # Espace de control
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def draw(self):
        """
        Actualisation de la zone de dessin
        """
        self.canvas.draw()

    def replot_three_graph(self, t, x, y, z):
        """

        :param t: Axe des abscisses
        :param x: Première courbe
        :param y: Seconde courbe
        :param z: Troisième courbe
        """
        self.subplot.clear()
        self.subplot.set_title("Time Domain Signal")
        self.subplot.set_xlabel("Time")
        self.subplot.set_ylabel("Amplitude")
        print(np.size(t), np.size(x))
        self.subplot.plot(t, x, label="ax")
        self.subplot.plot(t, y, label="ay")
        self.subplot.plot(t, z, label="az")
        self.draw()

    def replot_one_graph(self, t, x):
        """

        :param t: Axe des abscisses
        :param x:  courbe
        """
        self.subplot.clear()
        self.subplot.set_title("Time Domain Signal")
        self.subplot.set_xlabel("Time")
        self.subplot.set_ylabel("Amplitude")
        print(np.size(t), np.size(x))
        self.subplot.plot(t, x, label="ax")
        self.draw()
