import pygame, time, datetime


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
    color = (51, 53, 53)
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
    DISPLAY_COLOR_NIGHT = (70, 80, 80)
    DISPLAY_COLOR_DAY = (135, 206, 235)

    MENU_SIZE = 100
    MENU_COLOR_NIGHT = (30, 50, 50)
    MENU_COLOR_DAY = (255, 255, 255)

    TEXT_FONT = "arial.ttf"
    TEXT_SIZE = 25
    TEXT_COLOR = (10, 20, 10)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('images/evolution.png'))  # program image
        pygame.font.init()
        self.font = pygame.font.SysFont(GUI.TEXT_FONT, GUI.TEXT_SIZE)

        self.screen = pygame.display.set_mode((GUI.DISPLAY_X, GUI.DISPLAY_Y))  # create a screen
        self.display_color = GUI.DISPLAY_COLOR_NIGHT
        self.menu_color = GUI.MENU_COLOR_NIGHT


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
        self.light = False

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
                        if x <= GUI.DISPLAY_X - GUI.MENU_SIZE - Wall.size[0]:
                            self.walls.append(Wall(x, y, self.screen))
                            self.not_available_field.append(
                                [range(x, x + Wall.size[0] + 1), range(y, y + Wall.size[1] + 1)])

                            spawn = False

    def change_light(self):
        self.display_color = GUI.DISPLAY_COLOR_DAY \
            if self.display_color == GUI.DISPLAY_COLOR_NIGHT else GUI.DISPLAY_COLOR_NIGHT
        self.menu_color = GUI.MENU_COLOR_DAY \
            if self.menu_color == GUI.MENU_COLOR_NIGHT else GUI.MENU_COLOR_NIGHT
        self.light = not self.light

    def available_coordinates(self, x, y, radius):
        x_coordinate = set(range(x - radius, x + radius + 1))
        y_coordinate = set(range(y - radius, y + radius + 1))
        for wall in self.not_available_field:
            if set(wall[0]) & x_coordinate and set(wall[1]) & y_coordinate:
                return False
        return True

    def main(self):
        time_start = time.time()
        run = True
        while run:
            self.screen.fill(self.display_color)
            for obj in [*self.cells, *self.plants, *self.walls]:
                obj.draw()
            pygame.draw.rect(self.screen, self.menu_color, pygame.Rect(GUI.DISPLAY_X - GUI.MENU_SIZE, 0, 100, 700))

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

            self.screen.blit(self.font.render('Generation X', False, GUI.TEXT_COLOR), (10, 10))
            self.screen.blit(
                self.font.render(f'Time: {str(datetime.timedelta(seconds=round(time.time() - time_start)))}', False,
                                 GUI.TEXT_COLOR), (10, 10 + GUI.TEXT_SIZE))

            # pygame.draw.rect(self.screen, (0, 102, 204), (900, 686, 100, 7))
            # pygame.draw.rect(self.screen, (245, 191, 15), (900, 693, 100, 7))
            pygame.display.update()

display = GUI()
display.main()
