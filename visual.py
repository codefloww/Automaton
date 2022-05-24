import pygame, sys

class Object:
    def __init__(self, x, y, screen):
        self.coordinate_x = x
        self.coordinate_y = y
        self.screen = screen


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
    def __init__(self, x, y, image):
        self.image = image
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
        light_img = pygame.image.load("images/idea.png").convert_alpha()
        look_light  = pygame.transform.scale(light_img, (40, 40))
        self.light_button = Button(930, 100, look_light)

        cell_img = pygame.image.load("images/cell.png").convert_alpha()
        look_cell = pygame.transform.scale(cell_img, (40, 40))
        self.cell_button = Button(930, 200, look_cell)

        wall_img = pygame.image.load("images/wall.png").convert_alpha()
        look_wall = pygame.transform.scale(wall_img, (40, 40))
        self.wall_button = Button(930, 300, look_wall)

        plant_img = pygame.image.load("images/plant.png").convert_alpha()
        look_plant = pygame.transform.scale(plant_img, (40, 40))
        self.plant_button = Button(930, 400, look_plant)

        play_img = pygame.image.load("images/play-button.png")
        look_play = pygame.transform.scale(play_img, (40, 40))
        self.play_button = Button(930, 500, look_play)

    def spawn_cell(self):
        cell1 = Cell(200, 200, self.screen, (70, 10, 70))
        cell1.draw()

    def main(self):
        while True:
            self.screen.fill((70, 80, 80))
            mx, my = pygame.mouse.get_pos()
            click = False
            color = (255,255,255)
            pygame.draw.rect(self.screen, color, pygame.Rect(900, 0, 100, 700))
    
            if self.light_button.draw(self.screen):
                print("Turn the light on")
            if self.cell_button.draw(self.screen):
                print("Spawn a cell")
            if self.plant_button.draw(self.screen):
                print("Place some food")
            if self.play_button.draw(self.screen):
                print("Evolution starts")
            if self.wall_button.draw(self.screen):
                print("Build a wall")


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
