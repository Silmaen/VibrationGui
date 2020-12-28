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
        self.figure.tight_layout()
        # Espace de dessin
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # Espace de control
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        #self.canvas.get_tk_widget().place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #self.draw()

    def draw(self):
        """
        Actualisation de la zone de dessin
        """
        self.figure.show()
        ## self.canvas.draw()
        ## self.toolbar.update()

    def replot_three_graph(self, t, x, y, z):
        """

        :param t: Axe des abscisses
        :param x: Première courbe
        :param y: Seconde courbe
        :param z: Troisième courbe
        """
        #self.subplot.clear()
        self.subplot.set_title("Time Domain Signal")
        self.subplot.set_xlabel("Time")
        self.subplot.set_ylabel("Amplitude")
        self.subplot.plot(t, x, label="ax")
        self.subplot.plot(t, y, label="ay")
        self.subplot.plot(t, z, label="az")
        self.draw()
