import tkinter as tk
from tkinter import messagebox
import default
import diffusion_1d
import wave_1d
import schrodinger_1d
import plot_gui

class Gui(tk.Tk):
    """
    Welcome to Gui. this class is the gui interface for the Visuquation project.
    """
    # Assertion checks Variables.
    max_t_min = 0
    nt_min = 30
    nt_max = 20000
    max_ratio = 150
    max_x_min = 0
    nx_min = 30
    nx_max = 1000
    wave_vector_sigma_max_gauss_wave = 5
    wave_vector_sigma_max_sin_sinc_wave = 15
    wave_vector_sigma_max_gauss_sh = 5
    wave_vector_sigma_max_sin_sinc_sh = 10
    velocity_min = 0
    velocity_max = 0.01
    phase_mu_max = 15
    amplitude_max = 100
    amplitude_min = 0
    min_ratio_time_dif = 20
    min_ratio_dif = 20
    max_ratio_dif = 50
    nt_max_dif = 400
    nt_min_dif = 10
    max_t_min_dif = 1
    b_val_min = 1
    b_val_max = 1000
    alpha_min = 0.001
    alpha_max = 0.01
    nx_max_dif = 2000
    nx_min_dif = 10
    init_val_min = 0
    stability_wave_lower_bound = 0
    stability_wave_upper_bound = 1

    # Variables and empty lists that are used to create the user interface.
    Chosen_potential_type = ''
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

    # Tuple that are used to create the user interface.
    values_to_insert_Gaussian = ('Amplitude:', 'Sigma:', 'Mu:')
    values_to_insert_sin_sinc = ('Amplitude:', 'Phase:', 'Wave vector:')
    Equation_opts = ('Heat equation', 'Schrodinger equation', 'One way wave equation')
    Initial_func = ('Gaussian', 'Sinc wave', 'Sine wave')
    potential_type_list = ('harmonic potential', 'Gaussian potential')
    values_to_insert = ('Initial condition:', 'Number of Cells (nx):', 'x_max:', 'Boundary value at x0:',
                        'Number cycles:', 'Final time:', 'Alpha:', 'Velocity:')

    # Dictionaries for default values.
    default_Schrodinger_dict = {'nx': 400, 'x_max': 20, 'nt': 400, 't_max': 5}
    default_wave_dict = {'nx': 100, 'x_max': 10, 'nt': 500, 't_max': 30, 'velocity': 0.006}
    default_heat_dict = {'init': 0.01, 'nx': 50, 'x_max': 1.5, 'b_val': 100.0, 'nt': 100, 't_max': 3, 'alpha': 0.01}
    default_init_condition = {'amplitude': 10, 'phase/sigma': 1, 'wave_vector/mu': -5}

    def __init__(self, controller):
        super().__init__()
        self.configure(bg='black')  # Set background color.
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
        self.main_frm = tk.Frame(self)
        self.main_frm.grid(padx=30, pady=30)
        self.main_frm.config(bg="black")

    def _make_sub_frame(self):
        """
        This method creates a subframe and places Entries inside.
        """
        self.Chosen_equation = self.Equation_opts[0]
        self.sub_frm = tk.Frame(self.main_frm, highlightbackground="black", highlightthickness=2, padx=2, pady=5)

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

        self.myEntry = tk.Entry(self.sub_frm, borderwidth=1, width=25)
        self.labelDir = tk.Label(self.sub_frm, text=self.values_to_insert[-1])
        self.Label_list.append(self.labelDir)
        self.myEntry.insert(0, self.values_to_insert[-1])
        self.Entry_list.append(self.myEntry)
        self.Entry_label_dict = dict(zip(self.values_to_insert, self.Entry_list))

    def _show_special_entries_and_save_choice(self, choice):
        """
        This method builds the unique entries and the second sub-frame structure by calling the correct function
        according to the option menu choice by the user.
        """
        self.Chosen_equation = self.Equation_type.get()
        if choice == self.Equation_opts[1]:  # Schrodinger equation.
            self.choose_schrodinger()
        elif choice == self.Equation_opts[2]:  # One way wave equation.
            self.choose_wave()
        elif choice == self.Equation_opts[0]:  # Heat equation.
            self.choose_heat()

    def _create_enter_button(self):
        """
        This method creates the button that saves the entered values from the drop-down list.
        """
        self.solve_button = tk.Button(self.sub_frm, text='Solve Equation', command=self._click_solve_equation)
        self.solve_button.grid(sticky='n', padx=5, pady=5)

    def _make_drop_down_list(self):
        """
        This method creates a drop-down list to choose the equation type.
        """
        self.title_choose_eq = tk.Label(self.main_frm, text='Choose equation: ', font=('Helvatical bold', 10))
        self.title_choose_eq.grid(column=0, row=0, padx=5, pady=5)
        oMenuWidth = len(max(self.Equation_opts, key=len))
        self.Drop = tk.OptionMenu(self.main_frm, self.Equation_type, *self.Equation_opts,
                                  command=self._show_special_entries_and_save_choice)
        self.Equation_type.set(self.Equation_opts[0])
        self.Drop.config(width=oMenuWidth)
        self.Drop.grid(column=0, row=1)

    def _click_solve_equation(self):
        """
        This method saves the input from the entries and checks the input by calling the relevant functions,
        this method is called When the user clicks solve equation button.
        """
        try:
            self.initial_condition = self.Entry_list[0].get()
            self.Number_of_cells = self.Entry_list[1].get()
            self.x_max = self.Entry_list[2].get()
            self.boundary_value_at_x0 = self.Entry_list[3].get()
            self.Number_of_cycles = self.Entry_list[4].get()
            self.Final_time = self.Entry_list[5].get()
            self.Alpha = self.Entry_list[6].get()
        except ValueError:
            self._error_message("Error in Equation form - did you miss an item?")
            return None
        if self.Chosen_equation == self.Equation_opts[0]:  # Heat wave equation.
            self.solve_clicked_when_heat_chosen()
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
            self.solve_clicked_when_wave_chosen()
        if self.Chosen_equation == self.Equation_opts[1]:  # Schrodinger equation.
            self.solve_clicked_when_schrodinger_chosen()
        self.plot_gui.set_equation(self.eq)
        self.eq.solve()

    def _create_initial_func_drop_down_list(self):
        """
        This method creates the drop-down list to choose the initial condition form.
        """
        omenuwidth1 = len(max(self.Initial_func, key=len))
        self.title_init_fun = tk.Label(self.sub_frm, text='Choose initial condition form: ', font=('Helvatical bold',
                                                                                                   10))
        self.init_cond = tk.StringVar()
        self.init_cond.set(self.Initial_func[0])
        self.drop_init_fun = tk.OptionMenu(self.sub_frm, self.init_cond, *self.Initial_func,
                                   command=self._get_from_initial_func_drop_down_list)
        self.drop_init_fun.config(width=omenuwidth1)

    def _get_from_initial_func_drop_down_list(self, arbitrary_init):
        """
        This method fits the relevant frame according to the initial condition option menu choice of the user by calling
        the relevant function.
        """
        self.Chosen_initial_condition_form = self.init_cond.get()
        if self.Chosen_initial_condition_form == 'Gaussian':
            self.choose_gaussian()
        elif self.Chosen_initial_condition_form == 'Sinc wave' or self.Chosen_initial_condition_form == 'Sine wave':
            self.choose_sin_sinc()

    def _create_potential_type_dropdown_list(self):
        """
        This method creates the potential type option menu.
        """
        omenuwidth2 = len(max(self.potential_type_list, key=len))
        self.title_pot_type = tk.Label(self.sub_frm, text='Choose potential type: ', font=('Helvatical bold', 10))
        self.pot_type = tk.StringVar()
        self.pot_type.set(self.potential_type_list[1])
        self.drop_pot_type = tk.OptionMenu(self.sub_frm, self.pot_type, *self.potential_type_list,
                                           command=self._get_from_potential_type_drop_down_list)
        self.drop_pot_type.config(width=omenuwidth2)

    def _get_from_potential_type_drop_down_list(self, arbitrary_pot):
        """
        This method gets the potential type from the relevant option menu.
        """
        self.Chosen_potential_type = self.pot_type.get()

    def choose_schrodinger(self):
        """
        This method is called when the user chooses the Schrodinger equation at the option menu and fits the gui
        accordingly.
        """
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
        self.Entry_list[1].insert(0, self.default_Schrodinger_dict['nx'])
        self.Entry_list[2].insert(0, self.default_Schrodinger_dict['x_max'])
        self.Entry_list[4].insert(0, self.default_Schrodinger_dict['nt'])
        self.Entry_list[5].insert(0, self.default_Schrodinger_dict['t_max'])

    def choose_wave(self):
        """
        This method is called when the user chooses the wave equation at the option menu and fits the gui accordingly.
        """
        self.solve_button.grid_forget()
        self.drop_pot_type.grid_forget()
        self.title_pot_type.grid_forget()
        self.Entry_list[0].grid_forget()
        self.Label_list[0].grid_forget()
        self.Entry_list[3].grid_forget()
        self.Label_list[3].grid_forget()
        self.Label_list[-1].grid(row=8, column=0, padx=0, pady=3, sticky=tk.W)
        self.Entry_list[-1].grid(row=8, column=1, padx=0, pady=3, sticky=tk.W)
        self.Entry_list[-2].grid_forget()
        self.Label_list[-2].grid_forget()
        self.drop_init_fun.grid(column=1, row=10)
        self.title_init_fun.grid(column=0, row=10, padx=0, pady=3, sticky=tk.W)
        self._create_enter_button()

        # Set default suggested values for the solution.
        for i in range(0, len(self.Entry_list)):
            if len(self.Entry_list[i].get()) != 0:
                self.Entry_list[i].delete(0, 'end')
        self.Entry_list[1].insert(0, self.default_wave_dict['nx'])
        self.Entry_list[2].insert(0, self.default_wave_dict['x_max'])
        self.Entry_list[4].insert(0, self.default_wave_dict['nt'])
        self.Entry_list[5].insert(0, self.default_wave_dict['t_max'])
        self.Entry_list[7].insert(0, self.default_wave_dict['velocity'])

    def choose_heat(self):
        """
        This method is called when the user chooses the heat equation at the option menu and fits the gui accordingly.
        """
        self.drop_init_fun.grid_forget()
        self.title_init_fun.grid_forget()
        self.drop_pot_type.grid_forget()
        self.title_pot_type.grid_forget()
        if self.Label_list_Gaussian:
            for i in range(0, len(self.values_to_insert_Gaussian)):
                self.Entry_list_Gaussian[i].grid_forget()
                self.Label_list_Gaussian[i].grid_forget()
            self.Entry_list_Gaussian.clear()
            self.Label_list_Gaussian.clear()
        if self.Label_list_Sin_Sinc:
            for i in range(0, len(self.values_to_insert_sin_sinc)):
                self.Entry_list_Sin_Sinc[i].grid_forget()
                self.Label_list_Sin_Sinc[i].grid_forget()
            self.Entry_list_Sin_Sinc.clear()
            self.Label_list_Sin_Sinc.clear()
        self.solve_button.grid_forget()
        self.Entry_list[0].grid(row=1, column=1, padx=0, pady=3, sticky=tk.W)
        self.Label_list[0].grid(row=1, column=0, padx=0, pady=3, sticky=tk.W)
        self.Entry_list[3].grid(row=4, column=1, padx=0, pady=3, sticky=tk.W)
        self.Label_list[3].grid(row=4, column=0, padx=0, pady=3, sticky=tk.W)
        self.Label_list[-2].grid(row=8, column=0, padx=0, pady=3, sticky=tk.W)
        self.Entry_list[-2].grid(row=8, column=1, padx=0, pady=3, sticky=tk.W)
        self.Entry_list[-1].grid_forget()
        self.Label_list[-1].grid_forget()
        self._create_enter_button()

        # Set default suggested values for the solution.
        for i in range(0, len(self.Entry_list)):
            if len(self.Entry_list[i].get()) != 0:
                self.Entry_list[i].delete(0, 'end')
        self.Entry_list[0].insert(0, self.default_heat_dict['init'])
        self.Entry_list[1].insert(0, self.default_heat_dict['nx'])
        self.Entry_list[2].insert(0, self.default_heat_dict['x_max'])
        self.Entry_list[3].insert(0, self.default_heat_dict['b_val'])
        self.Entry_list[4].insert(0, self.default_heat_dict['nt'])
        self.Entry_list[5].insert(0, self.default_heat_dict['t_max'])
        self.Entry_list[6].insert(0, self.default_heat_dict['alpha'])

    def choose_gaussian(self):
        """
        This method is called when the user chooses the Gaussian initial condition at the option menu and fits the gui
        accordingly.
        """
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
                self.labelDir_Gaussian.grid(row=11 + i, column=0, padx=0, pady=3, sticky=tk.W)
                self.Label_list_Gaussian.append(self.labelDir_Gaussian)
                # textbox
                self.myEntryGaussian = tk.Entry(self.sub_frm, borderwidth=1, width=25)
                self.myEntryGaussian.grid(row=11 + i, column=1, pady=3)
                self.Entry_list_Gaussian.append(self.myEntryGaussian)
        # Default values.
        if len(self.Entry_list_Gaussian[0].get()) == 0:
            self.Entry_list_Gaussian[0].insert(0, self.default_init_condition['amplitude'])
            self.Entry_list_Gaussian[1].insert(0, self.default_init_condition['phase/sigma'])
            self.Entry_list_Gaussian[2].insert(0, self.default_init_condition['wave_vector/mu'])
        self._create_enter_button()

    def choose_sin_sinc(self):
        """
        This method is called when the user chooses the sin or sinc initial condition at the option menu and fits the gui
        accordingly.
        """
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
        # Default values.
        if len(self.Entry_list_Sin_Sinc[0].get()) == 0:
            self.Entry_list_Sin_Sinc[0].insert(0, self.default_init_condition['amplitude'])
            self.Entry_list_Sin_Sinc[1].insert(0, self.default_init_condition['phase/sigma'])
            self.Entry_list_Sin_Sinc[2].insert(0, self.default_init_condition['wave_vector/mu'])
        self._create_enter_button()

    def solve_clicked_when_heat_chosen(self):
        """
        This method is called when the user chooses the heat equation and clicks "solve equation". This method checks the
        input related to this specific equation.
        """
        try:
            max_x = float(self.Entry_label_dict["x_max:"].get())
            nx = int(self.Entry_label_dict["Number of Cells (nx):"].get())
            max_t = float(self.Entry_label_dict["Final time:"].get())
            nt = int(self.Entry_label_dict["Number cycles:"].get())
            alpha = float(self.Entry_label_dict["Alpha:"].get())
            b_val = float(self.Entry_label_dict["Boundary value at x0:"].get())
            init_val = float(self.Entry_label_dict["Initial condition:"].get())
            assert (nt / max_t >= self.min_ratio_time_dif)
            assert (self.nt_min_dif <= nt <= self.nt_max_dif)
            assert (self.max_t_min_dif <= max_t)
            assert (self.b_val_min <= b_val < self.b_val_max)
            assert (self.alpha_min <= alpha <= self.alpha_max)
            assert (self.min_ratio_dif <= nx / max_x <= self.max_ratio_dif)
            assert (self.nx_min_dif <= nx <= self.nx_max_dif)
            assert (self.init_val_min < init_val < b_val)
            self.eq = diffusion_1d.Diffusion1D(max_x, nx, max_t, nt, alpha, b_val, init_val)
        except ValueError:
            self._error_message("Bad input in equation data. Please insert floats or integers.")
        except AssertionError:
            self._error_message(f'The values of initial condition, nx, boundary value at x0, Number cycles, '
                                f'final time and Alpha must satisfy: ({self.nx_min_dif}, {self.nx_max_dif}), '
                                f'({self.b_val_min}, {self.b_val_max}], ({self.nt_min_dif}, {self.nt_max_dif}), '
                                f'>= {self.max_t_min_dif}, ({self.alpha_min}, {self.alpha_max}) respectively. '
                                f'Also, nt/max_t >= {self.min_ratio_time_dif} and nx/max_x must to be inside the '
                                f'range: ({self.min_ratio_dif}, {self.max_ratio_dif}).')

    def solve_clicked_when_wave_chosen(self):
        """
        This method is called when the user chooses the wave equation and clicks "solve equation", this method checks
        the input related to this specific equation.
        """
        if self.Chosen_initial_condition_form == '':
            self._error_message('you have to set the initial condition from the relevant option menu.')
            return None
        try:
            nt = int(self.Entry_label_dict["Number cycles:"].get())
            max_t = float(self.Entry_label_dict["Final time:"].get())
            # Assertion conditions that necessary to get a reasonable solution.
            assert (self.max_t_min < max_t and self.nt_min <= nt <= self.nt_max and nt / max_t < self.max_ratio)
        except ValueError:
            self._error_message('Bad input in data, Number cycles must be integer and Final time must be float'
                                ' (or integer).')
            return None
        except AssertionError:
            self._error_message(f'The values of Final time and Number cycles must satisfy the conditions: '
                                f'{self.max_t_min} < Final time, {self.nt_min} <= Number cycles <= {self.nt_max}'
                                f' and Number cycles/Final time < {self.max_ratio}.')
            return None
        try:
            max_x = float(self.Entry_label_dict["x_max:"].get())
            nx = int(self.Entry_label_dict["Number of Cells (nx):"].get())
            # Assertion conditions that necessary to get a reasonable solution.
            assert (self.max_x_min < max_x < nx / 2)
            assert (self.nx_min < nx < self.nx_max)
        except ValueError:
            self._error_message('Bad input in data, nx must be integer and x_max must be float (or integer).')
            return None
        except AssertionError:
            self._error_message(f'The values of x_max and nx must to be between [{self.max_x_min}, {nx}/2], '
                                f'[{self.nx_min}, {self.nx_max}], respectively.')
            return None
        try:
            velocity = float(self.Entry_label_dict["Velocity:"].get())
            init_wave_form = self.Chosen_initial_condition_form
            # Euler's method stability condition.
            assert (self.stability_wave_lower_bound < velocity*(max_t/max_x)*((nx+1)/(nt+1)) <=
                    self.stability_wave_upper_bound)
            if init_wave_form == 'Gaussian':
                amplitude = float(self.Amplitude_Gaussian)
                wave_vector_sigma = float(self.Sigma)
                phase_mu = float(self.Mu)
                # Assertion conditions that necessary to get a reasonable solution.
                assert (abs(phase_mu) <= abs(max_x))
                assert (abs(wave_vector_sigma) <= self.wave_vector_sigma_max_gauss_wave)
                assert (0 < amplitude != 0)
                assert (self.velocity_min < velocity <= self.velocity_max)
            if init_wave_form == 'Sinc wave' or init_wave_form == 'Sine wave':
                amplitude = float(self.Amplitude_Sin_Sinc)
                wave_vector_sigma = float(self.Wave_vector)
                phase_mu = float(self.Phase)
                # Assertion conditions that necessary to get a reasonable solution.
                assert (abs(wave_vector_sigma) <= self.wave_vector_sigma_max_sin_sinc_wave)
                assert (abs(phase_mu) < max_x)
                assert (amplitude > 0)
                assert (self.velocity_min < velocity <= self.velocity_max)
        except ValueError:
            self._error_message("Bad input in equation data. Please insert floats or integers.")
            return None
        except AssertionError:
            if init_wave_form == 'Gaussian':
                self._error_message(f'The values of Amplitude,sigma, Mu and Velocity must to be between !=0,'
                                    f' (-{self.wave_vector_sigma_max_gauss_wave},'
                                    f' {self.wave_vector_sigma_max_gauss_wave}), (-x_max, x_max),'
                                    f' [{self.velocity_min}, {self.velocity_max}) respectively. Also, the known '
                                    f'stability condition must be true.')
            if init_wave_form == 'Sinc wave' or init_wave_form == 'Sine wave':
                self._error_message(f'The values of Amplitude, Phase, Wave vector and Velocity must to be between'
                                    f' > 0, [-x_max, x_max], (-{self.wave_vector_sigma_max_sin_sinc_wave},'
                                    f'{self.wave_vector_sigma_max_sin_sinc_wave}), [{self.velocity_min},'
                                    f'{self.velocity_max}) respectively. Also, the known stability condition must be'
                                    f' true')
                return None
        self.eq = wave_1d.Wave1D(max_x, nx, max_t, nt, velocity, init_wave_form,
                                 amplitude, wave_vector_sigma, phase_mu)

    def solve_clicked_when_schrodinger_chosen(self):
        """
        This method is called when the user chooses the Schrodinger equation and clicks "solve equation". This method checks the
        input related to this specific equation.
        """
        if self.Chosen_initial_condition_form == '':
            self._error_message('you have to set the initial condition from the relevant option menu.')
            return None
        try:
            max_t = float(self.Entry_label_dict["Final time:"].get())
            nt = int(self.Entry_label_dict["Number cycles:"].get())
            assert (self.max_t_min < max_t and self.nt_min <= nt <= self.nt_max and nt / max_t < self.max_ratio)
        except ValueError:
            self._error_message('Bad input in data, Number cycles must be integer and Final time must be float'
                                ' (or integer).')
            return None
        except AssertionError:
            self._error_message(f'The values of Final time and Number cycles must satisfy the conditions: '
                                f'{self.max_t_min} < Final time, {self.nt_min} <= Number cycles <= {self.nt_max} '
                                f'and Number cycles/Final time < {self.max_ratio}')
            return None
        try:
            if self.Chosen_potential_type == '':
                self._error_message('you have to set the potential type from the relevant option menu.')
                return None
            init_wave_form = self.Chosen_initial_condition_form
            potential_type = self.Chosen_potential_type
            max_x = float(self.Entry_label_dict["x_max:"].get())
            nx = int(self.Entry_label_dict["Number of Cells (nx):"].get())
            # Assertion conditions that necessary to get a reasonable solution.
            assert (self.max_x_min < max_x < nx / 2)
            assert (self.nx_min < nx < self.nx_max)
        except ValueError:
            self._error_message('Bad input in data, nx must be integer and x_max must be float (or integer).')
            return None
        except AssertionError:
            self._error_message(f'The values of x_max and nx must to be between [{self.max_x_min}, {nx}/2], '
                                f'[{self.nx_min}, {self.nx_max}], respectively.')
            return None
        try:
            if init_wave_form == 'Gaussian':
                amplitude = float(self.Amplitude_Gaussian)
                wave_vector_sigma = float(self.Sigma)
                phase_mu = float(self.Mu)
                # Assertion conditions that necessary to get a reasonable solution.
                assert (abs(phase_mu) <= self.phase_mu_max)
                assert (abs(wave_vector_sigma) <= self.wave_vector_sigma_max_gauss_sh)
                assert (self.amplitude_min < amplitude <= self.amplitude_max)
            if init_wave_form == 'Sinc wave' or init_wave_form == 'Sine wave':
                amplitude = float(self.Amplitude_Sin_Sinc)
                wave_vector_sigma = float(self.Wave_vector)
                phase_mu = float(self.Phase)
                # Assertion conditions that necessary to get a reasonable solution.
                assert (abs(wave_vector_sigma) <= self.wave_vector_sigma_max_sin_sinc_sh)
                assert (abs(phase_mu) < max_x)
                assert (self.amplitude_min < amplitude <= self.amplitude_max)
            if self.Chosen_potential_type == 'harmonic potential':
                potential_type = 'harmonic potential'
            if self.Chosen_potential_type == 'Gaussian potential':
                potential_type = 'Gaussian potential'
        except ValueError:
            self._error_message("Bad input in equation data. Please insert floats or integers.")
            return None
        except AssertionError:
            if init_wave_form == 'Gaussian':
                self._error_message(f'The values of Amplitude,sigma and Mu must to be between [{self.amplitude_min}'
                                    f',{self.amplitude_max}), (-{self.wave_vector_sigma_max_gauss_sh},'
                                    f' {self.wave_vector_sigma_max_gauss_sh}), (-{self.phase_mu_max},'
                                    f' {self.phase_mu_max}) respectively')
            if init_wave_form == 'Sinc wave' or init_wave_form == 'Sine wave':
                self._error_message(f'The values of Amplitude, Phase and Wave vector must to be between '
                                    f'[{self.amplitude_min}, {self.amplitude_max}), [-x_max,x_max],'
                                    f' (-{self.wave_vector_sigma_max_sin_sinc_sh},'
                                    f' {self.wave_vector_sigma_max_sin_sinc_sh}) respectively')
                return None
        self.eq = schrodinger_1d.schrodinger1D(max_x, nx, max_t, nt, init_wave_form, amplitude, wave_vector_sigma,
                                               phase_mu, potential_type)