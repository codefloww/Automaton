from visual import GUI


class Simulation:
    def __init__(self):
        self.gui = GUI()
        self.generation = 0

    def run(self):
        self.gui.main()
        # self.env.set_cell(i, 5, Cell(i, 5, 'organism')) for setting the cell
        # here we need something to refresh the GUI
        # like self.gui.refresh(self.env) or self.gui.update(self.env)

    def run_simulation(self):
        print(self.gui.environment)
        for i in range(100):
            print(i)
        

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    # try to be able to set some cells in environment via GUI

