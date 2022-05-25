from environment import Environment
from cell import Cell
from visual import GUI

class Simulation:
    def __init__(self, env = None):
        self.env = env or Environment(10, 10)
        self.gui = GUI()
        self.generation = 0

    def run(self):
        self.gui.main()
        # self.env.set_cell(i, 5, Cell(i, 5, 'organism')) for setting the cell
        # here we need something to refresh the GUI
        # like self.gui.refresh(self.env) or self.gui.update(self.env)
        print(self.env.get_environment_state())
        self.run_simulation()

    def run_simulation(self):
        while True:
            self.run()
            self.generation += 1
            print(f"Generation: {self.generation}")
        

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    # try to be able to set some cells in environment via GUI

