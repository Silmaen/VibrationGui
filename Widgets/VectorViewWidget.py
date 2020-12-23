# encoding: utf8
"""
Module de définition d'une vue de vecteur
"""
import tkinter as tk
import tkinter.ttk as ttk


class VectorView(ttk.Frame):
    """
    Simple vue permettant l'affichage de vecteur.
    """
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        # subwidgets
        o = ttk.Label(self, text=' X', width=2)
        o.grid(row=0, column=0)
        self.wx = tk.DoubleVar(0.000)
        o = ttk.Label(self, width=4, justify='center', textvariable=self.wx, anchor='center', relief='sunken')
        o.grid(row=0, column=1, sticky='nswe')
        o = ttk.Label(self, text=' Y', width=2)
        o.grid(row=0, column=2)
        self.wy = tk.DoubleVar(0.000)
        o = ttk.Label(self, width=4, justify='center', textvariable=self.wy, anchor='center', relief='sunken')
        o.grid(row=0, column=3, sticky='nswe')
        o = ttk.Label(self, text=' Z', width=2)
        o.grid(row=0, column=4)
        self.wz = tk.DoubleVar(0.000)
        o = ttk.Label(self, width=4, justify='center', textvariable=self.wz, anchor='center', relief='sunken')
        o.grid(row=0, column=5, sticky='nswe')
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(5, weight=1)
        self.configure(x=0.0, y=0.0, z=0.0)

    def configure(self, cnf=None, **kw):
        """
        Fonction de configuration (Setter General)
        """
        key = 'x'
        if key in kw:
            self.wx.set(kw[key])
            del kw[key]
        key = 'y'
        if key in kw:
            self.wy.set(kw[key])
            del kw[key]
        key = 'z'
        if key in kw:
            self.wz.set(kw[key])
            del kw[key]
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def cget(self, key):
        """
        Getter general
        :param key: nom de la variable demandée
        :return: sa valeur
        """
        option = 'x'
        if key == option:
            return self.wx.get()
        option = 'y'
        if key == option:
            return self.wy.get()
        option = 'z'
        if key == option:
            return self.wz.get()
        option = 'value'
        if key == option:
            return self.wx.get(), self.wy.get(), self.wz.get()
        return ttk.Frame.cget(self, key)

