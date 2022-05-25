import pygame, sys
import random
from cell import Cell as CCell
from environment import Environment
SKY_BLUE = (135, 206, 235)
YELLOW = (245, 236, 142)
GREEN = (110, 212, 123)
PURPLE = (150, 110, 212)
RED = (247, 129, 134)


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
    color = (74, 120, 0)
    radius = 15

    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)

    def draw(self):
        pygame.draw.circle(self.screen, Plant.color,
                           (self.coordinate_x, self.coordinate_y), Plant.radius)


class Wall(Object):
    color = (20, 20, 20)
    size = (40, 40)

    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)

    def draw(self):
        pygame.draw.rect(self.screen, Wall.color,
                         (self.coordinate_x, self.coordinate_y, Wall.size[0], Wall.size[1]))


class Button:
    def __init__(self, x, y, path):
        img = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """Draws a button on screen."""
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clecked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:  # 0 - left click
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw a button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


class GUI:
    DISPLAY_X = 1000
    DISPLAY_Y = 700
    DISPLAY_COLOR = (70, 80, 80)
    MENU_COLOR = (30, 50, 50)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GUI.DISPLAY_X, GUI.DISPLAY_Y))  # create a screen
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('images/evolution.png'))  # program image

        # load button images
        self.light_button = Button(930, 100, "images/idea.png")
        self.cell_button = Button(930, 200, "images/cell.png")
        self.wall_button = Button(930, 300, "images/wall.png")
        self.plant_button = Button(930, 400, "images/plant.png")
        self.play_button = Button(930, 500, "images/play-button.png")

        self.cells = []
        self.plants = []
        self.walls = []
        self.environment = Environment(GUI.DISPLAY_X, GUI.DISPLAY_Y)

    def spawn_cell(self, name_class):
        spawn = True
        while spawn:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    spawn = False
                    x, y = pygame.mouse.get_pos()
                    if name_class == 'Cell':
                        self.cells.append(Cell(x, y, self.screen, (70, 10, 70)))
                        self.environment.cells_matrix[y][x] = 1
                        self.environment.cells_objects.append(CCell(x, y))
                    elif name_class == 'Plant':
                        self.plants.append(Plant(x, y, self.screen))
                    elif name_class == 'Wall':
                        self.walls.append(Wall(x, y, self.screen))

    def main(self):
        run = True
        while run:
            self.screen.fill(GUI.DISPLAY_COLOR)
            for obj in [*self.cells, *self.plants, *self.walls]:
                obj.draw()
            pygame.draw.rect(self.screen, GUI.MENU_COLOR, pygame.Rect(900, 0, 100, 700))

            if self.light_button.draw(self.screen):
                self.change_light()
            if self.cell_button.draw(self.screen):
                self.spawn_cell('Cell')
            if self.plant_button.draw(self.screen):
                self.spawn_cell('Plant')
            if self.play_button.draw(self.screen):
                print("Evolution starts")
                self.start()
            if self.wall_button.draw(self.screen):
                self.spawn_cell('Wall')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    run = False
                    pygame.quit()
            pygame.display.update()


    def change_light(self):
        if GUI.DISPLAY_COLOR == (70, 80, 80):
            GUI.DISPLAY_COLOR = SKY_BLUE
        else:
            GUI.DISPLAY_COLOR = (70, 80, 80)

        if GUI.MENU_COLOR == (30, 50, 50):
            GUI.MENU_COLOR = (255, 255, 255)
        else:
            GUI.MENU_COLOR = (30, 50, 50)

    def screen_draw(self):
        self.screen.fill(SKY_BLUE)
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(920, 0, 100, 700))
        self.light_button.draw(self.screen)
        self.cell_button.draw(self.screen)
        self.wall_button.draw(self.screen)
        self.plant_button.draw(self.screen)
        self.play_button.draw(self.screen)
        for obj in [*self.cells, *self.plants, *self.walls]:
            obj.draw()
        pygame.display.update()

    def start(self):
        CLOCK = pygame.time.Clock()
        while True:
            CLOCK.tick(5)
            self.environment.evolve()
            self.cells = [Cell(ccell.x, ccell.y, self.screen, (70, 10, 70)) for ccell in self.environment.cells_objects]
            self.screen_draw()


display = GUI()
display.main()
