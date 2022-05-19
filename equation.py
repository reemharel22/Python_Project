import numpy as np
import scipy.sparse
import scipy.linalg
import scipy
import matplotlib.pyplot as plt
import matplotlib.animation as animation



class Equation:
    def __init__(self):
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

    def start_plot(self, fig):
        pass

    def plot_step(self, step):
        pass

class Diffusion1D(Equation):
    def __init__(self, max_x, nx, max_t, nt, alpha, b_val, init_val):
        # Representation of sparse matrix and right-hand side
        self.x = np.linspace(0, max_x, nx + 1)  # mesh points in grid
        self.nx = nx
        self.dx = self.x[1] - self.x[0]
        self.t = np.linspace(0, max_t, nt + 1)  # mesh points in grid
        self.nt = nt
        self.dt = self.t[1] - self.t[0]
        self.F = alpha * self.dt / self.dx ** 2
        self.alpha = alpha
        self.u_current = np.zeros(self.nx + 1)  # unknown u at new time level
        self.u_prev = np.zeros(self.nx + 1)
        self.main = np.zeros(self.nx + 1)
        self.lower = np.zeros(self.nx - 1)
        self.upper = np.zeros(self.nx - 1)
        self.b = np.zeros(self.nx + 1)
        self.main[:] = 1 + 2 * self.F
        self.main[0] = 1
        self.main[self.nx] = 1
        self.lower[:] = -self.F  # 1
        self.upper[:] = -self.F  # 1
        self.A = np.zeros((self.nx + 1, self.nx + 1))

        for i in range(1, self.nx):
            self.A[i, i - 1] = -self.F
            self.A[i, i + 1] = -self.F
            self.A[i, i] = 1 + 2 * self.F
        self.A[0, 0] = self.A[self.nx, self.nx] = 1
        # self.A = scipy.sparse.diags(
        #     diagonals=[self.main, self.lower, self.upper],
        #     offsets=[0, -1, 1], shape=(self.nx + 1, self.nx + 1),
        #     format='csr')
        # self.A.todense()  # Check that A is correct
        self.boundary_val = b_val
        self.cycle = 0
        self.time_steps = nt
        self.solutions = np.zeros([nt+1, self.nx + 1])
        self.u_prev[:] = init_val
        self.step = 1
        self.u_prev[0] = b_val# init val
        self.u_current[:] = self.u_prev[:]

    def finish_execution(self):
        if self.cycle >= self.nt:
            return True
        else:
            return False

    def set_boundary_condition(self):
        self.main[0] = 1
        self.main[self.nx] = 1
        # self.u_prev[0] = b_val
        for i in range(1, self.nx):
            self.b[i] = -self.u_prev[i]
        self.b[0] = self.b[self.nx] = 0

    def solve_time_step(self):
        for i in range(1, self.nx):
            self.u_current[i] = self.u_prev[i] + self.F * (self.u_prev[i - 1] - 2 * self.u_prev[i] + self.u_prev[i + 1])

    def update(self):
        self.cycle = self.cycle + 1
        self.solutions[self.cycle, :] = self.u_current
        self.u_prev = self.u_current

    def plot_animation(self, fig):
        pause = False
        ax = fig.add_subplot(111)
        line, = ax.plot(self.x, self.solutions[0, :])
        plt.xlim([0, self.x[-1]])
        plt.ylim([0, np.max(self.solutions)])

        def animate(i):
            if i > len(self.solutions):
                return line,
            line.set_ydata(self.solutions[i, :])
            return line,

        ani = animation.FuncAnimation(
            fig, animate, blit=True, frames=200, save_count=50)

        # fig.show()

    def start_plot(self, fig):
        self.step = 1
        pause = False
        ax = fig.subplots()
        self.line, = ax.plot(self.x, self.solutions[1, :])
        plt.xlim([0, self.x[-1]])
        plt.ylim([0, np.max(self.solutions[:, :])])

    def plot_step(self, i):
        self.step = self.step + i
        if self.step > len(self.solutions):
            self.step = 1
            return False
        if self.step < 1:
            self.step = 1
            return False
        self.line.set_ydata(self.solutions[self.step, :])



