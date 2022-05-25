# class Automaton:
#     """
#     class for abstract machines maybe
#     """

class Cell:
    def __init__(self, x, y, genome: list = None):
        self.x = x
        self.y = y
        self.genome = genome
        # genome = [weight, reaction, ...]

    def __str__(self):
        return f"cell on ({self.x},{self.y}) with genome = {self.genome}"

    def go(self, direction: str):
        """
        provides moving cell in one of four main directions
        :param direction:
        :return:
        """
        if direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1
        elif direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1


