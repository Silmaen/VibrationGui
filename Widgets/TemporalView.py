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
        ttk.Frame.__init__(self, master, **kw)
        self.Graphique = MyGraphWidget(self)
        self.Graphique.grid(sticky='nsew')
        self.Graphique.rowconfigure('0', weight='1')
        self.Graphique.columnconfigure('0', weight='1')
        self.FrameResult = ttk.Labelframe(self)
        self.label_1 = ttk.Label(self.FrameResult)
        self.label_1.config(text='Valeur min: ')
        self.label_1.grid()
        self.label_2 = ttk.Label(self.FrameResult)
        self.label_2.config(anchor='e', text='@')
        self.label_2.grid(column='0', row='1', sticky='e')
        self.ValeurMin = VectorView(self.FrameResult)
        self.ValeurMin.grid(column='1', row='0', sticky='ew')
        self.ValeurMin.columnconfigure('1', weight='1')
        self.ValeurMin_time = VectorView(self.FrameResult)
        self.ValeurMin_time.grid(column='1', row='1', sticky='ew')
        self.ValeurMin_time.columnconfigure('1', weight='1')
        self.label_3 = ttk.Label(self.FrameResult)
        self.label_3.config(text=' Valeurs max: ')
        self.label_3.grid(column='2', row='0', sticky='ew')
        self.label_4 = ttk.Label(self.FrameResult)
        self.label_4.config(text='@')
        self.label_4.grid(column='2', row='1', sticky='e')
        self.ValeurMax = VectorView(self.FrameResult)
        self.ValeurMax.grid(column='3', row='0', sticky='ew')
        self.ValeurMax.columnconfigure('3', weight='1')
        self.ValeurMax_time = VectorView(self.FrameResult)
        self.ValeurMax_time.grid(column='3', row='1', sticky='ew')
        self.label_5 = ttk.Label(self.FrameResult)
        self.label_5.config(text=' RMS:')
        self.label_5.grid(column='4', row='0', sticky='ew')
        self.label_6 = ttk.Label(self.FrameResult)
        self.label_6.config(text=' Écart type: ')
        self.label_6.grid(column='4', row='1', sticky='e')
        self.ValeurRMS = VectorView(self.FrameResult)
        self.ValeurRMS.grid(column='5', row='0', sticky='ew')
        self.ValeurRMS.columnconfigure('5', weight='1')
        self.ValeurStd = VectorView(self.FrameResult)
        self.ValeurStd.grid(column='5', row='1', sticky='ew')
        self.ValeurStd.columnconfigure('5', weight='1')
        self.FrameResult.config(text='Résultats')
        self.FrameResult.grid(sticky='nsew')
        self.FrameResult.rowconfigure('1', weight='0')
        self.FrameResult.columnconfigure('0', weight='1')

    def set_data(self, data):
        """
        Mets à jour l'affichage avec les données.
        :param data: the set of data, need data["time"], data["ax"], data["ay"], data["az"]
        """
        if "time" not in data or "ax" not in data or "ay" not in data or "az" not in data:
            return
        self.ValeurMin.configure(x=data["ax"].min(), y=data["ay"].min(), z=data["az"].min())
        self.ValeurMin_time.configure(x=data["time"][data["ax"].argmin()], y=data["time"][data["ay"].argmin()],
                                      z=data["time"][data["az"].argmin()])
        self.ValeurMax.configure(x=data["ax"].max(), y=data["ay"].max(), z=data["az"].max())
        self.ValeurMax_time.configure(x=data["time"][data["ax"].argmax()], y=data["time"][data["ay"].argmax()],
                                      z=data["time"][data["az"].argmax()])
        self.ValeurRMS.configure(x=np.sqrt(np.mean(np.square(data["ax"]))), y=np.sqrt(np.mean(np.square(data["ay"]))),
                                 z=np.sqrt(np.mean(np.square(data["az"]))))
        self.ValeurStd.configure(x=data["ax"].std(), y=data["ay"].std(), z=data["az"].std())
        self.Graphique.replot_three_graph(data["time"], data["ax"], data["ay"], data["az"])
