"""
Module de définition de la page principale du programme
"""
import tkinter as tk
import tkinter.ttk as ttk
from ConsoleViewWidget import ConsoleWidget
from TemporalView import AffichageTemporel


class MainFrameWidget(ttk.Frame):
    """
    La page principale du programme
    """
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)

        # configuration de la grille principale
        self.rowconfigure('0', minsize='400', weight='4')
        self.rowconfigure('1', minsize='100', weight='1')
        self.columnconfigure('0', minsize='500', weight='1')

        # configuration de la grille du haut
        self.frame_haut = ttk.Frame(self)
        self.frame_haut.rowconfigure('0', minsize='400', weight='1')
        self.frame_haut.columnconfigure('0', minsize='100', weight='1')
        self.frame_haut.columnconfigure('1', minsize='400', weight='5')
        self.frame_haut.grid(sticky='nsew')

        self.frame_gauche = ttk.Frame(self.frame_haut)
        self.frame_gauche.grid(sticky='nsew')
        self.notebook_droit = ttk.Notebook(self.frame_haut)
        self.affichage_temporel = AffichageTemporel(self.notebook_droit)
        self.affichage_temporel.grid(sticky='nsew')
        self.affichage_temporel.rowconfigure('0', minsize='0', weight='1')
        self.affichage_temporel.columnconfigure('0', weight='1')
        self.notebook_droit.add(self.affichage_temporel, sticky='nsew', text='Analyse Temporelle')
        self.notebook_droit.grid(column='1', row='0', sticky='nsew')

        self.console_widget = ConsoleWidget(self)
        self.console_widget.grid(row='1', sticky='nsew')

    def log(self, msg: str, lvl: int = 1):
        self.console_widget.log(msg, lvl)

    def set_data_temporal(self, data):
        self.affichage_temporel.set_data(data)
