from gui import Gui
import numpy as np
from equation import Equation
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class controller:
    def __init__(self):
        self.gui = Gui(self)
        self.Equation = Equation()

    def main(self):
        self.gui.main()

if __name__ == '__main__':
    Equation = controller()
    Equation.main()