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
git-clone https://github.com/codefloww/Automata.git
```
and after that go to clonned directory and run:
```bash
python3 -m pip3 install .
```
for installing package via pip.

## Run
To run a simulation you can simply go to the [simulation.py](automaton/simulation.py) or import package to your file and simply running something like
```python
from simulation import Simulation
sim = Simulation()
sim.run()
```
You will see a window that looks like this  
![image](https://user-images.githubusercontent.com/90351072/172068831-82bdd030-a719-48ad-a551-c3db273bf288.png)  
Here you can click on light bulb to turn on light in the environment:  
![image](https://user-images.githubusercontent.com/90351072/172068706-4564ae58-13dd-44d4-ae37-43eeb87eeabf.png)  
You can also choose different instances to place in environment, erase them, go back via Ctrl-Z.  
<img width="640" alt="image" src="https://user-images.githubusercontent.com/90351072/172069046-ae76a72a-3278-4aba-a960-abd9d2fd323c.png">  
After that you press Play button to run simulation:  
![](https://github.com/codefloww/Automaton/images/example.gif)
Every simulation may be different from each other because of the mutations and crossover.)

### License
[MIT](LICENSE)

