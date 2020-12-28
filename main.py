#! /usr/bin/env python
# encoding: utf8
"""
Section principale du programme
"""
good_env = True
try:
    import tkinter as tk
except Exception as err:
    good_env = False
    print("ERREUR: le module 'tkinter' n'est pas présent ou vous utilisez une version de python trop vielle.")
    print(str(err))
try:
    import numpy as np
    from MainFrame import MainFrameWidget
except Exception as err:
    good_env = False
    print("ERREUR: un module nécessaire est absent: " + str(err))
if not good_env:
    import sys
    sys.exit(-666)


# data
t = np.arange(0, 3, .01)
x = 2 * np.sin(2 * np.pi * t)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Analyse de vibration")
    root.geometry("800x600")
    w = MainFrameWidget(master=root)
    w.pack(expand=True, fill='both')
    root.mainloop()
