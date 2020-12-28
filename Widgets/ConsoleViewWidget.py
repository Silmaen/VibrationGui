"""
Module de définition du widget Tk pour le log dans la console
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrollbarhelper import ScrollbarHelper
from datetime import datetime

"""
Niveaux de log:
0: erreur fatale
1: erreur
2: avertissement
3: remarques
4: debug
5: trace
niveau spécial:
-1: communication série (TX)
-2: communication série (RX)
"""
default_level = 1
max_level = 5
level_name = ["ERREUR FATALE ", "ERREUR ", "AVERTISSEMENT ", "REMARQUE ", "DEBUG ", "TRACE "]


class ConsoleWidget(ttk.Frame):
    """
    Widget permettant l'affichage d'une console en lecture seule.
    """
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)

        # options
        self.log_level = tk.IntVar()
        self.log_special = tk.BooleanVar()
        self.horodatage = tk.BooleanVar()
        self.print_type = tk.BooleanVar()

        self.scrollbar_helper = ScrollbarHelper(self, scrolltype='both')
        self.ConsoleText = tk.Text(self.scrollbar_helper.container, height='1', state="disabled")
        self.ConsoleText.pack(side='top', expand='true', fill='both')
        self.scrollbar_helper.add_child(self.ConsoleText)
        self.scrollbar_helper.grid(row=0, column=0, sticky='nswe')

        self.frame_bas = ttk.Frame(self)
        self.chk_autoscroll = ttk.Checkbutton(self.frame_bas)
        self.autoscroll = tk.BooleanVar()
        self.chk_autoscroll.config(text='Défilement Automatique', variable=self.autoscroll, command=self.autoscroll_change)
        self.chk_autoscroll.pack(anchor='nw', side='left')
        self.chk_wrap = ttk.Checkbutton(self.frame_bas)
        self.wordwrap = tk.BooleanVar()
        self.chk_wrap.config(text='Retour à la ligne', variable=self.wordwrap, command=self.wordwrap_change)
        self.chk_wrap.pack(anchor='nw', side='left')
        self.frame_bas.grid(row=1, column=0, sticky='nswe')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(autoscroll=False, wordwrap=False, log_level=default_level, log_special=True, horodatage=True, print_type=True)

    def configure(self, cnf=None, **kw):
        """
        Fonction de configuration (Setter General)
        """
        key = 'autoscroll'
        if key in kw:
            self.autoscroll.set(kw[key])
            del kw[key]
            self.autoscroll_change()
        key = 'wordwrap'
        if key in kw:
            self.wordwrap.set(kw[key])
            del kw[key]
            self.wordwrap_change()
        key = 'log_level'
        if key in kw:
            self.log_level.set(kw[key])
            del kw[key]
        key = 'log_special'
        if key in kw:
            self.log_special.set(kw[key])
            del kw[key]
        key = 'horodatage'
        if key in kw:
            self.horodatage.set(kw[key])
            del kw[key]
        key = 'print_type'
        if key in kw:
            self.print_type.set(kw[key])
            del kw[key]
        ttk.Frame.configure(self, cnf, **kw)

    config = configure

    def cget(self, key):
        """
        Getter general
        :param key: nom de la variable demandée
        :return: sa valeur
        """
        option = 'autoscroll'
        if key == option:
            return self.autoscroll.get()
        option = 'wordwrap'
        if key == option:
            return self.wordwrap.get()
        option = 'log_level'
        if key == option:
            return self.log_level.get()
        option = 'log_special'
        if key == option:
            return self.log_special.get()
        option = 'horodatage'
        if key == option:
            return self.horodatage.get()
        option = 'print_type'
        if key == option:
            return self.print_type.get()
        return ttk.Frame.cget(self, key)

    def autoscroll_change(self):
        """
        Action lors d'un changement de la variable d'auto-scroll
        """
        if self.autoscroll.get():
            self.ConsoleText.configure(state="normal")
            self.ConsoleText.see('end')
            self.ConsoleText.configure(state="disabled")

    def wordwrap_change(self):
        """
        Action lors d'un changement de la variable de wrap.
        """
        self.ConsoleText.configure(state="normal")
        self.ConsoleText.configure(wrap=["none", "word"][self.wordwrap.get()])
        if self.autoscroll.get():
            self.ConsoleText.see('end')
        self.ConsoleText.configure(state="disabled")

    def log(self, msg, lvl: int = default_level):
        """
        fonction de log dans la console
        :param msg: le message à afficher
        :param lvl: le niveau du message (cf. les niveaux de log)
        """
        if lvl > self.log_level.get() or (not self.log_special.get() and lvl < 0):
            return
        if type(msg) == bytes:
            msg = msg.decode("utf8")
        self.ConsoleText.configure(state="normal")
        prefix = ""
        if self.horodatage.get():
            prefix += datetime.now().strftime("%Y%m%d-%H:%M:%S ")
        if lvl < 0:
            if self.log_special.get():
                prefix += ["<<< ", ">>> "][lvl]
        else:
            if self.print_type.get():
                prefix += level_name[lvl]
        # Découpages des différentes lignes et formatage
        to_print = [prefix + a.rstrip() + "\n" for a in msg.splitlines(keepends=False)]
        for p in to_print:
            self.ConsoleText.insert('end', p)
        if self.autoscroll.get():
            self.ConsoleText.see('end')
        self.ConsoleText.configure(state="disabled")
