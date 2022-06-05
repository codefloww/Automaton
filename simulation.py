from visual import GUI
from environment import Environment


class Simulation:
    def __init__(self, env=None):
        # 55, 42
        self.env = env or Environment(55, 42)
        self.gui = GUI(self.env)
        self.generations = 1000
        self.steps = 300

    def run(self):
        # # the first stage of gui in which we interact with the interface and setup env
        # self.gui.setup()
        # # the second stage of gui in which we run evolution(should start after pressing play in previous function)
        # self.run_simulation()

        self.gui.main(self.generations, self.steps)

    # def run_simulation(self):
    #     # we have 1000 generations
    #     for gen in range(1000):
    #         for step in range(300):
    #             self.run_step()
    #             self.gui.run() # updates gui


if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    # try to be able to set some cells in environment via GUI
