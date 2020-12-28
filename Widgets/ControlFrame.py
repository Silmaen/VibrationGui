"""
Module de définition du cadre des controls
"""
import tkinter.ttk as ttk


class ControlframeWidget(ttk.Frame):
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
        self.button_new = ttk.Button(self.frame_fichier)
        self.button_new.config(state='disabled', text='Nouveau')
        self.button_new.grid(sticky='nsew')
        self.button_save = ttk.Button(self.frame_fichier)
        self.button_save.config(state='disabled', text='Sauver')
        self.button_save.grid(row='1', sticky='nsew')
        self.button_load = ttk.Button(self.frame_fichier)
        self.button_load.config(state='disabled', text='Charger')
        self.button_load.grid(row='2', sticky='nsew')

        ttk.Separator(self, orient='horizontal').grid(column='0', row='1', sticky='nsew')

        self.frame_mesure = ttk.Frame(self)
        self.frame_mesure.grid(column='0', row='2', sticky='nsew')
        self.button_mesure = ttk.Button(self.frame_mesure)
        self.button_mesure.config(state='disabled', text='Mesure')
        self.button_mesure.grid(sticky='nsew')

        self.configure(**kw)

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
            self.button_mesure.configure(command=kw[key], state="normal")
            del kw[key]
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def log(self, msg: str, lvl: int = 1):
        """
        fonction de log dans la console
        :param msg: le message à afficher
        :param lvl: le niveau du message (cf. les niveaux de log)
        """
        if self.log_callback:
            self.log_callback(msg, lvl)
