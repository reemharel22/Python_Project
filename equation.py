import numpy as np
import scipy.sparse
import scipy.linalg
import scipy
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

# style.use('ggplot')

class Equation:
    def __init__(self):
        # self.step = 0 should be defined by inheritence claseses
        # self.solutions should be defined by inheritence classes
        pass

    def return_results(self):
        pass

    def set_boundary_condition(self):
        pass

    def solve(self):
        while not self.finish_execution():
            self.set_boundary_condition()
            self.solve_time_step()
            self.update()

    def update(self):
        pass

    def finish_execution(self):
        pass

    def solve_time_step(self):
        pass

    # it is common for all 1d equations to do this..
    def plot_animation(self, fig):
        self.fig = fig
        self.ax = self.fig.add_subplot(111)
        line, = self.ax.plot(self.x, self.solutions[1, :])

        def animate(i):
            if i >= len(self.solutions):
                return line,
            line.set_ydata(self.solutions[i, :])
            return line,

        self.ani = animation.FuncAnimation(self.fig, animate, interval=25, blit=False, frames=200, save_count=50)
        return self.ani

    def start_plot(self, fig, xlabel, ylabel):
        self.step = 1
        self.ax = fig.subplots()
        self.line, = self.ax.plot(self.x, self.solutions[1, :])
        plt.xlim([0, self.x[-1]])
        plt.ylim([0, np.max(self.solutions[:, :])])
        plt.xlabel('Position')
        plt.ylabel('Flux')

    def plot_step(self, i):
        self.step = self.step + i
        if self.step > len(self.solutions):
            self.step = 1
            return False
        if self.step < 1:
            self.step = 1
            return False
        self.line.set_ydata(self.solutions[self.step, :])






class Wave1D(Equation):
    def __init__(self, max_x, nx, max_t, nt, velocity, init_wave_form, amplitude, wave_vector_sigma, phase_mu):
        self.t = np.linspace(0, max_t, nt + 1)
        self.dt = self.t[1] - self.t[0]
        self.nt = nt
        self.x = np.linspace(0, max_x, nx + 1)
        self.dx = self.x[1] - self.x[0]
        self.nx = nx
        if init_wave_form == 'Sine wave':
            self.f0 = amplitude * np.sin(wave_vector_sigma * np.pi * self.x / max_x + phase_mu)
        if init_wave_form == 'Sinc wave':
            self.f0 = amplitude * np.sin(wave_vector_sigma * np.pi * self.x / max_x + phase_mu)/\
                      wave_vector_sigma * np.pi * self.x / max_x + phase_mu
        if init_wave_form == 'Gaussian':
            self.f0 = amplitude * np.exp(-1/(2*wave_vector_sigma**2)*(self.x-phase_mu)**2)
        self.F = velocity * self.dt / self.dx
        self.velocity = velocity
        self.u_current = np.zeros(self.nx + 1)
        self.u_prev = np.zeros(self.nx + 1)
        self.cycle = 0
        self.time_steps = nt
        self.solutions = np.zeros([nt + 1, self.nx + 1])
        self.u_prev[:] = np.copy(self.f0)
        self.step = 1
        self.u_prev[0] = np.copy(self.f0[0])  # init val
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

    # def plot_animation(self, fig):
    #     pause = False
    #     self.fig = fig
    #     # self.x = 20 * np.arange(0, 2 * np.pi, 0.01)  # x-array
    #     # self.fig = plt.Figure()
    #
    #     # self.eq.plot_animation(self.fig)
    #     self.ax = self.fig.add_subplot(111)
    #     line, = self.ax.plot(self.x, self.solutions[1, :])
    #
    #     #
    #     def animate(i):
    #         if i >= len(self.solutions):
    #             return line,
    #         line.set_ydata(self.solutions[i, :])
    #         return line,
    #
    #     self.ani = animation.FuncAnimation(self.fig, animate, interval=25, blit=False, frames=200, save_count=50)

    def start_plot(self, fig):
        # self.step = 1
        # pause = False
        # ax = fig.subplots()
        # self.line, = ax.plot(self.x, self.solutions[1, :])
        # plt.xlim([0, self.x[-1]])
        # plt.ylim([0, np.max(self.solutions[:, :])])
        super().start_plot(fig, xlabel='Position', ylabel='Velocity (check me)')


    # def plot_step(self, i):
    #     self.step = self.step + i
    #     if self.step > len(self.solutions):
    #         self.step = 1
    #         return False
    #     if self.step < 1:
    #         self.step = 1
    #         return False
    #     self.line.set_ydata(self.solutions[self.step, :])


class schrodinger1D(Equation):
    def __init__(self, max_x, nx, max_t, nt, init_wave_form, wave_vector_sigma, phase_mu, potential_type):
        self.v0 = 10
        self.k0 = 1
        self.x = np.linspace(-max_x, max_x, nx + 1)
        self.dx = self.x[1] - self.x[0]
        self.nx = nx
        self.t = np.linspace(0, max_t, nt + 1)
        self.dt = self.t[1] - self.t[0]
        self.nt = nt
        if init_wave_form == 'Sine wave':
            self.f0 = lambda x: np.sin(wave_vector_sigma * np.pi * x / max_x + phase_mu)
            self.f0_squared = lambda x: (np.sin(wave_vector_sigma * np.pi * x / max_x + phase_mu)) ** 2
        if init_wave_form == 'Sinc wave':
            self.f0 = lambda x: np.sin(wave_vector_sigma * np.pi * x / max_x + phase_mu)/\
                      wave_vector_sigma * np.pi * x / max_x + phase_mu
            self.f0_squared = lambda x:(np.sin(wave_vector_sigma * np.pi * x / max_x + phase_mu)/\
                      wave_vector_sigma * np.pi * x / max_x + phase_mu) ** 2
        if init_wave_form == 'Gaussian':
            self.f0 = lambda x: np.exp(-1/(2*wave_vector_sigma**2)*(x-phase_mu)**2) * np.exp(1j * self.k0 * x)
            self.f0_squared = lambda x: (np.exp(-1/(2*wave_vector_sigma**2)*(x-phase_mu)**2)) ** 2
        if potential_type == 'harmonic potential':
            self.V = lambda x: self.v0 * x**2
        if potential_type == 'Gaussian potential':
            self.V = lambda x: self.v0 * np.exp(-(1/2)*x ** 2)
        self.I = integrate.quad(self.f0_squared, -max_x, max_x)[0]
        self.A = (1 / self.I) ** (1/2)
        self.psi_0 = self.A * self.f0(self.x)
        self.F = (1j*self.dt)/((self.dx)**2)
        self.u_current = np.zeros(self.nx + 1, dtype=np.complex_)
        self.u_prev = np.copy(self.psi_0)
        self.cycle = 0
        self.time_steps = nt
        self.solutions = np.zeros([nt + 1, self.nx + 1], dtype=np.complex_)
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

        #self.u_prev[0:] = self.u_current

    def update(self):
        self.cycle = self.cycle + 1
        self.solutions[self.cycle, :] = (abs(self.u_current))**2
        self.u_prev = self.u_current

    # def plot_animation(self, fig):
    #     pause = False
    #     self.fig = fig
    #     # self.x = 20 * np.arange(0, 2 * np.pi, 0.01)  # x-array
    #     # self.fig = plt.Figure()
    #
    #     # self.eq.plot_animation(self.fig)
    #     self.ax = self.fig.add_subplot(111)
    #     line, = self.ax.plot(self.x, self.solutions[1, :])
    #
    #     #
    #     def animate(i):
    #         if i >= len(self.solutions):
    #             return line,
    #         line.set_ydata(self.solutions[i, :])
    #         return line,
    #
    #     self.ani = animation.FuncAnimation(self.fig, animate, interval=25, blit=False, frames=200, save_count=50)

    def start_plot(self, fig):
        super().start_plot(fig, xlabel='Position', ylabel='Distribution (check me)')


    # def plot_step(self, i):
    #     self.step = self.step + i
    #     if self.step > len(self.solutions):
    #         self.step = 1
    #         return False
    #     if self.step < 1:
    #         self.step = 1
    #         return False
    #     self.line.set_ydata(self.solutions[self.step, :])



