

import numpy as np
import scipy


class Diffusion2D(Equation):
    def __init__(max_x, max_y, nx, ny, dt, alpha, up, down, left, right):
        self.x = np.linspace(0, max_x, nx + 1)  # mesh points in space
        self.y = np.linspace(0, max_y, ny + 1)  # mesh points in space
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]
        self.nx = nx
        self.ny = ny
        self.dt = dt
        self.gamma = (alpha * self.dt) / (self.dx * self.dy)
	# initialize the array
        self.u_prev = np.empty((max_x, max_y))
        self.u_current = np.empty((max_x, max_y))
        self.u_prev = 0
        self.u_current = 0
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def return_results(self):

        pass

    def set_boundary_condition(self):
      	self.u_current[self.nx-1:, :] = self.up
      	self.u_current[:1, 1:] = self.down
      	self.u_current[:, :1] = self.left
      	self.u_current[:, self.ny-1:] = self.right

      	self.u_prev[self.nx-1:, :] = self.up
      	self.u_prev[:1, 1:] = self.down
      	self.u_prev[:, :1] = self.left
      	self.u_prev[:, self.ny-1:] = self.right
        pass


    def finish_execution(self):
        pass


# Solves the diffusion 2d heat for a box! - for a cylinder it won't owrk... given a boundary condition of values..
    def solve_time_step(self):
        for i in range(1, self.nx - 1, self.dx): #self.x[-1] is our boundary condition
            for j in range(1, self.ny - 1, self.dy):
                self.u_current[i, j] = self.gamma * (self.u_prev[i+1][j] + self.u_prev[i-1][j] + self.u_prev[i][j+1] + self.u_prev[i][j-1] - 4*self.u_prev[i][j]) + self.u_prev[i][j]
  
        
    def update(self):
        self.u_prev = self.u_current
