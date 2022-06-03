import tkinter as tk
from tkinter import ttk
import default
from tkinter import messagebox

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import default as defaults
import equation

class PlotBox(tk.Tk):
    values_to_insert_Gaussian = ['Amplitude:',
                                      'Sigma:',
                                      'Mu:']

    values_to_insert_sin_sinc = ['Amplitude:',
                                      'Phase:',
                                      'Wave vector:']

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

    ## Create the figure box
    def create_figure(self):
        """
        This method creates a second subframe and places a figure inside it.
        """
        self.sub_frm2 = tk.Frame(self.main_frame, highlightbackground="black",
                                 highlightthickness=2, padx=defaults.subPAD,
                                 pady=defaults.subPAD)
        self.Title = tk.Label(self.sub_frm2,
                              text='Visualization of the solution',
                              font=('Helvatical bold', 25))
        self.Title.grid(column=0, row=0)

        self.sub_frm2.grid(column=1, row=2, padx=defaults.subPAD_out,
                           pady=defaults.subPAD_out)

        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self.sub_frm2)
        self.canvas.get_tk_widget().grid(column=0, row=2)

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
        self.MyButton2.grid(column=1, row=2, sticky='n', padx=5,
                            pady=5)

        self.MyButton2 = tk.Button(self.sub_frm2, text='Previous plot',
        command=self._command_prev_plot)
        self.MyButton2.grid(column=3, row=2, sticky='n', padx=5,
                            pady=5)

        self.MyButton2 = tk.Button(self.sub_frm2, text='Animate',
                                   command=self._command_animate_plot)
        self.MyButton2.grid(column=1, row=2, sticky='n', padx=5,
                            pady=50)

        self.MyButton2 = tk.Button(self.sub_frm2, text='Stop',
                                   command=self._command_animate_plot)
        self.MyButton2.grid(column=3, row=2, sticky='n', padx=5,
                            pady=50)

    def _animate_equation(self):
        try:
            self.eq.start_plot(self.fig)
            self.canvas.draw()
        except:
            self._error_message("Failed to animate")

    def _command_animate_plot(self):
        step = self.step - 1
        # try:
        #     # while self.fig
        # except:
        #     self._error_message("No previous plot found")
        pass

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

    def set_equation(self, eq):
        self.eq = eq