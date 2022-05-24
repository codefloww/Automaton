import pygame, sys
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
    radius = 7

    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)

    def draw(self):
        pygame.draw.circle(self.screen, Plant.color,
                           (self.coordinate_x, self.coordinate_y), Plant.radius, 4)


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
    Field_SIZE = 100
    DISPLAY_COLOR = (70, 80, 80)
    MENU_COLOR = (30, 50, 50)
    TEXT_FONT = "arial.ttf"
    TEXT_SIZE = 25

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(GUI.TEXT_FONT, GUI.TEXT_SIZE)
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

        self.not_available_field = []

    def spawn_cell(self, name_class):
        spawn = True
        while spawn:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    x, y = pygame.mouse.get_pos()

                    if name_class == 'Cell':
                        if self.available_coordinates(x, y, Cell.radius):
                            self.cells.append(Cell(x, y, self.screen, (70, 10, 70)))
                            spawn = False
                    elif name_class == 'Plant':
                        if self.available_coordinates(x, y, Plant.radius):
                            self.plants.append(Plant(x, y, self.screen))
                            spawn = False
                    elif name_class == 'Wall':
                        if x <= GUI.DISPLAY_X-GUI.Field_SIZE-Wall.size[0]:
                            self.walls.append(Wall(x, y, self.screen))
                            self.not_available_field.append([range(x, x+Wall.size[0]+1), range(y, y+Wall.size[1]+1)])
                            spawn = False

    def main(self):
        run = True
        while run:
            self.screen.fill(GUI.DISPLAY_COLOR)
            for obj in [*self.cells, *self.plants, *self.walls]:
                obj.draw()
            pygame.draw.rect(self.screen, GUI.MENU_COLOR, pygame.Rect(GUI.DISPLAY_X-GUI.Field_SIZE, 0, 100, 700))

            if self.light_button.draw(self.screen):
                self.change_light()
            if self.cell_button.draw(self.screen):
                self.spawn_cell('Cell')
            if self.plant_button.draw(self.screen):
                self.spawn_cell('Plant')
            if self.play_button.draw(self.screen):
                print("Evolution starts")
            if self.wall_button.draw(self.screen):
                self.spawn_cell('Wall')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    run = False
                    pygame.quit()

            text_surface = self.font.render('Generation 0', False, (10, 20, 10))
            self.screen.blit(text_surface, (10, 10))
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

    def available_coordinates(self, x, y, radius):
        x_coordinate = set(range(x - radius, x + radius + 1))
        y_coordinate = set(range(y - radius, y + radius + 1))
        for wall in self.not_available_field:
            if set(wall[0]) & x_coordinate and set(wall[1]) & y_coordinate:
                return False
        return True


display = GUI()
display.main()
