import pygame, sys


class Object:
    def __init__(self, x, y, screen):
        self.coordinate_x = x
        self.coordinate_y = y
        self.screen = screen

    def move(self, x, y):
        self.coordinate_x = (self.coordinate_x + x) % GUI.DISPLAY_X
        self.coordinate_y = (self.coordinate_y + y) % GUI.DISPLAY_Y

class Cell(Object):
    radius = 10

    def __init__(self, x, y, screen, color):
        super().__init__(x, y, screen)
        self.color = color

    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           (self.coordinate_x, self.coordinate_y), Cell.radius)


class Plant(Object):
    color = (80, 150, 80)
    radius = 20

    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)

    def draw(self):
        pygame.draw.circle(self.screen, Plant.color,
                         (self.coordinate_x, self.coordinate_y), Plant.radius)


class Wall(Object):
    color = (40, 40, 40)
    size = (40, 40)

    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)

    def draw(self):
        pygame.draw.rect(self.screen, Wall.color,
                         (self.coordinate_x, self.coordinate_y, Wall.size[0], Wall.size[1]))


class GUI:
    DISPLAY_X = 1000
    DISPLAY_Y = 700

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GUI.DISPLAY_X, GUI.DISPLAY_Y))  # create a screen
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('../Automaton/images/evolution.png'))  # program image

    def main(self):
        while True:
            self.screen.fill((70, 80, 80))
            mx, my = pygame.mouse.get_pos()
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            # приклади виведення об'єктів (над кольорами треба ще попрацювати :) )
            wall1 = Wall(500, 100, self.screen)
            wall1.draw()
            plant1 = Plant(300, 300, self.screen)
            plant1.draw()
            cell1 = Cell(200, 200, self.screen, (70, 10, 70))
            cell1.draw()


            pygame.display.update()


display = GUI()
display.main()

