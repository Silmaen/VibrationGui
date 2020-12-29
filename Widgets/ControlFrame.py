"""
Module de définition du cadre des controls
"""
import tkinter.ttk as ttk


class ControlFrameWidget(ttk.Frame):
    """
    Le cadre avec les boutons de control
    """
    def __init__(self, master=None, **kw):
        self.log_callback = None
        if 'log' in kw:
            self.log_callback = kw['log']
            del kw['log']
        ttk.Frame.__init__(self, master, **kw)
        self.rowconfigure('0', weight='1')
        self.rowconfigure('2', weight='1')
        self.columnconfigure('0', weight='1')

        self.frame_fichier = ttk.Frame(self)
        self.frame_fichier.grid(sticky='nsew')
        ttk.Label(self.frame_fichier, text='Projet', anchor="center").grid(sticky='nsew')
        self.button_new = ttk.Button(self.frame_fichier)
        self.button_new.config(state='disabled', text='Nouveau')
        self.button_new.grid(row='1', sticky='nsew')
        self.button_save = ttk.Button(self.frame_fichier)
        self.button_save.config(state='disabled', text='Sauver')
        self.button_save.grid(row='2', sticky='nsew')
        self.button_load = ttk.Button(self.frame_fichier)
        self.button_load.config(state='disabled', text='Charger')
        self.button_load.grid(row='3', sticky='nsew')

        ttk.Separator(self, orient='horizontal').grid(column='0', row='1', sticky='nsew')

        self.frame_mesure = ttk.Frame(self)
        self.frame_mesure.grid(column='0', row='2', sticky='nsew')
        ttk.Label(self.frame_mesure, text='Mesure', anchor="center").grid(sticky='nsew')

        ttk.Label(self.frame_mesure, text='Échelle de mesure:').grid(row='1', sticky='nsew')
        self.combobox_range = ttk.Combobox(self.frame_mesure)
        self.combobox_range.config(state="readonly", values=["2G", "4G", "8G", "16G"])
        self.combobox_range.current(3)
        self.combobox_range.grid(row='2', sticky='nsew')
        self.combobox_range.bind("<<ComboboxSelected>>", self.validate_range)

        ttk.Label(self.frame_mesure, text='Résolution:').grid(row='3', sticky='nsew')
        self.combobox_resolution = ttk.Combobox(self.frame_mesure)
        self.combobox_resolution.config(state="readonly", values=["LOW", "HIGH"])
        self.combobox_resolution.current(1)
        self.combobox_resolution.grid(row='4', sticky='nsew')
        self.combobox_resolution.bind("<<ComboboxSelected>>", self.validate_resolution)

        ttk.Label(self.frame_mesure, text='Durée de mesure:').grid(row='5', sticky='nsew')
        self.spin_time = ttk.Spinbox(self.frame_mesure)
        self.spin_time.config(state="readonly", command=self.time_change, from_=5, to=15, increment=1)
        self.spin_time.set(5)
        self.spin_time.grid(row='6', sticky='nsew')

        self.button_mesure = ttk.Button(self.frame_mesure)
        self.button_mesure.config(state='disabled', text='Mesure')
        self.button_mesure.grid(row='7', sticky='nsew')

        ttk.Separator(self, orient='horizontal').grid(column='0', row='3', sticky='nsew')

        self.frame_Data = ttk.Frame(self)
        self.frame_Data.grid(column='0', row='4', sticky='nsew')
        ttk.Label(self.frame_mesure, text='Jeu de données', anchor="center").grid(sticky='nsew')

        self.combobox_data = ttk.Combobox(self.frame_Data)
        self.combobox_data.config(validate='all', state="disabled")
        self.combobox_data.grid(row='1', sticky='nsew')
        self.combobox_data.bind("<<ComboboxSelected>>", self.validate_data)

        self.graph_change_callback = None
        self.range_change_callback = None
        self.resolution_change_callback = None
        self.time_change_callback = None
        self.configure(**kw)

    def validate_data(self, event):
        """
        Événement lors d'un changement de valeur
        :param event:
        """
        self.log(str(event) + " " + str(self.combobox_data.current()), 5)
        if self.graph_change_callback is not None:
            self.graph_change_callback()

    def validate_range(self, event):
        """
        Événement lors d'un changement de valeur
        :param event:
        """
        self.log(str(event) + " " + str(self.combobox_range.current()), 5)
        if self.range_change_callback is not None:
            self.range_change_callback()

    def validate_resolution(self, event):
        """
        Événement lors d'un changement de valeur
        :param event:
        """
        self.log(str(event) + " " + str(self.combobox_resolution.current()), 5)
        if self.resolution_change_callback is not None:
            self.resolution_change_callback()

    def time_change(self):
        """
        Événement lors d'un changement de valeur
        """
        self.log("Changement du temps: " + str(self.spin_time.get()), 5)
        if self.time_change_callback is not None:
            self.time_change_callback()

    def configure(self, cnf=None, **kw):
        """
        Fonction de configuration (Setter General)
        """
        key = 'log'
        if key in kw:
            self.log_callback = kw[key]
            del kw[key]
        key = 'new_callback'
        if key in kw:
            self.button_new.configure(command=kw[key], state="normal")
            del kw[key]
        key = 'save_callback'
        if key in kw:
            self.button_save.configure(command=kw[key], state="normal")
            del kw[key]
        key = 'load_callback'
        if key in kw:
            self.button_load.configure(command=kw[key], state="normal")
            del kw[key]
        key = 'mesure_callback'
        if key in kw:
            self.button_mesure.configure(command=kw[key], state="readonly")
            del kw[key]
        key = 'graph_change_callback'
        if key in kw:
            self.graph_change_callback = kw[key]
            del kw[key]
        key = 'range_change_callback'
        if key in kw:
            self.range_change_callback = kw[key]
            del kw[key]
        key = 'resolution_change_callback'
        if key in kw:
            self.resolution_change_callback = kw[key]
            del kw[key]
        key = 'time_change_callback'
        if key in kw:
            self.time_change_callback = kw[key]
            del kw[key]
        key = 'data_list'
        if key in kw:
            self.define_mesure_list(kw[key])
            del kw[key]
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def cget(self, key):
        """
        Getter global
        :param key: le nom de la propriété
        """
        if key == "mesure_time":
            return self.spin_time.get()
        if key == "mesure_range":
            return self.combobox_range.current()
        if key == "mesure_resolution":
            return self.combobox_resolution.current()
        return ttk.Frame.cget(self, key)

    def log(self, msg: str, lvl: int = 1):
        """
        fonction de log dans la console
        :param msg: le message à afficher
        :param lvl: le niveau du message (cf. les niveaux de log)
        """
        if self.log_callback:
            self.log_callback(msg, lvl)

    def define_mesure_list(self, data_list):
        """
        Définition de la nouvelle liste de données
        :param data_list: la nouvelle liste
        """
        if type(data_list) != list:
            data_list = []
        self.combobox_data.configure(state=["readonly", "disabled"][len(data_list) == 0])
        self.combobox_data.configure(values=data_list)
        if len(data_list) > 0:
            self.combobox_data.current(len(data_list)-1)

    def measuring(self):
        """
        Désactive les boutons non utilisables pendant une mesure
        """
        self.button_mesure.configure(state="disabled")
        self.combobox_range.configure(state="disabled")
        self.combobox_resolution.configure(state="disabled")
        self.spin_time.configure(state="disabled")

    def readyToMeasure(self):
        """
        Réactive les boutons non utilisables pendant une mesure
        """
        self.button_mesure.configure(state="normal")
        self.combobox_range.configure(state="readonly")
        self.combobox_resolution.configure(state="readonly")
        self.spin_time.configure(state="readonly")
