import datetime
import pygame
import random
import time

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
    size = (11, 11)

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
        pygame.init()
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('images/evolution.png'))  # program image
        pygame.font.init()
        self.font = pygame.font.SysFont(GUI.TEXT_FONT, GUI.TEXT_SIZE)
        self.display_color = GUI.DISPLAY_COLOR_NIGHT
        self.menu_color = GUI.MENU_COLOR_NIGHT

        # load button images
        self.light_button = Button(940, 50, "images/idea.png", "images/idea_on.png")
        self.cell_button = Button(940, 140, "images/virus.png", "images/virus_on.png", "Cell")
        self.wall_button = Button(940, 230, "images/wall.png", "images/wall_on.png", "Wall")
        self.plant_button = Button(940, 320, "images/plant.png", "images/plant_on.png", "Plant")
        self.erase_button = Button(940, 410, "images/eraser.png", "images/eraser_on.png")
        self.play_button = Button(940, 500, "images/play-button.png", "images/video-pause-button.png")
        self.quit_button = Button(940, 590, "images/remove.png")
        self.button = None
        self.cur_spawning_button = None

        self.environment = Environment((GUI.DISPLAY_X - GUI.MENU_SIZE) // 7 + 1, GUI.DISPLAY_Y // 7 + 1)
        self.coeff = 12
        self.not_available_field = []
        self.light = False
        self.run = True

    def spawn_cell(self, name_class):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = pygame.mouse.get_pos()

                if name_class == 'Cell':
                    if self.available_coordinates(x, y, Organism.radius):
                        self.environment.set_cell(x // self.coeff, y // self.coeff, Organism(x, y))
                elif name_class == 'Plant':
                    if self.available_coordinates(x, y, Plant.radius):
                        self.environment.set_cell(x // self.coeff, y // self.coeff, Plant(x, y))
                elif name_class == 'Wall':
                    for i in range(-1, 2):
                        x_c = (x // self.coeff) * self.coeff + self.coeff*i
                        for j in range(-1, 2):
                            y_c = (y // self.coeff) * self.coeff + self.coeff*j
                            if x_c <= GUI.DISPLAY_X - GUI.MENU_SIZE - Wall.size[0]:
                                self.environment.set_cell(x_c // self.coeff, y_c // self.coeff, Wall(x_c, y_c))
            if event.type == pygame.QUIT:  # if press close button
                self.run= False

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
        if x >= GUI.DISPLAY_X-GUI.MENU_SIZE or y >= GUI.DISPLAY_Y:
            return False
        if self.environment.grid[x//self.coeff][y//self.coeff].cell_type == 'wall':
            return False
        return True

    def main(self):
        time_start = time.time()
        i = 0
        while self.run:
            GUI.SCREEN.fill(self.display_color)
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
            
            if self.erase_button.is_on and self.erase_button.draw(GUI.SCREEN):
                self.erase_button.turn_off()
            if self.erase_button.draw(GUI.SCREEN):
                self.erase_button.turn_on()
                print("Erase")

            # Quit button
            if self.quit_button.draw(GUI.SCREEN):
                self.run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    self.run= False

            clock.tick(FPS)

            GUI.SCREEN.blit(self.font.render('Generation X', False, GUI.TEXT_COLOR), (10, 10))
            GUI.SCREEN.blit(
                self.font.render(f'Time: {str(datetime.timedelta(seconds=round(time.time() - time_start)))}', False,
                                 GUI.TEXT_COLOR), (10, 10 + GUI.TEXT_SIZE))

            pygame.display.update()


if __name__ == '__main__':
    display = GUI()
    display.main()
