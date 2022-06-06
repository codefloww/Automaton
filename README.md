# Automaton
Automaton is a team project for the discrete math course and intended to showcase a simulation and finite and determined automatons.  
This project is made by Pavlo, Dima, Nastya, Yaryna, and Nastya.

## How it works?
This is a simulation of life in some water environment. There are some characteristics of environment and 3 main instances: plants, wall and organisms,  
which are our automatas. So this is a cellular automaton. The evolution is implemented via genoms of each automatons and processes like mutations, reproducing and other.  
For more information go to our [awesome Wiki pages](https://github.com/codefloww/Automaton/wiki).  

## Installation
To try our simulator you need to install package.  
You can do it by running:
```bash
git clone https://github.com/codefloww/Automata.git
```
and after that go to clonned directory and run:(It's recommended to do after entering venv)
```bash
python3 -m pip install .
```
for installing package via pip.

## Run
To run a simulation you can simply go in the Automaton directory that you clonned and run the [automaton/simulation.py](automaton/simulation.py) or import package to your file and simply running something like
```python
from automaton.simulation import Simulation
from automaton.environment import Environment
env = Environment (55, 42)
sim = Simulation(env)
sim.run(100, 100)
```
You will see a window that looks like this  
![image](https://user-images.githubusercontent.com/90351072/172121305-fa8d4de9-72ec-43ee-84e2-1b5451ddb5e5.png)
Here you can click on light bulb to turn on light in the environment:  
![image](https://user-images.githubusercontent.com/90351072/172121355-0f1ecb85-4e20-457f-a560-9f20d693cf92.png)
You can also choose different instances to place in environment, erase them, go back via Ctrl-Z.  
<img width="640" alt="image" src="https://user-images.githubusercontent.com/90351072/172069046-ae76a72a-3278-4aba-a960-abd9d2fd323c.png">  
After that you press Play button to run simulation: 
![Alt text](https://github.com/codefloww/Automaton/images/example.gif)
Every simulation may be different from each other because of the mutations and crossover.)

### License
[MIT](LICENSE)

