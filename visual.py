import random

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
                        

class Button():
    def __init__(self, x, y, path):
        img = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, surface):
        """Draws a button on screen."""
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clecked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False: # 0 - left click
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw a button
        surface.blit(self.image, (self.rect.x, self.rect.y))
  
        return action

class GUI:
    DISPLAY_X = 1000
    DISPLAY_Y = 700

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GUI.DISPLAY_X, GUI.DISPLAY_Y))  # create a screen
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('images/evolution.png'))  # program image

        #load button images
        pygame.draw.rect(self.screen, (30, 50, 50), pygame.Rect(900, 0, 100, 700))
        self.light_button = Button(930, 100, "images/idea.png")
        self.cell_button = Button(930, 200, "images/cell.png")
        self.wall_button = Button(930, 300, "images/wall.png")
        self.plant_button = Button(930, 400, "images/plant.png")
        self.play_button = Button(930, 500, "images/play-button.png")

        self.cells = []
        self.plants = []
        self.walls = []

    def spawn_cell(self):
        cell1 = Cell(200, 200, self.screen, (70, 10, 70))
        cell1.draw()

    def main(self):

        run = True
        while run:
            self.screen.fill((70, 80, 80))
            pygame.draw.rect(self.screen, (30, 50, 50), pygame.Rect(900, 0, 100, 700))

    
            if self.light_button.draw(self.screen):
                print("Turn the light on")
            if self.cell_button.draw(self.screen):
                # print("Spawn a cell")
                self.cells.append(Cell(random.randint(0, GUI.DISPLAY_X-100), random.randint(0, GUI.DISPLAY_Y), self.screen, (70, 10, 70)))
            if self.plant_button.draw(self.screen):
                # print("Place some food")
                self.plants.append(Plant(random.randint(0, GUI.DISPLAY_X-100), random.randint(0, GUI.DISPLAY_Y), self.screen))
            if self.play_button.draw(self.screen):
                print("Evolution starts")
            if self.wall_button.draw(self.screen):
                # print("Build a wall")
                self.walls.append(Wall(random.randint(0, GUI.DISPLAY_X-100), random.randint(0, GUI.DISPLAY_Y), self.screen))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    run = False
                    pygame.quit()

            for obj in [*self.cells, *self.plants, *self.walls]:
                obj.draw()
            pygame.display.update()


display = GUI()
display.main()
