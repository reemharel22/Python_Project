import numpy as np
import scipy

class Equation:
    def __init__(self):
        pass
    def return_results(self):
        pass

    def set_boundary_condition(self):
        pass

    def Solver(self):
        while not self.finish_execution():
            self.set_boundary_condition()
            self.solve_time_step()


    def finish_execution(self):
        pass

    def solve_time_step(self):
        pass

class Diffusion1D(Equation):
    def __init__(self, max_x, nx, dt, alpha):
        # Representation of sparse matrix and right-hand side
        self.x = np.linspace(0, max_x, nx + 1)  # mesh points in space
        self.dx = self.x[1] - self.x[0]
        self.dt = dt
        self.F = alpha * self.dt / self.dx ** 2
        self.u_next = np.zeros(self.nx + 1)  # unknown u at new time level
        self.u_prev = np.zeros(self.nx + 1)
        self.main = np.zeros(self.nx + 1)
        self.lower = np.zeros(self.nx - 1)
        self.upper = np.zeros(self.nx - 1)
        self.b = np.zeros(self.nx + 1)
        self.main[:] = 1 + 2 * self.F
        self.lower[:] = -self.F  # 1
        self.upper[:] = -self.F  # 1
        self.A = scipy.sparse.diags(
            diagonals=[self.main, self.lower, self.upper],
            offsets=[0, -1, 1], shape=(self.nx + 1, self.nx + 1),
            format='csr')
        self.A.todense()  # Check that A is correct

    def set_boundary_condition(self):
        self.main[0] = 1
        self.main[self.nx] = 1

    def solve_time_step(self):
        print("TODO")
        # b = self.u_prev
        # b[0] = b[-1] = 0.0  # boundary conditions
        # u[:] = scipy.sparse.linalg.spsolve(A, b)
        # u_1[:] = u

