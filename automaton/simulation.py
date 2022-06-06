from environment import Environment
from visual import GUI


class Simulation:
    def __init__(self, env=None):
        self.env = env or Environment(55, 42)
        self.gui = GUI(self.env)
        self.generation = 0

    def run(self, generations, steps):
        self.gui.main(generations, steps)

    def run_simulation(self):
        print(self.env)
        for i in range(1000):
            print(i)


if __name__ == "__main__":
    # try to be able to set some cells in environment via GUI
    env = Environment(55, 42)
    sim = Simulation(env)
    sim.run(100, 100)
