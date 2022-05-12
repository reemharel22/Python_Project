import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import default
import equation


class Gui(tk.Tk):
    PAD = 30

    subPAD = 30

    subPAD_out = 30

    Entry_list = []
    Entry_label_dict = []

    opts = ['Heat equation', 'Schrodinger equation',
            'One way wave equation']

    visual_opts = ['Image', 'Animation']



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

        self._create_figure()

        self._visualiztion_type_drop_down_list()

        self._create_solve_button()

    def main(self):

        self.mainloop()

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

        self.sub_frm.grid(column=0, row=2, padx=self.subPAD_out, pady=self.subPAD_out)

        self.values_to_insert = ['Initial condition:',
                                 'Number of Cells (nx):',
                                 'x_max:',
                                 'Boundry value at x0:',
                                 'Number cycles:',
                                 'Final time:',
                                 'Alpha:',
                                 'Potential:',
                                 'Velocity:']

        for i in range(0, len(self.values_to_insert) - 2):
            # labels
            labelDir = tk.Label(self.sub_frm, text=self.values_to_insert[i])
            labelDir.grid(row=i+1, column=0, padx=0, pady=3, sticky=tk.W)

            # textbox
            self.myEntry = tk.Entry(self.sub_frm, borderwidth=1, width=25)
            self.myEntry.grid(row=i+1, column=1, pady=3)
            self.myEntry.insert(0, default.Diffusion_default[self.values_to_insert[i]])

            self.Entry_list.append(self.myEntry)

        for j in range(0, 2):
            self.myEntry = tk.Entry(self.sub_frm, borderwidth=3, width=25)

            self.myEntry.insert(0, self.values_to_insert
            [len(self.values_to_insert) - 2 + j])

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

            self.Entry_list[-2].grid(padx=5, pady=5)

            self.Entry_list[-1].grid_forget()

            self.Entry_list[-3].grid_forget()

            self._create_enter_button()

        elif e == self.opts[2]:

            self.MyButton.grid_forget()

            self.Entry_list[-1].grid(padx=5, pady=5)

            self.Entry_list[-2].grid_forget()

            self.Entry_list[-3].grid_forget()

            self._create_enter_button()

        elif e == self.opts[0]:

            self.MyButton.grid_forget()

            self.Entry_list[-3].grid(padx=5, pady=5)

            self.Entry_list[-2].grid_forget()

            self.Entry_list[-1].grid_forget()

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

            self.var_8 = self.Entry_list[7].get()

            self.var_9 = self.Entry_list[8].get()
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
            self.eq.solve()
            print("Done solving (should be as a message popup")

        elif self.value == self.opts[1]:

            self.var_10 = self.Entry_list[10].get()

        elif self.value == self.opts[2]:

            self.var_10 = self.Entry_list[11].get()

    def _create_figure(self):
        """
        This method creates a second subframe and places a figure inside it.
        """
        self.sub_frm2 = tk.Frame(self.main_frm, highlightbackground="black",
                                 highlightthickness=2, padx=self.subPAD,
                                 pady=self.subPAD)
        self.Title = tk.Label(self.sub_frm2,
                              text='Visualization of the solution',
                              font=('Helvatical bold', 25))
        self.Title.grid(column=0, row=0)

        self.sub_frm2.grid(column=1, row=2, padx=self.subPAD_out,
                           pady=self.subPAD_out)

        self.fig = plt.Figure(figsize=(6, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self.sub_frm2)
        self.canvas.get_tk_widget().grid(column=0, row=2)


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

    def _animate_equation(self):
        print("Visual option:", self.type_visualization)
        if self.type_visualization == self.visual_opts[0]:
            self.eq.plot_image(self.fig, 1)
        elif self.type_visualization == self.visual_opts[1]:
            self.canvas.draw()

            self.eq.plot_animation(self.fig)
        self.canvas.draw()

    def _create_solve_button(self):
        """
        This method creates the solve button.
        """

        self.MyButton2 = tk.Button(self.main_frm, text='Start Plotting!',
        command=self._animate_equation)

        self.MyButton2.grid(column=1, row=3, sticky='n', padx=5,
                            pady=5)





