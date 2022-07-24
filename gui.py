import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import wave_1d
import schrodinger_1d
import default
import equation
import diffusion_1d
import plot_gui

class Gui(tk.Tk):
    """
    This class is the gui interface for the Visuquation project.
    """
    # Variables and empty lists that are used to design the user interface.
    PAD = 30
    Chosen_equation = ''
    Chosen_initial_condition_form = ''
    Entry_list = []
    Label_list = []
    Entry_list_Gaussian = []
    Label_list_Gaussian = []
    Entry_list_Sin_Sinc = []
    Label_list_Sin_Sinc = []
    Entry_label_dict = []
    Special_Entry_List = []

    # Tuple that are used to design the user interface.
    values_to_insert_Gaussian = ('Amplitude:', 'Sigma:', 'Mu:')
    values_to_insert_sin_sinc = ('Amplitude:', 'Phase:', 'Wave vector:')
    Equation_opts = ('Heat equation', 'Schrodinger equation', 'One way wave equation')
    Initial_func = ('Gaussian', 'Sinc wave', 'Sine wave')
    potential_type_list = ('harmonic potential', 'Gaussian potential')
    values_to_insert = ('Initial condition:', 'Number of Cells (nx):', 'x_max:', 'Boundry value at x0:',
                        'Number cycles:', 'Final time:', 'Alpha:', 'Velocity:')

    def __init__(self, controller):
        super().__init__()
        self.title('Visuquation User Interface')
        self._make_main_frame()  # Creation of the main frame of the gui.

        # Variables that refers to the equation type drop-down list.
        self.Equation_type = tk.StringVar()
        self.Equation_type.set(self.Equation_opts[0])

        # These methods will be explained in the future.
        self._make_drop_down_list()
        self._make_sub_frame()
        self._create_enter_button()
        self.plot_gui = plot_gui.PlotBox(self.main_frm)
        self._create_initial_func_drop_down_list()
        self._create_potential_type_dropdown_list()

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
        self.Chosen_equation = self.Equation_opts[0]
        self.sub_frm = tk.Frame(self.main_frm, highlightbackground="black", highlightthickness=2, padx=5, pady=5)

        self.Title = tk.Label(self.sub_frm,
                              text='Please enter the following values:', font=('Helvatical bold', 10))

        self.Title.grid(column=0, row=0, pady=5)
        self.sub_frm.grid(column=0, row=2, padx=default.subPAD_out, pady=default.subPAD_out)

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
        self.labelDir = tk.Label(self.sub_frm, text=self.values_to_insert[-1])
        self.Label_list.append(self.labelDir)
        self.myEntry.insert(0, self.values_to_insert[-1])
        self.Entry_list.append(self.myEntry)
        self.Entry_label_dict = dict(zip(self.values_to_insert, self.Entry_list))

    def _show_special_entries_and_save_choice(self, choice):
        """
        This method builds the unique entries and saves the choice from the dropdown list.
        """
        self.Chosen_equation = self.Equation_type.get()
        if choice == self.Equation_opts[1]:  # Schrodinger equation.
            self.solve_button.grid_forget()
            self.Entry_list[0].grid_forget()
            self.Label_list[0].grid_forget()
            self.Entry_list[3].grid_forget()
            self.Label_list[3].grid_forget()
            self.Entry_list[-1].grid_forget()
            self.Label_list[-1].grid_forget()
            self.Entry_list[-2].grid_forget()
            self.Label_list[-2].grid_forget()
            self.drop_pot_type.grid(column=1, row=9)
            self.title_pot_type.grid(column=0, row=9, padx=0, pady=3, sticky=tk.W)
            self.drop_init_fun.grid(column=1, row=10)
            self.title_init_fun.grid(column=0, row=10, padx=0, pady=3, sticky=tk.W)
            self._create_enter_button()

            # Set default suggested values for the solution.
            for i in range(0, len(self.Entry_list)):
                if len(self.Entry_list[i].get()) != 0:
                    self.Entry_list[i].delete(0, 'end')
            self.Entry_list[1].insert(0, '400')
            self.Entry_list[2].insert(0, '20')
            self.Entry_list[4].insert(0, '400')
            self.Entry_list[5].insert(0, '5')

        elif choice == self.Equation_opts[2]:  # One way wave equation.
            self.solve_button.grid_forget()
            self.drop_pot_type.grid_forget()
            self.title_pot_type.grid_forget()
            self.Entry_list[0].grid_forget()
            self.Label_list[0].grid_forget()
            self.Entry_list[3].grid_forget()
            self.Label_list[3].grid_forget()
            self.Label_list[-1].grid(row=8,column=0, padx=0, pady=3, sticky=tk.W)
            self.Entry_list[-1].grid(row=8,column=1, padx=5, pady=5)
            self.Entry_list[-2].grid_forget()
            self.Label_list[-2].grid_forget()
            self.drop_init_fun.grid(column=1, row=10)
            self.title_init_fun.grid(column=0, row=10, padx=0, pady=3, sticky=tk.W)
            self._create_enter_button()

            # Set default suggested values for the solution.
            for i in range(0, len(self.Entry_list)):
                if len(self.Entry_list[i].get()) != 0:
                    self.Entry_list[i].delete(0, 'end')
            self.Entry_list[1].insert(0, '100')
            self.Entry_list[2].insert(0, '10')
            self.Entry_list[4].insert(0, '500')
            self.Entry_list[5].insert(0, '30')
            self.Entry_list[7].insert(0, '0.006')

        elif choice == self.Equation_opts[0]:  # Heat wave equation.
            self.drop_init_fun.grid_forget()
            self.title_init_fun.grid_forget()
            self.drop_pot_type.grid_forget()
            self.title_pot_type.grid_forget()
            if self.Entry_list_Gaussian:
                for i in range(0, len(self.values_to_insert_Gaussian)):
                    self.Entry_list_Gaussian[i].grid_forget()
            if self.Label_list_Gaussian:
                for i in range(0, len(self.values_to_insert_Gaussian)):
                    self.Label_list_Gaussian[i].grid_forget()
                self.Entry_list_Gaussian.clear()
                self.Label_list_Gaussian.clear()
            if self.Entry_list_Sin_Sinc:
                for i in range(0, len(self.values_to_insert_sin_sinc)):
                    self.Entry_list_Sin_Sinc[i].grid_forget()
            if self.Label_list_Sin_Sinc:
                for i in range(0, len(self.values_to_insert_sin_sinc)):
                    self.Label_list_Sin_Sinc[i].grid_forget()
                self.Entry_list_Sin_Sinc.clear()
                self.Label_list_Sin_Sinc.clear()
            self.solve_button.grid_forget()
            self.Entry_list[0].grid(row=1, column=1, padx=0, pady=3)
            self.Label_list[0].grid(row=1, column=0, padx=0, pady=3, sticky=tk.W)
            self.Entry_list[3].grid(row=4, column=1, padx=0, pady=3)
            self.Label_list[3].grid(row=4, column=0, padx=0, pady=3, sticky=tk.W)
            self.Label_list[-2].grid(row=8, column=0, padx=0, pady=3, sticky=tk.W)
            self.Entry_list[-2].grid(row=8, column=1, padx=5, pady=5)
            self.Entry_list[-1].grid_forget()
            self.Label_list[-1].grid_forget()
            self._create_enter_button()

            # Set default suggested values for the solution.
            for i in range(0, len(self.Entry_list)):
                if len(self.Entry_list[i].get()) != 0:
                    self.Entry_list[i].delete(0, 'end')
            self.Entry_list[0].insert(0, '0.01')
            self.Entry_list[1].insert(0, '50')
            self.Entry_list[2].insert(0, '1.5')
            self.Entry_list[3].insert(0, '100.0')
            self.Entry_list[4].insert(0, '100')
            self.Entry_list[5].insert(0, '3')
            self.Entry_list[6].insert(0, '0.01')

    def _create_enter_button(self):
        """
        This method creates the button that saves the entered values from the drop-down list.
        """
        self.solve_button = tk.Button(self.sub_frm, text='Solve Equation', command=self._click_solve_equation)
        self.solve_button.grid(sticky='n', padx=5, pady=5)

    def _make_drop_down_list(self):
        """
        This method creates a dropdown list to choose the equation type.
        """
        self.title_choose_eq = tk.Label(self.main_frm, text='Choose equation: ', font=('Helvatical bold', 10))
        self.title_choose_eq.grid(column=0, row=0, padx=5, pady=5)
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
            self.boundary_value_at_x0 = self.Entry_list[3].get()
            self.Number_of_cycles = self.Entry_list[4].get()
            self.Final_time = self.Entry_list[5].get()
            self.Alpha = self.Entry_list[6].get()
        except:
            self._error_message("Error in Equation form - did you miss an item?")
            return

        if self.Chosen_equation == self.Equation_opts[0]:  # Heat wave equation.
            try:
                max_x = float(self.Entry_label_dict["x_max:"].get())
                nx = int(self.Entry_label_dict["Number of Cells (nx):"].get())
                max_t = float(self.Entry_label_dict["Final time:"].get())
                nt = int(self.Entry_label_dict["Number cycles:"].get())
                alpha = float(self.Entry_label_dict["Alpha:"].get())
                b_val = float(self.Entry_label_dict["Boundry value at x0:"].get())
                init_val = float(self.Entry_label_dict["Initial condition:"].get())
            except:
                self._error_message("Bad input in equation data. Please insert floats or integers.")
                return
            self.eq = diffusion_1d.Diffusion1D(max_x, nx, max_t, nt, alpha, b_val, init_val)

        if (self.Chosen_equation == self.Equation_opts[1] or self.Chosen_equation == self.Equation_opts[2]) and\
                (self.Chosen_initial_condition_form == 'Sinc wave' or
                 self.Chosen_initial_condition_form == 'Sine wave') and self.Entry_list_Sin_Sinc:
            self.Amplitude_Sin_Sinc = self.Entry_list_Sin_Sinc[0].get()
            self.Phase = self.Entry_list_Sin_Sinc[1].get()
            self.Wave_vector = self.Entry_list_Sin_Sinc[2].get()

        if (self.Equation_opts[1] or self.Equation_opts[2]) and (self.Chosen_initial_condition_form == 'Gaussian') and \
                self.Entry_list_Gaussian:
            self.Amplitude_Gaussian = self.Entry_list_Gaussian[0].get()
            self.Sigma = self.Entry_list_Gaussian[1].get()
            self.Mu = self.Entry_list_Gaussian[2].get()

        if self.Chosen_equation == self.Equation_opts[2]:  # One way wave equation.
            self.Velocity = self.Entry_list[7].get()
            try:
                max_x = float(self.Entry_label_dict["x_max:"].get())
                nx = int(self.Entry_label_dict["Number of Cells (nx):"].get())
                max_t = float(self.Entry_label_dict["Final time:"].get())
                nt = int(self.Entry_label_dict["Number cycles:"].get())
                velocity = float(self.Entry_label_dict["Velocity:"].get())
                init_wave_form = self.Chosen_initial_condition_form
                if init_wave_form == 'Gaussian':
                    amplitude = float(self.Amplitude_Gaussian)
                    wave_vector_sigma = float(self.Sigma)
                    phase_mu = float(self.Mu)
                    # Assertion conditions that necessary to get a reasonable solution.
                    assert (abs(phase_mu) <= abs(max_x))
                    assert (abs(wave_vector_sigma) <= 5)
                    assert (0 < amplitude != 0)
                    assert (0 < velocity <= 0.01)
                if init_wave_form == 'Sinc wave' or init_wave_form == 'Sine wave':
                    amplitude = float(self.Amplitude_Sin_Sinc)
                    wave_vector_sigma = float(self.Wave_vector)
                    phase_mu = float(self.Phase)
                    # Assertion conditions that necessary to get a reasonable solution.
                    assert (abs(wave_vector_sigma) <= 15)
                    assert (abs(phase_mu) < max_x)
                    assert (amplitude > 0)
                    assert (0 < velocity <= 0.01)
            except ValueError:
                self._error_message("Bad input in equation data. Please insert floats or integers.")
            except AssertionError:
                if init_wave_form == 'Gaussian':
                    self._error_message('The values of Amplitude,sigma, Mu and Velocity must to be between !=0, (-5,5),'
                                        ' (-x_max,x_max), [0,0.01) respectively')
                if init_wave_form == 'Sinc wave' or init_wave_form == 'Sine wave':
                    self._error_message('The values of Amplitude, Phase, Wave vector and Velocity must to be between'
                                        ' > 0, [-x_max,x_max], (-15,15), [0,0.01) respectively')
                return
            self.eq = wave_1d.Wave1D(max_x, nx, max_t, nt, velocity, init_wave_form,
                                     amplitude, wave_vector_sigma, phase_mu)
        if self.Chosen_equation == self.Equation_opts[1]:  # Schrodinger equation.
            try:
                max_x = float(self.Entry_label_dict["x_max:"].get())
                nx = int(self.Entry_label_dict["Number of Cells (nx):"].get())
                max_t = float(self.Entry_label_dict["Final time:"].get())
                nt = int(self.Entry_label_dict["Number cycles:"].get())
                init_wave_form = self.Chosen_initial_condition_form
                potential_type = self.Chosen_potential_type
                if init_wave_form == 'Gaussian':
                    amplitude = float(self.Amplitude_Gaussian)
                    wave_vector_sigma = float(self.Sigma)
                    phase_mu = float(self.Mu)
                    # Assertion conditions that necessary to get a reasonable solution.
                    assert(abs(phase_mu) <= 15)
                    assert(abs(wave_vector_sigma) <= 5)
                    assert(0 < amplitude <= 100)
                if init_wave_form == 'Sinc wave' or init_wave_form == 'Sine wave':
                    amplitude = float(self.Amplitude_Sin_Sinc)
                    wave_vector_sigma = float(self.Wave_vector)
                    phase_mu = float(self.Phase)
                    # Assertion conditions that necessary to get a reasonable solution.
                    assert(abs(wave_vector_sigma) <= 10)
                    assert(abs(phase_mu) < max_x)
                    assert(0 < amplitude <= 100)
                if self.Chosen_potential_type == 'harmonic potential':
                    potential_type = 'harmonic potential'
                if self.Chosen_potential_type == 'Gaussian potential':
                    potential_type = 'Gaussian potential'
            except ValueError:
                self._error_message("Bad input in equation data. Please insert floats or integers.")
            except AssertionError:
                if init_wave_form == 'Gaussian':
                    self._error_message('The values of Amplitude,sigma and Mu must to be between [0,100),(-5,5),'
                                        '(-15,15) respectively')
                if init_wave_form == 'Sinc wave' or init_wave_form == 'Sine wave':
                    self._error_message('The values of Amplitude, Phase and Wave vector must to be between [0,100),'
                                        ' [-x_max,x_max],(-10,10) respectively')
                return
            self.eq = schrodinger_1d.schrodinger1D(max_x, nx, max_t, nt, init_wave_form,amplitude, wave_vector_sigma,
                                                   phase_mu, potential_type)
        self.plot_gui.set_equation(self.eq)
        self.eq.solve()

    def _create_initial_func_drop_down_list(self):
        """
        This method creates the drop-down list to choose the initial condition form.
        """
        omenuwidth1 = len(max(self.Initial_func, key=len))
        self.title_init_fun = tk.Label(self.sub_frm, text='Choose initial condition form: ', font=('Helvatical bold', 10))
        self.init_cond = tk.StringVar()
        self.init_cond.set(self.Initial_func[0])
        self.drop_init_fun = tk.OptionMenu(self.sub_frm, self.init_cond, *self.Initial_func,
                                   command=self._get_from_initial_func_drop_down_list)
        self.drop_init_fun.config(width=omenuwidth1)

    def _get_from_initial_func_drop_down_list(self, arbitrary_init):
        self.Chosen_initial_condition_form = self.init_cond.get()
        if self.Chosen_initial_condition_form == 'Gaussian':
            self.solve_button.grid_forget()
            if self.Entry_list_Sin_Sinc:
                for i in range(0, len(self.values_to_insert_sin_sinc)):
                    self.Label_list_Sin_Sinc[i].grid_forget()
                    self.Entry_list_Sin_Sinc[i].grid_forget()
                self.Entry_list_Sin_Sinc.clear()
                self.Label_list_Sin_Sinc.clear()
            if not self.Entry_list_Gaussian:
                for i in range(0, len(self.values_to_insert_Gaussian)):
                    # labels
                    self.labelDir_Gaussian = tk.Label(self.sub_frm, text=self.values_to_insert_Gaussian[i])
                    self.labelDir_Gaussian.grid(row = 11 + i, column=0, padx=0, pady=3, sticky=tk.W)
                    self.Label_list_Gaussian.append(self.labelDir_Gaussian)
                    # textbox
                    self.myEntryGaussian = tk.Entry(self.sub_frm, borderwidth=1, width=25)
                    self.myEntryGaussian.grid(row = 11 + i, column=1, pady=3)
                    self.Entry_list_Gaussian.append(self.myEntryGaussian)

            # Default values.
            if len(self.Entry_list_Gaussian[0].get()) == 0:
                self.Entry_list_Gaussian[0].insert(0, '10')
                self.Entry_list_Gaussian[1].insert(0, '1')
                self.Entry_list_Gaussian[2].insert(0, '-5')
            self._create_enter_button()
        elif self.Chosen_initial_condition_form == 'Sinc wave' or self.Chosen_initial_condition_form == 'Sine wave':
            self.solve_button.grid_forget()
            if self.Entry_list_Gaussian:
                for i in range(0, len(self.values_to_insert_Gaussian)):
                    self.Label_list_Gaussian[i].grid_forget()
                    self.Entry_list_Gaussian[i].grid_forget()
                self.Entry_list_Gaussian.clear()
                self.Label_list_Gaussian.clear()
            if not self.Entry_list_Sin_Sinc:
                for i in range(0, len(self.values_to_insert_sin_sinc)):
                    # labels
                    self.labelDir_Sin_Sinc = tk.Label(self.sub_frm, text=self.values_to_insert_sin_sinc[i])
                    self.labelDir_Sin_Sinc.grid(row=11 + i, column=0, padx=0, pady=3, sticky=tk.W)
                    self.Label_list_Sin_Sinc.append(self.labelDir_Sin_Sinc)
                    # textbox
                    self.myEntrySinSinc = tk.Entry(self.sub_frm, borderwidth=1, width=25)
                    self.myEntrySinSinc.grid(row=11 + i, column=1, pady=3)
                    self.Entry_list_Sin_Sinc.append(self.myEntrySinSinc)
                    #self.myEntrySinSinc.insert(0, self.values_to_insert_sin_sinc[i])
            # Default values.
            if len(self.Entry_list_Sin_Sinc[0].get()) == 0:
                self.Entry_list_Sin_Sinc[0].insert(0, '10')
                self.Entry_list_Sin_Sinc[1].insert(0, '1')
                self.Entry_list_Sin_Sinc[2].insert(0, '-5')
            self._create_enter_button()

    def _create_potential_type_dropdown_list(self):
        omenuwidth2 = len(max(self.potential_type_list, key=len))
        self.title_pot_type = tk.Label(self.sub_frm, text='Choose potential type: ', font=('Helvatical bold', 10))
        self.pot_type = tk.StringVar()
        self.pot_type.set(self.potential_type_list[1])
        self.drop_pot_type = tk.OptionMenu(self.sub_frm, self.pot_type, *self.potential_type_list,
                                   command=self._get_from_potential_type_drop_down_list)
        self.drop_pot_type.config(width=omenuwidth2)

    def _get_from_potential_type_drop_down_list(self, arbitrary_pot):
        self.Chosen_potential_type = self.pot_type.get()






