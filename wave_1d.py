from equation import Equation
import numpy as np

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

