
from cell import Authomaton
from numpy import random


class Territory():
    def __init__(self, x, y) -> None:
        self.type = random.choice(["G", "G", "_"]) # --зробив два айтема "G" чисто для прикладу : поле виходить адекватнішим.
        self.cell = Authomaton(x, y)
        self.features = [] # modifiers of the territory : light, food, climate etc. 
        # --Краще нам розділити features на різні проперті : self.light, self.food, self.climate і т.д

    def __str__(self) -> str:
        return self.type


class Environment():
    def __init__(self, width, height) -> None:
        self.width = width # width of the field
        self.height = height # height of the field

    def create_field(self):
        """
        Generates an absolutely random field.
        """
        # --Доведеться зробити його кращим. Це поле - чисто для репрезентації.
        self.field = [[Territory(x, y) for y in range(self.width)] for x in range(self.height)]

    def update_env(self):
        """
        
        """
        # --Якщо по факту то слабо собі уявляю як це має працювати. Напевно, це промах моєї системи :/

    def __str__(self) -> str:
        """
        Represents the landscape. "_" and "G" symbols represent water and ground respectively.
        """
        output = ""
        for i in self.field:
            for j in i:
                output += str(j) + " "
            output += "\n"
        return output


# --Приклад створеного середовища :
env = Environment(20, 20)
env.create_field()
print(env)
