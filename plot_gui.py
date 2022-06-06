import tkinter as tk
from tkinter import ttk
import default
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
import default as defaults
import equation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    FigureCanvasTk,
    NavigationToolbar2Tk
)
import matplotlib.animation as animation

import matplotlib
matplotlib.use('TkAgg')


class PlotBox(tk.Tk):
    """
    We don't care what equation is solved, just the fact that we have an equation and it has the plot function
    """
    Entry_label_dict = []

    Special_Entry_List = []

    Equation_opts = ['Heat equation', 'Schrodinger equation',
            'One way wave equation']

    visual_opts = ['Image', 'Animation']

    Initial_func = ['Gaussian', 'Sinc wave', 'Sine wave']

    def __init__(self, main_frame):
        self.main_frame = main_frame
        self.create_figure()
        self._create_buttons_of_figure()
        self._create_plot_button()
        self.step = 0

    def set_equation(self, eq) -> (equation.Equation):
        self.eq = eq

    ## Create the figure box
    def create_figure(self):
        """
        This method creates a second subframe and places a figure inside it.
        """
        self.sub_frm2 = tk.Frame(self.main_frame, highlightbackground="black",
                                 highlightthickness=2, padx=defaults.subPAD,
                                 pady=defaults.subPAD)
        self.Title = tk.Label(self.sub_frm2,
                              text='Visualization',
                              font=('Helvatical bold', 25))
        self.Title.grid(column=0, row=0)

        self.sub_frm2.grid(column=1, row=2, padx=defaults.subPAD_out,
                           pady=defaults.subPAD_out)

        self.fig = Figure(figsize=(6, 4), dpi=100)
        # self.canvas = FigureCanvasTkAgg(self.fig, self.sub_frm2)
        self.frame = tk.Frame(self.sub_frm2)
        self.frame.grid(column=2, row=1, padx=defaults.subPAD_out,
                           pady=defaults.subPAD_out)

        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        # self.canvas.get_tk_widget().grid(column=0, row=2)
        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame).update()


    def _create_plot_button(self):
        """
        This method creates the solve button.
        """

        self.MyButton2 = tk.Button(self.main_frame, text='Start Plotting!',
                                   command=self._animate_equation)

        self.MyButton2.grid(column=1, row=3, sticky='n', padx=5,
                            pady=5)

    def _create_buttons_of_figure(self):
        """
        This method creates the solve button.
        """
        self.step = 0

        self.MyButton2 = tk.Button(self.sub_frm2, text='Next plot',
        command=self._command_next_plot)
        self.MyButton2.grid(column=1, row=1, sticky='n', padx=5,
                            pady=50)

        self.MyButton2 = tk.Button(self.sub_frm2, text='Previous plot',
        command=self._command_prev_plot)
        self.MyButton2.grid(column=0, row=1, sticky='n', padx=5,
                            pady=50)

        self.MyButton2 = tk.Button(self.sub_frm2, text='Animate',
                                   command=self._command_animate_plot)
        self.MyButton2.grid(column=1, row=1, sticky='n', padx=5,
                            pady=100)

        self.MyButton2 = tk.Button(self.sub_frm2, text='Stop',
                                   command=self._command_animate_plot)
        self.MyButton2.grid(column=0, row=1, sticky='n', padx=5,
                            pady=100)

    def _animate_equation(self):
        try:
            self.eq.start_plot(self.fig)
            self.canvas.draw()
        except:
            self._error_message("Failed to animate")


    def _command_animate_plot(self):
        self.step = self.step - 1
        # try:
        # self.x = 20*np.arange(0, 2*np.pi, 0.01)        # x-array
        # self.fig = plt.Figure()

        self.eq.plot_animation(self.fig)
        # self.ax = self.fig.add_subplot(111)
        # line, = self.ax.plot(self.x, np.sin(self.x))
        # #
        # def animate(i):
        #     print("ANIMATION")
        #
        #     if i == 100:
        #         return
        #     line.set_ydata(np.sin(self.x + i))  # update the data
        #     return line,
        # self.ani = animation.FuncAnimation(self.fig, animate, interval=25, blit=False, frames=200, save_count=50)
        self.canvas.draw()

    def _command_next_plot(self):
        try:
            if self.eq.plot_step(1):
                self._error_message("No next plot found. Reset to initial plot")
            else:
                self.fig.canvas.draw()
        except:
            self._error_message("Are you sure you clicked solve and started plotting?")

    def _command_prev_plot(self):
        try:
            if self.eq.plot_step(-1):
                self._error_message("No previous plot found. Reset to initial plot")
            else:
                self.fig.canvas.draw()
        except:
            self._error_message("Are you sure you clicked solve and started plotting?")

    def _error_message(self, message):
        messagebox.showerror("Error", message)

