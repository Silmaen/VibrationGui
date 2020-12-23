import tkinter as tk
from Widgets.GraphWidget import MyGraphWidget
import numpy as np
# for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# data
t = np.arange(0, 3, .01)
x = 2 * np.sin(2 * np.pi * t)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Super Programme de test")
    root.geometry("1024x768")

    gr = MyGraphWidget(root)
    gr.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.5)
    gr.add_subplot(111)
    gr.plot(t, x)

    root.mainloop()
