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
        # self.step = 0 should be defined by inheritance classes
        # self.solutions should be defined by inheritance classes
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

    def start_plot(self, fig, xlabel ='Position' , ylabel = 'flux'):
        self.step = 1
        self.ax = fig.subplots()
        self.line, = self.ax.plot(self.x, self.solutions[1, :])
        #self.ax.set_xlim([0, self.x[-1]])
        #self.ax.set_ylim([0, np.max(self.solutions[:, :])])
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        plt.xlim([0, self.x[-1]])
        plt.ylim([0, np.max(self.solutions[:, :])])
        #plt.xlabel('Position')
        #plt.ylabel('Flux')

    def plot_step(self, i):
        self.step = self.step + i
        if self.step > len(self.solutions):
            self.step = 1
            return False
        if self.step < 1:
            self.step = 1
            return False
        self.line.set_ydata(self.solutions[self.step, :])



