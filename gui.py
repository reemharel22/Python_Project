import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import default
import equation
import plot_gui

class Gui(tk.Tk):
    PAD = 30

    # subPAD = 30
    #
    # subPAD_out = 30

    Chosen_equation = ''

    Chosen_initial_condition_form = ''

    Entry_list = []

    Label_list = []

    Entry_list_Gaussian = []

    Label_list_Gaussian = []

    Entry_list_Sin_Sinc = []

    Label_list_Sin_Sinc = []

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

    def __init__(self, controller):

        super().__init__()

        self.title('Visuquation User Interface')

        self._make_main_frame()

        self.Equation_type = tk.StringVar()

        self.Equation_type.set(self.Equation_opts[0])

        self._make_drop_down_list()

        self._make_sub_frame()

        self._create_enter_button()

        self.plot_gui = plot_gui.PlotBox(self.main_frm)

        # self.plot_gui.create_figure()

        # self._create_figure()

        # self._create_solve_button()

        # self._create_buttons_of_figure()

        self._create_initial_func_drop_down_list()

    def main(self):

        self.mainloop()

    def _error_message(self, message):
        messagebox.showerror("Error", message)

    def _make_main_frame(self):
        """
        This method creates the main frame.
        """

        self.main_frm = ttk.Frame(self)

        self.main_frm.grid(padx=self.PAD, pady=self.PAD)


    def _make_sub_frame(self):
        """
        This method creates a subframe and places Entries inside.
        """
        # default:
        self.Chosen_equation = self.Equation_opts[0]
        self.sub_frm = tk.Frame(self.main_frm, highlightbackground="black",
                                highlightthickness=2, padx=5,#self.subPAD,
                                pady=5)#self.subPAD)

        self.Title = tk.Label(self.sub_frm,
                              text='Please enter the following values:',
                              font=('Helvatical bold', 10))

        self.Title.grid(column=0, row=0, pady=5)

        self.sub_frm.grid(column=0, row=2, padx=default.subPAD_out, pady=default.subPAD_out)

        self.values_to_insert = ['Initial condition:',
                                 'Number of Cells (nx):',
                                 'x_max:',
                                 'Boundry value at x0:',
                                 'Number cycles:',
                                 'Final time:',
                                 'Alpha:',
                                 'Velocity:']

        for i in range(0, len(self.values_to_insert) - 1):
            # labels
            self.labelDir = tk.Label(self.sub_frm, text=self.values_to_insert[i])
            self.labelDir.grid(row=i+1, column=0, padx=0, pady=3, sticky=tk.W)
            self.Label_list.append(self.labelDir)

            # textbox
            self.myEntry = tk.Entry(self.sub_frm, borderwidth=1, width=25)
            self.myEntry.grid(row=i+1, column=1, pady=3)
            self.myEntry.insert(0, default.Diffusion_default[self.values_to_insert[i]])
            self.Entry_list.append(self.myEntry)

        self.myEntry = tk.Entry(self.sub_frm, borderwidth=3, width=25)
        self.labelDir = tk.Label(self.sub_frm,
                                 text=self.values_to_insert[-1])
        self.Label_list.append(self.labelDir)

        self.myEntry.insert(0, self.values_to_insert[-1])

        self.Entry_list.append(self.myEntry)

        self.Entry_label_dict = dict(zip(self.values_to_insert, self.Entry_list))

        self.Entry_label_dict_wave = dict(zip(self.values_to_insert, self.Entry_list))

    def _show_special_entries_and_save_choice(self, e):
        """
        This method builds the unique entries and saves
        the choice from the dropdown list.
        """
        self.Chosen_equation = self.Equation_type.get()

        if e == self.Equation_opts[1]: # schrodinger

            self.MyButton.grid_forget()

            self.Entry_list[-1].grid_forget()

            self.Label_list[-1].grid_forget()

            self.Entry_list[-2].grid_forget()

            self.Label_list[-2].grid_forget()

            self.drop3.grid(column=1, row=9)

            self.title4.grid(column=0, row=9, padx=0, pady=3, sticky=tk.W)

            self._create_enter_button()

        elif e == self.Equation_opts[2]: # one way wave

            self.MyButton.grid_forget()

            self.Label_list[-1].grid(row=8,column=0, padx=0, pady=3, sticky=tk.W)

            self.Entry_list[-1].grid(row=8,column=1, padx=5, pady=5)

            self.Entry_list[-2].grid_forget()

            self.Label_list[-2].grid_forget()

            self.drop3.grid(column=1, row=9)

            self.title4.grid(column=0, row=9, padx=0, pady=3, sticky=tk.W)

            self._create_enter_button()

        elif e == self.Equation_opts[0]: # heat wave!

            self.drop3.grid_forget()

            self.title4.grid_forget()

            if self.Entry_list_Sin_Sinc:

                for i in range(0, len(self.values_to_insert_sin_sinc)):

                    self.Entry_list_Sin_Sinc[i].grid_forget()

                    self.Label_list_Sin_Sinc[i].grid_forget()

                self.Entry_list_Sin_Sinc.clear()

                self.Label_list_Sin_Sinc.clear()

            if self.Entry_list_Gaussian:

                for i in range(0, len(self.values_to_insert_Gaussian)):

                    self.Label_list_Gaussian[i].grid_forget()

                    self.Entry_list_Gaussian[i].grid_forget()

                self.Entry_list_Gaussian.clear()

                self.Label_list_Gaussian.clear()

            self.MyButton.grid_forget()

            self.Label_list[-2].grid(row=8, column=0, padx=0, pady=3, sticky=tk.W)

            self.Entry_list[-2].grid(row=8, column=1, padx=5, pady=5)

            self.Entry_list[-1].grid_forget()

            self.Label_list[-1].grid_forget()

            self._create_enter_button()

    def _create_enter_button(self):
        """
        This method creates the button that saves the entered values.
        """
        self.MyButton = tk.Button(self.sub_frm, text='Solve Equation',
                                  command=self._click_solve_equation)

        self.MyButton.grid(sticky='n', padx=5, pady=5)

    def _make_drop_down_list(self):
        """
        This method creates a dropdown list to choose the equation type.
        """
        self.title3 = tk.Label(self.main_frm,
                               text='Choose equation: ',
                               font=('Helvatical bold', 10))

        self.title3.grid(column=0, row=0, padx=5, pady=5)

        oMenuWidth = len(max(self.Equation_opts, key=len))

        self.Drop = tk.OptionMenu(self.main_frm, self.Equation_type, *self.Equation_opts,
                                  command=self._show_special_entries_and_save_choice)

        self.Drop.config(width=oMenuWidth)

        self.Drop.grid(column=0, row=1)

    # When you click solve, this is called!
    def _click_solve_equation(self):
        """
        This method saves the input from the entries.
        """
        try:
            self.initial_condition = self.Entry_list[0].get()

            self.Number_of_cells = self.Entry_list[1].get()

            self.x_max = self.Entry_list[2].get()

            self.boundry_value_at_x0 = self.Entry_list[3].get()

            self.Number_of_cycles = self.Entry_list[4].get()

            self.Final_time = self.Entry_list[5].get()

            self.Alpha = self.Entry_list[6].get()
        except:
            self._error_message("Error in Equation form")
            return

        if self.Chosen_equation == self.Equation_opts[0]: # Heat wave
            max_x = float(self.Entry_label_dict["x_max:"].get())
            nx = int(self.Entry_label_dict["Number of Cells (nx):"].get())
            max_t = float(self.Entry_label_dict["Final time:"].get())
            nt = int(self.Entry_label_dict["Number cycles:"].get())
            alpha = float(self.Entry_label_dict["Alpha:"].get())
            b_val = float(self.Entry_label_dict["Boundry value at x0:"].get())
            init_val = float(self.Entry_label_dict["Initial condition:"].get())
            self.eq = equation.Diffusion1D(max_x, nx, max_t, nt, alpha, b_val, init_val)
            self.plot_gui.set_equation(self.eq)
            self.eq.solve()

        if self.Chosen_equation == self.Equation_opts[2]:  # One way wave
            max_x = float(self.Entry_label_dict_wave["x_max:"].get())
            nx = int(self.Entry_label_dict_wave["Number of Cells (nx):"].get())
            max_t = float(self.Entry_label_dict_wave["Final time:"].get())
            nt = int(self.Entry_label_dict_wave["Number cycles:"].get())
            Velocity = float(self.Entry_label_dict_wave["Velocity:"].get())
            self.eq = equation.Wave1D(max_x, nx, max_t, nt, Velocity)
            self.plot_gui.set_equation(self.eq)
            self.eq.solve()

        # Re'em: Shaya, this is logically wrong, if the above if occurs, this if we never occur... its the same if
        # Please change this..
        elif self.Chosen_equation == self.Equation_opts[2]:

            self.Velocity = self.Entry_list[7].get()

        if (self.Equation_opts[1] or self.Equation_opts[2]) and (self.Chosen_initial_condition_form == 'Sinc wave' or
                                               self.Chosen_initial_condition_form == 'Sine wave'
        ) and self.Entry_list_Sin_Sinc:

            self.Amplitude_Sin_Sinc = self.Entry_list_Sin_Sinc[0].get()

            self.Phase = self.Entry_list_Sin_Sinc[1].get()

            self.Wave_vector = self.Entry_list_Sin_Sinc[2].get()

        elif (self.Equation_opts[1] or self.Equation_opts[2]) and (self.Chosen_initial_condition_form ==
                                                                   'Gaussian') and self.Entry_list_Gaussian:

            self.Amplitude_Gaussian = self.Entry_list_Gaussian[0].get()

            self.Sigma = self.Entry_list_Gaussian[1].get()

            self.Mu = self.Entry_list_Gaussian[2].get()


    def _create_initial_func_drop_down_list(self):

        oMenuWidth1 = len(max(self.Initial_func, key=len))

        self.title4 = tk.Label(self.sub_frm,
                               text='Choose initial condition form: ',
                               font=('Helvatical bold', 10))

        self.clicked3 = tk.StringVar()

        self.drop3 = tk.OptionMenu(self.sub_frm, self.clicked3, *self.Initial_func,
        command = self._get_from_initial_func_drop_down_list)

        self.drop3.config(width=oMenuWidth1)

    def _get_from_initial_func_drop_down_list(self, e3):

        self.Chosen_initial_condition_form = self.clicked3.get()

        if self.Chosen_initial_condition_form == 'Gaussian':

            self.MyButton.grid_forget()

            if self.Entry_list_Sin_Sinc:

                for i in range(0, len(self.values_to_insert_sin_sinc)):

                    self.Entry_list_Sin_Sinc[i].grid_forget()

                    self.Label_list_Sin_Sinc[i].grid_forget()

                self.Entry_list_Sin_Sinc.clear()

                self.Label_list_Sin_Sinc.clear()

            if not(self.Entry_list_Gaussian):

                for i in range(0, len(self.values_to_insert_Gaussian)):

                    # labels
                    self.labelDir_Gaussian = tk.Label(self.sub_frm, text=self.values_to_insert_Gaussian[i])
                    self.labelDir_Gaussian.grid(row = 10 + i, column=0, padx=0, pady=3, sticky=tk.W)
                    self.Label_list_Gaussian.append(self.labelDir)

                    # textbox
                    self.myEntryGaussian = tk.Entry(self.sub_frm, borderwidth=1, width=25)
                    self.myEntryGaussian.grid(row = 10 + i, column=1, pady=3)
                    self.Entry_list_Gaussian.append(self.myEntryGaussian)
                    self.myEntryGaussian.insert(0, self.values_to_insert_Gaussian[i])

            self._create_enter_button()

        elif self.Chosen_initial_condition_form == 'Sinc wave' or self.Chosen_initial_condition_form == 'Sine wave':

            self.MyButton.grid_forget()

            if self.Entry_list_Gaussian:

                for i in range(0, len(self.values_to_insert_Gaussian)):

                    self.Entry_list_Gaussian[i].grid_forget()

                    self.Label_list_Gaussian[i].grid_forget()

                self.Entry_list_Gaussian.clear()

                self.Label_list_Gaussian.clear()

            if not(self.Entry_list_Sin_Sinc):

                for i in range(0, len(self.values_to_insert_sin_sinc)):
                    # labels
                    self.labelDir_Sin_Sinc = tk.Label(self.sub_frm, text=self.values_to_insert_sin_sinc[i])
                    self.labelDir_Sin_Sinc.grid(row=10 + i, column=0, padx=0, pady=3, sticky=tk.W)
                    self.Label_list_Sin_Sinc.append(self.labelDir_Sin_Sinc)

                    # textbox
                    self.myEntrySinSinc = tk.Entry(self.sub_frm, borderwidth=1, width=25)
                    self.myEntrySinSinc.grid(row=10 + i, column=1, pady=3)
                    self.Entry_list_Sin_Sinc.append(self.myEntrySinSinc)
                    self.myEntrySinSinc.insert(0, self.values_to_insert_sin_sinc[i])

            self._create_enter_button()







