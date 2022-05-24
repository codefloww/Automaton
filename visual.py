import random
import pygame

#color palette
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

    def __init__(self, x, y, screen):
        colors = [YELLOW, RED, PURPLE]
        super().__init__(x, y, screen)
        self.color = random.choice(colors)

    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           (self.coordinate_x, self.coordinate_y), Cell.radius)


class Plant(Object):
    # color = (80, 150, 80)
    color = GREEN
    radius = 20

    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)

    def draw(self):
        pygame.draw.circle(self.screen, Plant.color,
                         (self.coordinate_x, self.coordinate_y), Plant.radius)


class Wall(Object):
    # color = (40, 40, 40)
    color = (52, 74, 83)
    size = (30, 30)

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
        # pygame.init()
        self.screen = pygame.display.set_mode((GUI.DISPLAY_X, GUI.DISPLAY_Y))  # create a screen
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('images/evolution.png'))  # program image
        #load button images
        self.light_button = Button(940, 80, "images/idea.png")
        self.cell_button = Button(940, 180, "images/virus.png")
        self.wall_button = Button(940, 280, "images/wall.png")
        self.plant_button = Button(940, 380, "images/plant.png")
        self.play_button = Button(940, 480, "images/play-button.png")
        self.quit_button = Button(940, 580, "images/remove.png")

        self.cells = []
        self.plants = []
        self.walls = []

    def main(self):
        run = True
        while run:
            self.screen.fill(SKY_BLUE)
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(920, 0, 100, 700))
    
            if self.light_button.draw(self.screen):
                print("Turn the light on")
            if self.cell_button.draw(self.screen):
                # print("Spawn a cell")
                self.cells.append(Cell(random.randint(0, GUI.DISPLAY_X-100), random.randint(0, GUI.DISPLAY_Y), self.screen))
            if self.plant_button.draw(self.screen):
                # print("Place some food")
                self.plants.append(Plant(random.randint(0, GUI.DISPLAY_X-100), random.randint(0, GUI.DISPLAY_Y), self.screen))
            if self.play_button.draw(self.screen):
                print("Evolution starts")
            if self.wall_button.draw(self.screen):
                # print("Build a wall")
                self.walls.append(Wall(random.randint(0, GUI.DISPLAY_X-100), random.randint(0, GUI.DISPLAY_Y), self.screen))
            if self.quit_button.draw(self.screen):
                run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    run = False
                    # pygame.quit()

            for obj in [*self.cells, *self.plants, *self.walls]:
                obj.draw()
            pygame.display.update()


display = GUI()
display.main()
