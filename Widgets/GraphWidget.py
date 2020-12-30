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
        self.graph_title = ["Time Domain Signal"]
        self.graph_x_label = ["Time"]
        self.graph_y_label = ["Amplitude"]
        self.configure(**kw)
        self.figure = Figure()
        self.subplots = [self.figure.add_subplot(111)]
        self.subplots[-1].set_title(self.graph_title[-1])
        self.subplots[-1].set_xlabel(self.graph_x_label[-1])
        self.subplots[-1].set_ylabel(self.graph_y_label[-1])
        # Espace de dessin
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # Espace de control
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def configure(self, cnf=None, **kw):
        """
        Fonction de configuration (Setter General)
        """
        key = 'plot_number'
        if key in kw:
            self.set_number_plot(kw[key])
            del kw[key]
        key = 'graph_title_'
        to_del = []
        for k in kw:
            if key in k:
                i = int(k.split(key)[-1])
                if i >= len(self.graph_y_label):
                    self.set_number_plot(i+1)
                self.graph_title[i] = kw[k]
                self.subplots[i].set_title(self.graph_title[i])
                to_del.append(k)
        key = 'graph_x_label_'
        for k in kw:
            if key in k:
                i = int(k.split(key)[-1])
                if i >= len(self.graph_y_label):
                    self.set_number_plot(i+1)
                self.graph_x_label[i] = kw[k]
                self.subplots[i].set_xlabel(self.graph_x_label[i])
                to_del.append(k)
        key = 'graph_y_label_'
        for k in kw:
            if key in k:
                i = int(k.split(key)[-1])
                if i >= len(self.graph_y_label):
                    self.set_number_plot(i+1)
                self.graph_y_label[i] = kw[k]
                self.subplots[i].set_ylabel(self.graph_y_label[i])
                to_del.append(k)
        for k in to_del:
            del kw[k]
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def cget(self, key):
        """
        Getter general
        :param key: nom de la variable demandée
        :return: sa valeur
        """
        option = 'graph_title_'
        if option in key:
            i = int(key.split(option)[-1])
            if i >= len(self.graph_title):
                return None
            return self.graph_title[i]
        option = 'graph_x_label_'
        if option in key:
            i = int(key.split(option)[-1])
            if i >= len(self.graph_title):
                return None
            return self.graph_x_label[i]
        option = 'graph_y_label_'
        if option in key:
            i = int(key.split(option)[-1])
            if i >= len(self.graph_title):
                return None
            return self.graph_y_label[i]
        return ttk.Frame.cget(self, key)

    def draw(self):
        """
        Actualisation de la zone de dessin
        """
        self.canvas.draw()

    def set_number_plot(self, number):
        """
        change the number of the plots
        :param number: the new number of curves
        """
        if number == len(self.graph_title):
            return
        if number < len(self.graph_title):
            del self.graph_title[number:]
            del self.graph_x_label[number:]
            del self.graph_y_label[number:]
            self.clear_graph()
        else:
            self.graph_title += [""] * (number - len(self.graph_title))
            self.graph_x_label += [""] * (number - len(self.graph_x_label))
            self.graph_y_label += [""] * (number - len(self.graph_y_label))
            self.clear_graph()

    def clear_graph(self):
        """
        Nettoie la vue graphique
        """
        self.figure.clear()
        self.subplots.clear()
        for i in range(len(self.graph_title)):
            self.subplots.append(self.figure.add_subplot(len(self.graph_title), 1, i+1))
            if self.graph_title[i] not in ["", None]:
                self.subplots[-1].set_title(self.graph_title[i])
            if self.graph_x_label[i] not in ["", None]:
                self.subplots[-1].set_xlabel(self.graph_x_label[i])
            if self.graph_y_label[i] not in ["", None]:
                self.subplots[-1].set_ylabel(self.graph_y_label[i])

    def plot_graphs(self, t, x: list, indices: list, labels: list = None):
        """
        Efface le graph courant et trace la courbe x(t).
        :param t: Axe des abscisses
        :param x: liste des courbes
        :param indices: liste des indice sur le
        :param labels: liste des labels de courbes
        """
        self.clear_graph()
        if labels is not None and len(labels) == len(x):
            for i, xx in enumerate(x):
                self.subplots[indices[i]].plot(t, xx, label=labels[i])
        else:
            for i, xx in enumerate(x):
                self.subplots[indices[i]].plot(t, xx)
        self.draw()

    def plot_spectrogram(self, t, f, s_log):
        """
        Dessine un spectrogramme
        :param t: échelle de temps
        :param f: échelle de fréquence
        :param s_log: le tableau de valeur
        """
        self.clear_graph()
        self.subplots[0].pcolormesh(t, f, s_log, shading="auto", cmap='ocean')
        self.draw()
