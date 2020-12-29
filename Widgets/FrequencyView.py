# encoding: utf8
"""
Module de définition de la vue d'analyse fréquentielle
"""
import tkinter.ttk as ttk
from GraphWidget import MyGraphWidget
from Tools.utils import fftw, compute_period, RMS_curve, compute_spectrogram, compute_PSD
from VectorViewWidget import VectorView


class FrequencyView(ttk.Frame):
    """
    Vue de l'affichage fréquentiel
    """

    def __init__(self, master=None, **kw):
        self.log_callback = None
        if 'log' in kw:
            self.log_callback = kw['log']
            del kw['log']
        ttk.Frame.__init__(self, master, **kw)

        self.rowconfigure('0', weight='1')
        self.columnconfigure('0', weight='1')

        self.Graphique = MyGraphWidget(self)
        self.Graphique.configure(graph_title="Analyse Fréquentielle",
                                 graph_x_label="Fréquence",
                                 graph_y_label="Amplitude")
        self.Graphique.grid(sticky='nsew')

        self.FrameResult = ttk.Labelframe(self)
        self.FrameResult.config(text='Résultats')
        self.FrameResult.grid(column='0', row='1', sticky='nsew')
        self.FrameResult.columnconfigure('1', weight='1')

        ttk.Label(self.FrameResult, text='Pic: ').grid(sticky='nsew')
        ttk.Label(self.FrameResult, anchor='e', text='@').grid(column='0', row='1', sticky='nsew')

        self.peek_value = VectorView(self.FrameResult)
        self.peek_value.grid(column='1', row='0', sticky='nsew')
        self.peek_value_at = VectorView(self.FrameResult)
        self.peek_value_at.grid(column='1', row='1', sticky='nsew')

    def configure(self, cnf=None, **kw):
        """
        Fonction de configuration (Setter General)
        """
        key = 'log'
        if key in kw:
            self.log_callback = kw[key]
            del kw[key]
        key = 'data'
        if key in kw:
            self.set_data(kw[key])
            del kw[key]
        key = 'graph_title'
        if key in kw:
            self.Graphique.configure(graph_title=kw[key])
            del kw[key]
        key = 'graph_x_label'
        if key in kw:
            self.Graphique.configure(graph_x_label=kw[key])
            del kw[key]
        key = 'graph_y_label'
        if key in kw:
            self.Graphique.configure(graph_y_label=kw[key])
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
        self.peek_value.configure(x=0., y=0., z=0.)
        self.peek_value_at.configure(x=0., y=0., z=0.)
        self.Graphique.clear_graph()
        self.Graphique.draw()

    def set_data(self, data, calcul="FFT"):
        """
        Mets à jour l'affichage avec les données.
        :param data: the set of data, need data["time"], data["ax"], data["ay"], data["az"]
        :param calcul: le type de calcul à effectuer: ["FFT", "RMS"]
        """
        import numpy as np
        if "time" not in data or "ax" not in data or "ay" not in data or "az" not in data:
            self.log("Erreur: Il manque des données (time, ax, ay, az)")
            return
        if calcul == "spectrogram":
            ampl = np.sqrt(data["ax"] ** 2 + data["ay"] ** 2 + data["az"] ** 2)
            f, t2, sxx = compute_spectrogram(data["time"], ampl)
            self.Graphique.plot_spectrogram(t2, f, np.log(sxx))
            return
        elif calcul == "RMS":
            t, x, y, z = RMS_curve(data["time"], data["ax"], data["ay"], data["az"])
        elif calcul == "PSD":
            t, x, y, z = compute_PSD(data["time"], data["ax"], data["ay"], data["az"])
        else:
            n = np.size(data["time"])
            dt, f, s = compute_period(data["time"])
            self.log("écart type de l'échantillon temporel: {:.5f} ".format(s) + ["BAD", "GOOD"][s < 0.001], 3)
            self.log("Fréquence d'échantillonnage         : {:.1f} Hz".format(f), 3)
            x = 2.0 / n * np.abs(fftw(data["ax"]))
            y = 2.0 / n * np.abs(fftw(data["ay"]))
            z = 2.0 / n * np.abs(fftw(data["az"]))
            t = np.linspace(0.0, 1.0 / (2.0 * dt), len(x))

        self.peek_value.configure(x=x.max(), y=y.max(), z=z.max())
        self.peek_value_at.configure(x=t[x.argmax()], y=t[y.argmax()], z=t[z.argmax()])
        self.Graphique.plot_graphs(t, [x, y, z], ["ax", "ay", "az"])
