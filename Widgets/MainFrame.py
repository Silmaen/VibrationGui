"""
Module de définition de la page principale du programme
"""
import tkinter.ttk as ttk
from ConsoleViewWidget import ConsoleWidget
from FrequencyView import FrequencyView
from TemporalView import AffichageTemporel
from ControlFrame import ControlFrameWidget
from Tools.Measure import MesureManager


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
        self.frame_haut.columnconfigure('0', minsize='100', weight='0')
        self.frame_haut.columnconfigure('1', minsize='400', weight='1')

        self.frame_haut.grid(sticky='nsew')

        self.frame_gauche = ttk.Frame(self.frame_haut)
        self.frame_gauche.grid(sticky='nsew')

        self.control_frame = ControlFrameWidget(self.frame_gauche)
        self.control_frame.configure(log=self.log)
        self.control_frame.configure(mesure_callback=self.begin_mesure)
        self.control_frame.configure(new_callback=self.new_data)
        self.control_frame.configure(save_callback=self.save_data)
        self.control_frame.configure(load_callback=self.load_data)
        self.control_frame.configure(graph_change_callback=self.current_data_change)
        self.control_frame.grid(sticky='nsew')

        self.notebook_droit = ttk.Notebook(self.frame_haut)
        self.notebook_droit.grid(column='1', row='0', sticky='nsew')

        self.affichage_temporel = AffichageTemporel(self.notebook_droit, log=self.log)
        self.affichage_temporel.grid(sticky='nsew')
        self.affichage_temporel.rowconfigure('0', minsize='0', weight='1')
        self.affichage_temporel.columnconfigure('0', weight='1')
        self.notebook_droit.add(self.affichage_temporel, sticky='nsew', text='Analyse Temporelle')

        self.rms_view = FrequencyView(self.notebook_droit, log=self.log)
        self.rms_view.grid(sticky='nsew')
        self.rms_view.rowconfigure('0', minsize='0', weight='1')
        self.rms_view.columnconfigure('0', weight='1')
        self.rms_view.configure(graph_title="RMS Mobile",
                                graph_x_label="Temps",
                                graph_y_label="Amplitude")
        self.notebook_droit.add(self.rms_view, sticky='nsew', text='RMS mobile')

        self.freq_view = FrequencyView(self.notebook_droit, log=self.log)
        self.freq_view.grid(sticky='nsew')
        self.freq_view.rowconfigure('0', minsize='0', weight='1')
        self.freq_view.columnconfigure('0', weight='1')
        self.notebook_droit.add(self.freq_view, sticky='nsew', text='Analyse Fréquentielle')

        self.spec_view = FrequencyView(self.notebook_droit, log=self.log)
        self.spec_view.grid(sticky='nsew')
        self.spec_view.rowconfigure('0', minsize='0', weight='1')
        self.spec_view.columnconfigure('0', weight='1')
        self.spec_view.configure(graph_title="Spectrogramme",
                                 graph_x_label="Temps",
                                 graph_y_label="Fréquence")
        self.notebook_droit.add(self.spec_view, sticky='nsew', text='Spectrogramme')

        self.console_widget = ConsoleWidget(self)
        self.console_widget.configure(log_level=5, autoscroll=True, wordwrap=True)
        self.console_widget.grid(row='1', sticky='nsew')

        self.mesure_manager = MesureManager(master, self.log, self.end_measure)
        self.global_data = []
        self.project_name = ""

    def configure(self, cnf=None, **kw):
        """
        Fonction de configuration (Setter General)
        """
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def log(self, msg: str, lvl: int = 1):
        """
        fonction de log dans la console
        :param msg: le message à afficher
        :param lvl: le niveau du message (cf. les niveaux de log)
        """
        self.console_widget.log(msg, lvl)

    def set_data(self, data):
        """
        Mets à jour l'affichage avec les données.
        :param data: the set of data, need data["time"], data["ax"], data["ay"], data["az"]
        """
        self.affichage_temporel.set_data(data)
        self.rms_view.set_data(data, "RMS")
        self.freq_view.set_data(data)
        self.spec_view.set_data(data, "spectrogram")

    def new_data(self):
        """
        Remise à zéro des données
        """
        self.global_data.clear()
        self.project_name = ""
        self.control_frame.configure(data_list=[])
        self.affichage_temporel.clear_data()
        self.freq_view.clear_data()
        self.rms_view.clear_data()
        self.spec_view.clear_data()

    def current_data_change(self):
        """
        Changement de data.
        """
        index = self.control_frame.combobox_data.current()
        self.set_data(self.global_data[index])

    def save_data(self):
        """
        Sauvegarde les données
        """
        from pathlib import Path
        import pickle
        if self.project_name == "":
            # todo: demander un nom de projet
            self.project_name = "projet"
        if len(self.global_data) < 1:
            self.log("Pas de données à sauvegarder")
            return
        data_dir = Path(__file__).parent.parent / "data"
        if not data_dir.is_dir():
            if data_dir.exists():
                data_dir.unlink()
            data_dir.mkdir()
        data_file = data_dir / (self.project_name + ".vmd")
        if data_file.exists():
            data_file.unlink()
        with open(data_file, "wb") as f:
            pickle.dump(self.global_data, f, pickle.HIGHEST_PROTOCOL)
        self.log("Données sauvegardée dans " + str(data_file), 3)

    def load_data(self):
        """
        Chargement de données depuis le disque dur
        """
        from pathlib import Path
        import pickle
        if self.project_name == "":
            # todo: demander un nom de projet
            self.project_name = "projet"
        data_dir = Path(__file__).parent.parent / "data"
        data_file = data_dir / (self.project_name + ".vmd")
        self.log("Chargement des données depuis " + str(data_file), 3)
        if not data_file.exists():
            self.log("Le fichier " + str(data_file) + " N'existe pas.")
            return
        self.new_data()
        with open(data_file, 'rb') as f:
            self.global_data = pickle.load(f)
        self.set_data(self.global_data[-1])
        self.control_frame.configure(data_list=[i for i in range(len(self.global_data))])
        self.log("Données chargées depuis " + str(data_file), 3)

    def end_measure(self):
        """
        Call back pour le gestionnaire de mesure sera appelé lorsque les mesures seront finies
        """
        self.control_frame.button_mesure.configure(state="normal")
        if self.mesure_manager.data_change:
            self.global_data.append(self.mesure_manager.get_data())
            self.control_frame.configure(data_list=[i for i in range(len(self.global_data))])
            self.set_data(self.global_data[-1])

    def begin_mesure(self):
        """
        Procédure de mesure: démarre les mesure dans un thread à part
        """
        self.log("Démarrage des mesures", 3)
        self.control_frame.button_mesure.configure(state="disabled")
        self.mesure_manager.Mesure()
