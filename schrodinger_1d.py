from equation import Equation
import numpy as np
import scipy.integrate as integrate

class schrodinger1D(Equation):
    """
    This class solves the one-dimensional Schrodinger equation by the Crank Nicolson method. This is the only method
    that satisfy Unitary propagator with necessary to keep the normalization of the wave function for all time.
    """
    def __init__(self, max_x, nx, max_t, nt, init_wave_form,amplitude, wave_vector_sigma, phase_mu, potential_type):
        # Variables.
        self.v0 = amplitude
        self.k0 = 1
        self.x = np.linspace(-max_x, max_x, nx + 1)
        self.dx = self.x[1] - self.x[0]
        self.nx = nx
        self.t = np.linspace(0, max_t, nt + 1)
        self.dt = self.t[1] - self.t[0]
        self.nt = nt

        # The user can choose the general form of the initial wave function, the options are Sine wave, Gaussian
        # and Sinc wave.
        if init_wave_form == 'Sine wave':
            self.f0 = lambda x: np.sin(wave_vector_sigma * np.pi * x / max_x + phase_mu)
            self.f0_squared = lambda x: (np.sin(wave_vector_sigma * np.pi * x / max_x + phase_mu)) ** 2
        if init_wave_form == 'Sinc wave':
            self.f0 = lambda x: np.sin(wave_vector_sigma * np.pi * x / max_x + phase_mu)/ \
                                (wave_vector_sigma * np.pi * x / max_x + phase_mu)
            self.f0_squared = lambda x:(np.sin(wave_vector_sigma * np.pi * x / max_x + phase_mu)/ \
                                        (wave_vector_sigma * np.pi * x / max_x + phase_mu)) ** 2
        if init_wave_form == 'Gaussian':
            self.f0 = lambda x: np.exp(-1/(2*wave_vector_sigma**2)*(x-phase_mu)**2) * np.exp(1j * self.k0 * x)
            self.f0_squared = lambda x: (np.exp(-1/(2*wave_vector_sigma**2)*(x-phase_mu)**2)) ** 2

        # The user can choose the potential type, the options are harmonic potential or Gaussian potential.
        if potential_type == 'harmonic potential':
            self.V = lambda x: self.v0 * x**2
        if potential_type == 'Gaussian potential':
            self.V = lambda x: self.v0 * np.exp(-(1/2)*x ** 2)

        # Calculation of the Amplitude by the normalization condition and other technical matrix definitions that halp
        # solve the equation.
        self.I = integrate.quad(self.f0_squared, -max_x, max_x)[0]
        self.A = (1 / self.I) ** (1/2)
        self.psi_0 = self.A * self.f0(self.x)
        self.F = (1j*self.dt)/((self.dx)**2)
        self.u_current = np.zeros(self.nx + 1, dtype=np.complex_)
        self.u_prev = np.copy(self.psi_0)
        self.cycle = 0
        self.time_steps = nt
        self.solutions = np.zeros([nt + 1, self.nx + 1])
        self.step = 1
        self.J = len(self.x)
        self.T = len(self.t)
        self.diagonal = 2 + (self.dx ** 2) * self.V(self.x)
        self.S = -np.diag(self.diagonal) + np.diag(np.ones(self.J - 1), 1) + np.diag(np.ones(self.J - 1), -1)
        self.CN = np.linalg.inv(np.eye(self.J) - self.F / 2 * self.S) @ (np.eye(self.J) + self.F / 2 * self.S)

    def finish_execution(self):
        if self.cycle >= self.nt:
            return True
        else:
            return False

    def solve_time_step(self):
        self.u_current[0:] = self.CN @ self.u_prev[0:]

    def update(self):
        self.cycle = self.cycle + 1
        self.solutions[self.cycle, :] = (abs(self.u_current))**2
        self.u_prev = self.u_current

    # Set the axis names.

    def start_plot(self, fig):
        super().start_plot(fig, xlabel='x', ylabel='$|\psi(x)|^2$', title='Probability amplitude vs position')
