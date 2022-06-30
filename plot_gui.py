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
        # For pause and resume animation...
        self.animation = None
        self.stop = False # To stop or to resume the animation

    def set_equation(self, eq) -> (equation.Equation):
        """
        Once we pressed solve equation, we have to notify the gui window, this is how we pass the equation
        :param eq:
        :return:
        """
        self.eq = eq

    ## Create the figure box
    def create_figure(self):
        """
        This method creates a second subframe and places a figure window inside it.
        The figure window is actualy a figure in matplotlib, it has a nice embedding rule
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

        # CReate the figure in which the plot itself will be shown
        self.fig = Figure(figsize=(6, 4), dpi=100)
        # self.canvas = FigureCanvasTkAgg(self.fig, self.sub_frm2)
        self.frame = tk.Frame(self.sub_frm2)
        self.frame.grid(column=2, row=1, padx=defaults.subPAD_out,
                           pady=defaults.subPAD_out)
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame).update()


    def _create_plot_button(self):
        """
        This method creates the solve button.
        """

        self.MyButton2 = tk.Button(self.main_frame, text='Plot',
                                   command=self._command_plot_equation)

        self.MyButton2.grid(column=1, row=3, sticky='n', padx=5,
                            pady=5)

    def _create_buttons_of_figure(self):
        """
        This method creates the interaction buttons.
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

        self.MyButton2 = tk.Button(self.sub_frm2, text='Pause/Resume',
                                   command=self._command_stop)
        self.MyButton2.grid(column=0, row=1, sticky='n', padx=5,
                            pady=100)

    def _command_plot_equation(self):
        """
        Starts plotting the solution of the equation
        :return: nothing
        """
        try:
            self.step = 0 # reset...
            self.eq.start_plot(self.fig)
            self.canvas.draw()
        except:
            self._error_message("Failed to animate")


    def _command_animate_plot(self):
        """
        Starts the animation
        :return:
        """
        self.step = self.step - 1
        self.animation = self.eq.plot_animation(self.fig) # we have to pass and create the fig
        self.canvas.draw()

    def _command_stop(self):
        if self.animation:
            if self.stop:
                self.animation.event_source.start()
                self.stop = False
            else:
                self.animation.event_source.stop()
                self.stop = True

    def _command_next_plot(self):
        """
        activates the next plot with the step counter...
        :return:
        """
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

