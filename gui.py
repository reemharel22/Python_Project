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

    opts = ['Heat equation', 'Schrodinger equation',
            'One way wave equation']

    visual_opts = ['Image', 'Animation']

    Initial_func = ['Gaussian', 'Sinc wave', 'Sine wave']

    def __init__(self, controller):

        super().__init__()

        self.title('Visuquation User Interface')

        self._make_main_frame()

        self.clicked = tk.StringVar()

        self.clicked.set(self.opts[0])

        self.clicked2 = tk.StringVar()

        self.clicked2.set(self.visual_opts[0])

        self._make_drop_down_list()

        self._make_sub_frame()

        self._create_enter_button()

        self.plot_gui = plot_gui.PlotBox(self.main_frm)
        # self.plot_gui.create_figure()
        # self._create_figure()

        # self._visualiztion_type_drop_down_list()

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
        self.value = self.opts[0]
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

    def _show_special_entries_and_save_choice(self, e):
        """
        This method builds the unique entries and saves
        the choice from the dropdown list.
        """

        self.value = self.clicked.get()

        if e == self.opts[1]:

            self.MyButton.grid_forget()

            if self.Entry_list[-1].winfo_ismapped():

                self.Entry_list[-1].grid_forget()

            if self.Label_list[-1].winfo_ismapped():

                self.Label_list[-1].grid_forget()

            if self.Entry_list[-2].winfo_ismapped():

                self.Entry_list[-2].grid_forget()

            if self.Label_list[-2].winfo_ismapped():

                self.Label_list[-2].grid_forget()

            self.drop3.grid(column=1, row=9)

            self.title4.grid(column=0, row=9, padx=0, pady=3, sticky=tk.W)

            self._create_enter_button()

        elif e == self.opts[2]:

            self.MyButton.grid_forget()

            self.Label_list[-1].grid(row=8,column=0, padx=0, pady=3, sticky=tk.W)

            self.Entry_list[-1].grid(row=8,column=1, padx=5, pady=5)

            if self.Entry_list[-2].winfo_ismapped():

                self.Entry_list[-2].grid_forget()

            if self.Label_list[-2].winfo_ismapped():

                self.Label_list[-2].grid_forget()

            self.drop3.grid(column=1, row=9)

            self.title4.grid(column=0, row=9, padx=0, pady=3, sticky=tk.W)

            self._create_enter_button()

        elif e == self.opts[0]:

            print(len(self.Entry_list_Gaussian))

            print(len(self.Entry_list_Sin_Sinc))

            print(len(self.Label_list_Sin_Sinc))

            print(len(self.Label_list_Gaussian))

            if len(self.Entry_list_Sin_Sinc) != 0:

                for i in range(0, 3):

                    self.Entry_list_Sin_Sinc[i].grid_forget()

                    self.Label_list_Sin_Sinc[i].grid_forget()

            if len(self.Entry_list_Gaussian) != 0:

               for i in range(0, 3):

                    self.Label_list_Gaussian[i].grid_forget()

                    self.Entry_list_Gaussian[i].grid_forget()

            self.drop3.grid_forget()

            self.title4.grid_forget()

            self.MyButton.grid_forget()

            self.Label_list[-2].grid(row=8, column=0, padx=0, pady=3, sticky=tk.W)

            self.Entry_list[-2].grid(row=8, column=1, padx=5, pady=5)

            if self.Entry_list[-1].winfo_ismapped():

                self.Entry_list[-1].grid_forget()

            if self.Label_list[-1].winfo_ismapped():

                self.Label_list[-1].grid_forget()

            self._create_enter_button()

    def _create_enter_button(self):
        """
        This method creates the button that saves the entered values.
        """

        self.MyButton = tk.Button(self.sub_frm, text='Apply!',
                                  command=self._get_from_entries)

        self.MyButton.grid(sticky='n', padx=5, pady=5)

    def _make_drop_down_list(self):
        """
        This method creates a dropdown list to choose the equation type.
        """

        self.title3 = tk.Label(self.main_frm,
                               text='Choose equation: ',
                               font=('Helvatical bold', 10))

        self.title3.grid(column=0, row=0, padx=5, pady=5)

        oMenuWidth = len(max(self.opts, key=len))

        self.Drop = tk.OptionMenu(self.main_frm, self.clicked, *self.opts,
                                  command=self._show_special_entries_and_save_choice)

        self.Drop.config(width=oMenuWidth)

        self.Drop.grid(column=0, row=1)

    # When you click solve, this is called!
    def _get_from_entries(self):
        """
        This method saves the input from the entries.
        """
        try:
            self.var_1 = self.Entry_list[0].get()

            self.var_2 = self.Entry_list[1].get()

            self.var_3 = self.Entry_list[2].get()

            self.var_4 = self.Entry_list[3].get()

            self.var_5 = self.Entry_list[4].get()

            self.var_6 = self.Entry_list[5].get()

            self.var_7 = self.Entry_list[6].get()

        except:
            print("Error in input! Please create an error button")
            return

        if self.value == self.opts[0]: # Heat wave
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
            print("Done solving (should be as a message popup")

        #elif self.value == self.opts[1]:

        #    self.var_10 = self.Entry_list[10].get()

        elif self.value == self.opts[2]:

            self.var_8 = self.Entry_list[7].get()

    def _create_solve_button(self):
        """
        This method creates the solve button.
        """

        self.MyButton2 = tk.Button(self.main_frm, text='Start Plotting!',
        command=self._animate_equation)

        self.MyButton2.grid(column=1, row=3, sticky='n', padx=5,
                            pady=5)

    def _visualiztion_type_drop_down_list(self):
        """
        This method creates a dropdown list to choose the Visualization type.
        """
        oMenuWidth = len(max(self.visual_opts, key=len))

        self.title2 = tk.Label(self.sub_frm2,
                               text='Choose Visualization type: ',
                               font=('Helvatical bold', 10))

        self.title2.grid(column=1, row=0)
        self.type_visualization = self.visual_opts[0] # default
        self.Drop2 = tk.OptionMenu(self.sub_frm2, self.clicked2, *self.visual_opts,
                                   command=self._save_choise)

        self.Drop2.config(width=oMenuWidth)

        self.Drop2.grid(column=1, row=1)

    def _save_choise(self, e2):
        self.type_visualization = self.clicked2.get()



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

        self.value2 = self.clicked3.get()

        if self.value2 == 'Gaussian':

            self.MyButton.grid_forget()

            self.Entry_list_Sin_Sinc.clear()

            self.Label_list_Sin_Sinc.clear()

            if len(self.Entry_list_Sin_Sinc) != 0:

                for i in range(0, 3):

                    self.Entry_list_Sin_Sinc[i].grid_forget()

                    self.Label_list_Sin_Sinc[i].grid_forget()

                self.Entry_list_Sin_Sinc.clear()

                self.Label_list_Sin_Sinc.clear()

            if len(self.Entry_list_Gaussian) != 0:

                for i in range(0, 3):

                    self.Entry_list_Gaussian[i].grid_forget()

                    self.Label_list_Gaussian[i].grid_forget()

                self.Entry_list_Gaussian.clear()

                self.Label_list_Gaussian.clear()

            for i in range(0, 3):

                # labels
                self.labelDir_Gaussian = tk.Label(self.sub_frm, text=self.values_to_insert_Gaussian[i])
                self.labelDir_Gaussian.grid(row = 10 + i, column=0, padx=0, pady=3, sticky=tk.W)
                self.Label_list_Gaussian.append(self.labelDir)

                # textbox
                self.myEntryGaussian = tk.Entry(self.sub_frm, borderwidth=1, width=25)
                self.myEntryGaussian.grid(row = 10 + i, column=1, pady=3)
                self.Entry_list_Gaussian.append(self.myEntryGaussian)

            self._create_enter_button()

        elif self.value2 == 'Sinc wave' or self.value2 == 'Sine wave':

            self.MyButton.grid_forget()

            if len(self.Entry_list_Gaussian) != 0:

                for i in range(0, len(self.values_to_insert_Gaussian)):

                    self.Entry_list_Gaussian[i].grid_forget()

                    self.Label_list_Gaussian[i].grid_forget()

                self.Entry_list_Gaussian.clear()

                self.Label_list_Gaussian.clear()

            if len(self.Entry_list_Sin_Sinc) != 0:

                for i in range(0, 3):

                     self.Entry_list_Sin_Sinc[i].grid_forget()

                     self.Label_list_Sin_Sinc[i].grid_forget()

                self.Entry_list_Sin_Sinc.clear()

                self.Label_list_Sin_Sinc.clear()

            for i in range(0, 3):
                # labels
                self.labelDir_Sin_Sinc = tk.Label(self.sub_frm, text=self.values_to_insert_sin_sinc[i])
                self.labelDir_Sin_Sinc.grid(row=10 + i, column=0, padx=0, pady=3, sticky=tk.W)
                self.Label_list_Sin_Sinc.append(self.labelDir_Sin_Sinc)

                # textbox
                self.myEntrySinSinc = tk.Entry(self.sub_frm, borderwidth=1, width=25)
                self.myEntrySinSinc.grid(row=10 + i, column=1, pady=3)
                self.Entry_list_Sin_Sinc.append(self.myEntrySinSinc)

            self._create_enter_button()







