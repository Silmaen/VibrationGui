# encoding: utf8
"""
Module de définition de la vue d'analyse temporelle
"""
import tkinter.ttk as ttk
from GraphWidget import MyGraphWidget
from VectorViewWidget import VectorView
import numpy as np


class AffichageTemporel(ttk.Frame):
    """
    Vue de l'affichage temporel
    """
    def __init__(self, master=None, **kw):
        self.log_callback = None
        if 'log' in kw:
            self.log_callback = kw['log']
            del kw['log']
        ttk.Frame.__init__(self, master, **kw)
        # zone graphique
        self.Graphique = MyGraphWidget(self)
        self.Graphique.configure(plot_number=3,
                                 graph_title_0="Analyse Temporelle",
                                 graph_x_label_0="",
                                 graph_y_label_0="Acceleration (m/s/s)",
                                 graph_title_1="",
                                 graph_x_label_1="",
                                 graph_y_label_1="Voltage (V)",
                                 graph_title_2="",
                                 graph_x_label_2="Temps (s)",
                                 graph_y_label_2="Courant (A)")
        self.Graphique.grid(sticky='nsew')

        # zone de résultats
        self.FrameResult = ttk.Labelframe(self)
        self.FrameResult.columnconfigure('1', weight='1')
        self.FrameResult.columnconfigure('3', weight='1')
        self.FrameResult.columnconfigure('5', weight='1')
        self.FrameResult.config(text='Résultats')
        self.FrameResult.grid(sticky='nsew')

        ttk.Label(self.FrameResult, anchor='e', text='Valeur min: ').grid(column='0', row='0', sticky='nsew')
        ttk.Label(self.FrameResult, anchor='e', text='@').grid(column='0', row='1', sticky='nsew')
        self.ValeurMin = VectorView(self.FrameResult)
        self.ValeurMin.grid(column='1', row='0', sticky='nsew')
        self.ValeurMin_time = VectorView(self.FrameResult)
        self.ValeurMin_time.grid(column='1', row='1', sticky='nsew')

        ttk.Label(self.FrameResult, anchor='e', text=' Valeurs max: ').grid(column='2', row='0', sticky='nsew')
        ttk.Label(self.FrameResult, anchor='e', text='@').grid(column='2', row='1', sticky='nsew')
        self.ValeurMax = VectorView(self.FrameResult)
        self.ValeurMax.grid(column='3', row='0', sticky='nsew')
        self.ValeurMax_time = VectorView(self.FrameResult)
        self.ValeurMax_time.grid(column='3', row='1', sticky='nsew')

        ttk.Label(self.FrameResult, anchor='e', text=' RMS:').grid(column='4', row='0', sticky='nsew')
        ttk.Label(self.FrameResult, anchor='e', text=' Écart type: ').grid(column='4', row='1', sticky='nsew')
        self.ValeurRMS = VectorView(self.FrameResult)
        self.ValeurRMS.grid(column='5', row='0', sticky='nsew')
        self.ValeurStd = VectorView(self.FrameResult)
        self.ValeurStd.grid(column='5', row='1', sticky='nsew')

        self.rowconfigure('0', weight='1')
        self.rowconfigure('1', weight='0')
        self.columnconfigure('0', weight='1')

    def configure(self, cnf=None, **kw):
        """
        Fonction de configuration (Setter General)
        """
        self.Graphique.configure(**kw)
        key = 'log'
        if key in kw:
            self.log_callback = kw[key]
            del kw[key]
        key = 'data'
        if key in kw:
            self.set_data(kw[key])
            del kw[key]
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def log(self, msg: str, lvl: int = 1):
        """
        Fonction de log dans la console
        :param msg: le message à afficher
        :param lvl: le niveau du message (cf. les niveaux de log)
        """
        if self.log_callback:
            self.log_callback(msg, lvl)

    def clear_data(self):
        """
        Nettoie la vue temporelle
        """
        self.ValeurMin.configure(x=0., y=0., z=0.)
        self.ValeurMin_time.configure(x=0., y=0., z=0.)
        self.ValeurMax.configure(x=0., y=0., z=0.)
        self.ValeurMax_time.configure(x=0., y=0., z=0.)
        self.ValeurRMS.configure(x=0., y=0., z=0.)
        self.ValeurStd.configure(x=0., y=0., z=0.)
        self.Graphique.clear_graph()
        self.Graphique.draw()

    def set_data(self, data):
        """
        Mets à jour l'affichage avec les données.
        :param data: the set of data, need data["time"], data["ax"], data["ay"], data["az"]
        """
        if "time" not in data or "ax" not in data or "ay" not in data or "az" not in data:
            self.log("Erreur: Il manque des données (time, ax, ay, az)")
            return
        self.ValeurMin.configure(x=data["ax"].min(), y=data["ay"].min(), z=data["az"].min())
        self.ValeurMin_time.configure(x=data["time"][data["ax"].argmin()],
                                      y=data["time"][data["ay"].argmin()],
                                      z=data["time"][data["az"].argmin()])
        self.ValeurMax.configure(x=data["ax"].max(), y=data["ay"].max(), z=data["az"].max())
        self.ValeurMax_time.configure(x=data["time"][data["ax"].argmax()],
                                      y=data["time"][data["ay"].argmax()],
                                      z=data["time"][data["az"].argmax()])
        self.ValeurRMS.configure(x=np.sqrt(np.mean(np.square(data["ax"]))),
                                 y=np.sqrt(np.mean(np.square(data["ay"]))),
                                 z=np.sqrt(np.mean(np.square(data["az"]))))
        self.ValeurStd.configure(x=data["ax"].std(), y=data["ay"].std(), z=data["az"].std())
        self.Graphique.plot_graphs(data["time"], [data["ax"], data["ay"], data["az"], data["v5"], data["v"], data["i"]],
                                   [0, 0, 0, 1, 1, 2],
                                   ["ax", "ay", "az", "v5", "v", "i"])
