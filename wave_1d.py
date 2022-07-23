from equation import Equation
import numpy as np

class Wave1D(Equation):
    """
    This class solves the one-dimensional and one directional wave equation by the Euler method.
    """
    def __init__(self, max_x, nx, max_t, nt, velocity, init_wave_form, amplitude, wave_vector_sigma, phase_mu):
        # Variables.
        self.t = np.linspace(0, max_t, nt + 1)
        self.dt = self.t[1] - self.t[0]
        self.nt = nt
        self.x = np.linspace(0, max_x, nx + 1)
        self.dx = self.x[1] - self.x[0]
        self.nx = nx

        # The user can choose the general form of the initial wave function, the options are Sine wave, Gaussian
        # and Sinc wave.
        if init_wave_form == 'Sine wave':
            self.f0 = amplitude * np.sin(wave_vector_sigma * np.pi * self.x / max_x + phase_mu)
        if init_wave_form == 'Sinc wave':
            self.f0 = amplitude * np.sin(wave_vector_sigma * np.pi * self.x / max_x + phase_mu)/\
                      wave_vector_sigma * np.pi * self.x / max_x + phase_mu
        if init_wave_form == 'Gaussian':
            self.f0 = amplitude * np.exp(-1/(2*wave_vector_sigma**2)*(self.x-phase_mu)**2)

        # Calculation of the Amplitude by the normalization condition and other technical matrix definitions that halp
        # solve the equation.
        self.F = velocity * self.dt / self.dx
        self.velocity = velocity
        self.u_current = np.zeros(self.nx + 1)
        self.u_prev = np.zeros(self.nx + 1)
        self.cycle = 0
        self.time_steps = nt
        self.solutions = np.zeros([nt + 1, self.nx + 1])
        self.u_prev[:] = np.copy(self.f0)
        self.step = 1
        self.u_prev[0] = np.copy(self.f0[0])
        self.u_current[:] = self.u_prev[:]

    def finish_execution(self):
        if self.cycle >= self.nt:
            return True
        else:
            return False

    def solve_time_step(self):
        for i in range(1, self.nx):
            self.u_current[i] = self.u_prev[i] - self.F * (self.u_prev[i - 1] + self.u_prev[i])

    def update(self):
        self.cycle = self.cycle + 1
        self.solutions[self.cycle, :] = self.u_current
        self.u_prev = self.u_current

    # Set the axis names.

    def start_plot(self, fig):
        super().start_plot(fig, xlabel='x', ylabel= '$\psi(x)$', title='Wave function vs position')


