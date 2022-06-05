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
        


    def run_simulation(self):
        print(self.env)
        for i in range(100):
            print(i)
        

if __name__ == "__main__":
    env = Environment(50, 50)
    my_cell = env.get_cell(0, 0)
    sim = Simulation(env)
    sim.run()
    # try to be able to set some cells in environment via GUI

