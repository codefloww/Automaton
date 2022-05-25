import random
import pygame

#color palette
SKY_BLUE = (135, 206, 235)
YELLOW = (245, 236, 142)
GREEN = (110, 212, 123)
PURPLE = (150, 110, 212)
RED = (247, 129, 134)


FPS = 60
clock = pygame.time.Clock()

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
    size = (40, 40)

    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)

    def draw(self):
        pygame.draw.rect(self.screen, Wall.color,
                         (self.coordinate_x, self.coordinate_y, Wall.size[0], Wall.size[1]))
           
class Button():
    def __init__(self, x, y, path, path_on=None, created=None):
        img_off = pygame.image.load(path).convert_alpha()
        self.image_off = pygame.transform.scale(img_off, (40, 40))

        path_on = path_on or path
        img_on = pygame.image.load(path_on).convert_alpha()
        self.image_on = pygame.transform.scale(img_on, (40, 40))

        self.image = self.image_off
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

        self.is_on = False
        self.created_object = created

    def turn_on(self):
        self.is_on = True
        self.image = self.image_on
    
    def turn_off(self):
        self.is_on = False
        self.image = self.image_off
    
    def draw(self, surface):
        """Draws a button on screen."""
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clecked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked: # 0 - left click
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
        self.screen = pygame.display.set_mode((GUI.DISPLAY_X, GUI.DISPLAY_Y))  # create a screen
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('images/evolution.png'))  # program image
        #load button images
        self.light_button = Button(940, 80, "images/idea.png", "images/idea_on.png")
        self.cell_button = Button(940, 180, "images/virus.png", "images/virus_on.png", "Cell")
        self.wall_button = Button(940, 280, "images/wall.png", "images/wall_on.png", "Wall")
        self.plant_button = Button(940, 380, "images/plant.png", "images/plant_on.png", "Plant")
        self.play_button = Button(940, 480, "images/play-button.png", "images/video-pause-button.png")
        self.quit_button = Button(940, 580, "images/remove.png")
        self.button = None
        self.cur_spawning_button = None

        self.cells = []
        self.plants = []
        self.walls = []

    def spawn_cell(self, name_class):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if name_class == 'Cell':
                    self.cells.append(Cell(x, y, self.screen))
                elif name_class == 'Plant':
                    self.plants.append(Plant(x, y, self.screen))
                elif name_class == 'Wall':
                    self.walls.append(Wall(x, y, self.screen))

    def button_navigate(self, button):
        self.button = button
        if self.button.is_on and self.button.draw(self.screen):
            self.button.turn_off()
            self.cur_spawning_button = None
        if self.button.draw(self.screen) and not self.button.is_on:
            if self.cur_spawning_button is None:
                self.cur_spawning_button = self.button
                self.button.turn_on()
        if self.button.is_on:
            self.spawn_cell(self.button.created_object)

    def main(self):
        run = True

        while run:
            self.screen.fill(SKY_BLUE)
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(920, 0, 100, 700))

            if self.light_button.is_on and self.light_button.draw(self.screen):
                self.light_button.turn_off()
            if self.light_button.draw(self.screen):
                self.light_button.turn_on()
                print("Turn the light on")

            # Cell button
            self.button_navigate(self.cell_button)

            #Plant button
            self.button_navigate(self.plant_button)

            #Wall button
            self.button_navigate(self.wall_button)

            #Play button
            if self.play_button.is_on and self.play_button.draw(self.screen):
                self.play_button.turn_off()
            if self.play_button.draw(self.screen):
                self.play_button.turn_on()
                print("Evolution starts")
            
            #Quit button
            if self.quit_button.draw(self.screen):
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    run = False

            for obj in [*self.cells, *self.plants, *self.walls]:
                obj.draw()

            clock.tick(FPS)
            pygame.display.update()


display = GUI()
display.main()
