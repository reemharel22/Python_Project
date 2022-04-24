import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class Gui(tk.Tk):
    PAD = 80

    subPAD = 50

    subPAD_out = 30

    Entry_list = []

    opts = ['Heat equation', 'Schrodinger equation',
            'One way wave equation']

    def __init__(self, controller):

        super().__init__()

        self.title('Visuquation User Interface')

        self._make_main_frame()

        self.clicked = tk.StringVar()

        self.clicked.set(self.opts[0])

        self._make_drop_down_list()

        self._make_sub_frame()

        self._create_enter_button()

        self._create_figure()

    def main(self):

        self.mainloop()

    def _make_main_frame(self):

        self.main_frm = ttk.Frame(self)

        self.main_frm.grid(padx=self.PAD, pady=self.PAD)

    def _make_sub_frame(self):

        self.sub_frm = tk.Frame(self.main_frm, highlightbackground="black",
                                highlightthickness=2, padx=self.subPAD,
                                pady=self.subPAD)

        self.Title = tk.Label(self.sub_frm,
                              text='Please enter initial values:',
                              font=('Helvatical bold', 15))

        self.Title.grid(column=0, row=0, padx=5, pady=5)

        self.sub_frm.grid(column=0, row=1, padx=self.subPAD_out, pady=self.subPAD_out)

        self.values_to_insert = ['Enter initial condition:', 'Enter initial time:',
                                 'Enter final time:', 'Enter initial position:',
                                 'Enter final position:', 'Enter time step size:',
                                 'Enter position step size:', 'Enter the potential:',
                                 'Enter the velocity:']

        for i in range(0, len(self.values_to_insert) - 2):
            self.myEntry = tk.Entry(self.sub_frm, borderwidth=3, width=25)

            self.myEntry.grid(padx=5, pady=5)

            self.myEntry.insert(0, self.values_to_insert[i])

            self.Entry_list.append(self.myEntry)

        for j in range(0, 2):
            self.myEntry = tk.Entry(self.sub_frm, borderwidth=3, width=25)

            self.myEntry.insert(0, self.values_to_insert
            [len(self.values_to_insert) - 2 + j])

            self.Entry_list.append(self.myEntry)

    def _show_special_entries_and_save_choice(self, e):
        """
        This method builds the unique entries and saves
        the choice from the dropdown list.
        """

        global value

        value = self.clicked.get()
        # Print to check.
        print(value)

        if e == self.opts[1]:

            self.MyButton.grid_forget()

            self.Entry_list[-2].grid(padx=5, pady=5)

            self.Entry_list[-1].grid_forget()

            self._create_enter_button()

        elif e == self.opts[2]:

            self.MyButton.grid_forget()

            self.Entry_list[-1].grid(padx=5, pady=5)

            self.Entry_list[-2].grid_forget()

            self._create_enter_button()

        elif e == self.opts[0]:

            self.Entry_list[-2].grid_forget()

            self.Entry_list[-1].grid_forget()

    def _create_enter_button(self):
        """
        This method creates the button that saves the entered values.
        """

        self.MyButton = tk.Button(self.sub_frm, text='Enter',
                                  command=self._get_from_entries)

        self.MyButton.grid(sticky='n', padx=5, pady=5)

    def _make_drop_down_list(self):
        """
        This method creates a dropdown list.
        """
        o_menu_width = len(max(self.opts, key=len))

        self.Drop = tk.OptionMenu(self.main_frm, self.clicked, *self.opts,
                                  command=self._show_special_entries_and_save_choice)

        self.Drop.config(width=o_menu_width)

        self.Drop.grid(column=0, row=0)

    def _get_from_entries(self):
        """
        This method saves the input from the entries.
        """
        global var_1
        global var_2
        global var_3
        global var_4
        global var_5
        global var_6
        global var_7
        global var_8
        global var_9
        var_1 = self.Entry_list[0].get()
        var_2 = self.Entry_list[1].get()
        var_3 = self.Entry_list[2].get()
        var_4 = self.Entry_list[3].get()
        var_5 = self.Entry_list[4].get()
        var_6 = self.Entry_list[5].get()
        var_7 = self.Entry_list[6].get()
        var_8 = self.Entry_list[7].get()
        var_9 = self.Entry_list[8].get()
        # Print to check.
        print(var_1)
        print(var_2)
        print(var_3)
        print(var_4)
        print(var_5)
        print(var_6)
        print(var_7)
        print(var_8)
        print(var_9)

    def _create_figure(self):
        self.sub_frm2 = tk.Frame(self.main_frm, highlightbackground="black",
                                 highlightthickness=2, padx=self.subPAD,
                                 pady=self.subPAD)
        self.Title = tk.Label(self.sub_frm2,
                              text='Animation of the solution',
                              font=('Helvatical bold', 30))
        self.Title.grid(column=0, row=0)

        self.sub_frm2.grid(column=1, row=1, padx=self.subPAD_out,
                           pady=self.subPAD_out)

        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self.sub_frm2)
        self.canvas.get_tk_widget().grid()
        self.canvas.draw()





