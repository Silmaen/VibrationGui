# encoding: utf8
"""
Module de définition d'un widget intégrant tout ce qu'il faut pour tracer des graph dans Tk
"""
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class MyGraphWidget(ttk.Frame):
    """
    Widget de dessin d'un graph
    """
    def __init__(self, master=None,  **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.graph_title = "Time Domain Signal"
        self.graph_x_label = "Time"
        self.graph_y_label = "Amplitude"
        self.configure(**kw)
        self.figure = Figure()
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_title(self.graph_title)
        self.subplot.set_xlabel(self.graph_x_label)
        self.subplot.set_ylabel(self.graph_y_label)
        # Espace de dessin
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # Espace de control
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def configure(self, cnf=None, **kw):
        """
        Fonction de configuration (Setter General)
        """
        key = 'graph_title'
        if key in kw:
            self.graph_title = kw[key]
            self.subplot.set_title(self.graph_title)
            del kw[key]
        key = 'graph_x_label'
        if key in kw:
            self.graph_x_label = kw[key]
            self.subplot.set_xlabel(self.graph_x_label)
            del kw[key]
        key = 'graph_y_label'
        if key in kw:
            self.graph_y_label = kw[key]
            self.subplot.set_ylabel(self.graph_y_label)
            del kw[key]
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def cget(self, key):
        """
        Getter general
        :param key: nom de la variable demandée
        :return: sa valeur
        """
        option = 'graph_title'
        if key == option:
            return self.graph_title
        option = 'graph_x_label'
        if key == option:
            return self.graph_x_label
        option = 'graph_y_label'
        if key == option:
            return self.graph_y_label
        return ttk.Frame.cget(self, key)

    def draw(self):
        """
        Actualisation de la zone de dessin
        """
        self.canvas.draw()

    def plot_graphs(self, t, x: list, labels: list = None):
        """
        Efface le graph courant et trace la courbe x(t).
        :param t: Axe des abscisses
        :param x: liste des courbes
        :param labels: liste des labels de courbes
        """
        self.subplot.clear()
        self.subplot.set_title(self.graph_title)
        self.subplot.set_xlabel(self.graph_x_label)
        self.subplot.set_ylabel(self.graph_y_label)
        if labels is not None and len(labels) == len(x):
            for i, xx in enumerate(x):
                self.subplot.plot(t, xx, label=labels[i])
        else:
            for xx in x:
                self.subplot.plot(t, xx)
        self.draw()

    def plot_one_graph(self, t, x, label: str = None):
        """
        Efface le graph courant et trace la courbe x(t).
        :param t: Axe des abscisses
        :param x:  courbe
        :param label: Le nom de la courbe
        """
        self.subplot.clear()
        self.subplot.set_title(self.graph_title)
        self.subplot.set_xlabel(self.graph_x_label)
        self.subplot.set_ylabel(self.graph_y_label)
        if label not in [None, ""]:
            self.subplot.plot(t, x, label="ax")
        else:
            self.subplot.plot(t, x, label=label)
        self.draw()
