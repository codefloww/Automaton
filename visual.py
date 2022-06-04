import random, pygame, time, datetime
from cell import Cell
from environment import Environment
possible_cells = ['organism', 'plant', 'wall', 'empty']

# color palette
SKY_BLUE = (135, 206, 235)
YELLOW = (245, 236, 142)
GREEN = (110, 212, 123)
PURPLE = (150, 110, 212)
RED = (247, 129, 134)
FPS = 60
clock = pygame.time.Clock()


class Organism(Cell):
    radius = 10

    def __init__(self, x, y):
        colors = [YELLOW, RED, PURPLE]
        super().__init__(x, y, possible_cells[0])
        self.color = random.choice(colors)

    def draw(self):
        pygame.draw.circle(GUI.SCREEN, self.color,
                           (self.x, self.y), Organism.radius)


class Plant(Cell):
    color = (110, 212, 123)
    radius = 7

    def __init__(self, x, y):
        super().__init__(x, y, possible_cells[1])

    def draw(self):
        pygame.draw.circle(GUI.SCREEN, Plant.color,
                           (self.x, self.y), Plant.radius, 4)


class Wall(Cell):
    color = (51, 53, 53)
    size = (40, 40)

    def __init__(self, x, y):
        super().__init__(x, y, possible_cells[2])

    def draw(self):
        pygame.draw.rect(GUI.SCREEN, Wall.color,
                         (self.x, self.y, Wall.size[0], Wall.size[1]))


class Button:
    def __init__(self, x, y, path, path_on=None, created=None):
        img_off = pygame.image.load(path).convert_alpha()
        self.image_off = pygame.transform.scale(img_off, (40, 40))

        path_on = path_on or path
        img_on = pygame.image.load(path_on).convert_alpha()
        self.image_on = pygame.transform.scale(img_on, (40, 40))

        self.image = self.image_off
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
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
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clecked conditions
        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[0] and not self.clicked:  # 0 - left click

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

    MENU_SIZE = 80
    MENU_COLOR_NIGHT = (30, 50, 50)
    MENU_COLOR_DAY = (255, 255, 255)

    TEXT_FONT = "arial.ttf"
    TEXT_SIZE = 25
    TEXT_COLOR = (10, 20, 10)
    SCREEN = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))

    def __init__(self):
        self.environment = Environment(GUI.DISPLAY_X - GUI.MENU_SIZE, GUI.DISPLAY_Y)
        pygame.init()
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('images/evolution.png'))  # program image
        pygame.font.init()
        self.font = pygame.font.SysFont(GUI.TEXT_FONT, GUI.TEXT_SIZE)
        self.display_color = GUI.DISPLAY_COLOR_NIGHT
        self.menu_color = GUI.MENU_COLOR_NIGHT

        # load button images
        self.light_button = Button(940, 80, "images/idea.png", "images/idea_on.png")
        self.cell_button = Button(940, 180, "images/virus.png", "images/virus_on.png", "Cell")
        self.wall_button = Button(940, 280, "images/wall.png", "images/wall_on.png", "Wall")
        self.plant_button = Button(940, 380, "images/plant.png", "images/plant_on.png", "Plant")
        self.play_button = Button(940, 480, "images/play-button.png", "images/video-pause-button.png")
        self.quit_button = Button(940, 580, "images/remove.png")
        self.button = None
        self.cur_spawning_button = None

        # self.cells = []
        # self.plants = []
        # self.walls = []

        self.not_available_field = []
        self.light = False

    def spawn_cell(self, name_class):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = pygame.mouse.get_pos()

                if name_class == 'Cell':
                    if self.available_coordinates(x, y, Organism.radius):
                        # self.cells.append(Organism(x, y))
                        self.environment.grid[x][y] = Organism(x, y)
                elif name_class == 'Plant':
                    if self.available_coordinates(x, y, Plant.radius):
                        # self.plants.append(Plant(x, y))
                        self.environment.grid[x][y] = Plant(x, y)
                elif name_class == 'Wall':
                    if x <= GUI.DISPLAY_X - GUI.MENU_SIZE - Wall.size[0]:
                        # self.walls.append(Wall(x, y))
                        self.environment.grid[x][y] = Wall(x, y)
                        self.not_available_field.append(
                            [range(x, x + Wall.size[0] + 1), range(y, y + Wall.size[1] + 1)])

    def button_navigate(self, button):
        self.button = button
        if self.button.is_on and self.button.draw(GUI.SCREEN):
            self.button.turn_off()
            self.cur_spawning_button = None
        if self.button.draw(GUI.SCREEN) and not self.button.is_on:
            if self.cur_spawning_button is None:
                self.cur_spawning_button = self.button
                self.button.turn_on()
        if self.button.is_on:
            self.spawn_cell(self.button.created_object)

    def change_light(self):
        self.display_color = GUI.DISPLAY_COLOR_DAY \
            if self.display_color == GUI.DISPLAY_COLOR_NIGHT else GUI.DISPLAY_COLOR_NIGHT
        self.menu_color = GUI.MENU_COLOR_DAY \
            if self.menu_color == GUI.MENU_COLOR_NIGHT else GUI.MENU_COLOR_NIGHT
        self.light = not self.light

    def available_coordinates(self, x, y, radius):
        x_coordinate = set(range(x - radius, x + radius + 1))
        y_coordinate = set(range(y - radius, y + radius + 1))
        if x >= GUI.DISPLAY_X-GUI.MENU_SIZE or y >= GUI.DISPLAY_Y:
            return False
        for wall in self.not_available_field:
            if set(wall[0]) & x_coordinate and set(wall[1]) & y_coordinate:
                return False
        return True

    def main(self):
        time_start = time.time()
        run = True
        while run:
            GUI.SCREEN.fill(self.display_color)
            # for obj in [*self.cells, *self.plants, *self.walls]:
            #     obj.draw()
            for width in self.environment.grid:
                for cell in width:
                    if cell.cell_type is not None:
                        cell.draw()
            pygame.draw.rect(GUI.SCREEN, self.menu_color, pygame.Rect(GUI.DISPLAY_X - GUI.MENU_SIZE, 0, 100, 700))

            if self.light_button.is_on and self.light_button.draw(GUI.SCREEN):
                self.light_button.turn_off()
                self.change_light()
            if self.light_button.draw(GUI.SCREEN):
                self.light_button.turn_on()
                self.change_light()
                print("Turn the light on")

            # Cell button
            self.button_navigate(self.cell_button)

            # Plant button
            self.button_navigate(self.plant_button)

            # Wall button
            self.button_navigate(self.wall_button)

            # Play button
            if self.play_button.is_on and self.play_button.draw(GUI.SCREEN):
                self.play_button.turn_off()
            if self.play_button.draw(GUI.SCREEN):
                self.play_button.turn_on()
                print("Evolution starts")
            
            # Quit button
            if self.quit_button.draw(GUI.SCREEN):
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    run = False

            clock.tick(FPS)

            GUI.SCREEN.blit(self.font.render('Generation X', False, GUI.TEXT_COLOR), (10, 10))
            GUI.SCREEN.blit(
                self.font.render(f'Time: {str(datetime.timedelta(seconds=round(time.time() - time_start)))}', False,
                                 GUI.TEXT_COLOR), (10, 10 + GUI.TEXT_SIZE))

            pygame.display.update()


if __name__ == '__main__':
    display = GUI()
    display.main()
