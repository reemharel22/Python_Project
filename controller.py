from gui import gui


class controller:
    def __init__(self):
        self.gui = gui(self)

    def main(self):
        self.gui.main()


if __name__ == '__main__':
    Equation = controller()
    Equation.main()
