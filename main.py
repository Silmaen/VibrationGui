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
# for plotting
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
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
    root.title("Super Programme de test")
    root.geometry("1024x768")

    root.mainloop()
