from gui import Gui
from equation import Equation

class controller:
    def __init__(self):
        self.gui = Gui(self)
        self.Equation = Equation()

    def main(self):
        self.gui.main()

if __name__ == '__main__':
    Equation = controller()
    Equation.main()