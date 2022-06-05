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
COEFF = 17
FPS = 60
clock = pygame.time.Clock()


class Organism(Cell):
    radius = 10

    def __init__(self, x, y,  light):
        colors = [YELLOW, RED, PURPLE]
        super().__init__(x, y, possible_cells[0], light)
        self.color = random.choice(colors)

    def draw(self):
        pygame.draw.circle(GUI.SCREEN, self.color,
                           (self.x, self.y), Organism.radius)


class Plant(Cell):
    color = (110, 212, 123)
    radius = 7

    def __init__(self, x, y,  light):
        super().__init__(x, y, possible_cells[1], light)

    def draw(self):
        pygame.draw.circle(GUI.SCREEN, Plant.color,
                           (self.x, self.y), Plant.radius, 4)


class Wall(Cell):
    color = (51, 53, 53)
    size = (16, 16)

    def __init__(self, x, y, light):
        super().__init__(x, y, possible_cells[2], light)

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


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class GUI:
    DISPLAY_X = 1000
    DISPLAY_Y = 700
    MENU_SIZE = 80
    SCREEN = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))

    def __init__(self, environment):
        """
        initialisation of the display, started color theme, buttons
        """
        pygame.init()
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('images/evolution.png'))  # program image
        pygame.font.init()

        self.font = pygame.font.SysFont("arial.ttf", 25)
        self.menu_color = (30, 50, 50)
        self.display_image = Background("images/green_bg.png", [0, 0]).image

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

        self.coeff = GUI.DISPLAY_X // environment.width
        self.environment = environment
        self.queue_cell = []
        self.erase = False
        self.run = True

    def spawn_cell(self, name_class):
        """
        user can spawn or erase(/Сtrl+Z) сells
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.KMOD_CTRL:
                    deleted = False
                    while not deleted:
                        if self.queue_cell:
                            for x, y in self.queue_cell.pop():
                                if self.environment.get_cell(x, y).cell_type != 'empty':
                                    self.environment.set_cell(x, y, Cell(x, y, 'empty', self.environment.light))
                                    deleted = True
                        else:
                            deleted = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if self.erase:
                    if x < GUI.DISPLAY_X - GUI.MENU_SIZE and y < GUI.DISPLAY_Y and \
                            self.environment.get_cell(x // self.coeff, y // self.coeff).cell_type != 'empty':
                        self.environment.set_cell(x // self.coeff, y // self.coeff, Cell(x, y, 'empty', self.environment.light))
                elif name_class == 'Cell':
                    x = (x // self.coeff) * self.coeff + self.coeff // 2
                    y = (y // self.coeff) * self.coeff + self.coeff // 2
                    self.add_cell(x, y, Organism(x, y, self.environment.light))
                elif name_class == 'Plant':
                    self.add_cell(x, y, Plant(x, y, self.environment.light))
                elif name_class == 'Wall':
                    for i in range(-1, 1):
                        x_c = (x // self.coeff) * self.coeff + self.coeff * i
                        for j in range(-1, 1):
                            y_c = (y // self.coeff) * self.coeff + self.coeff * j
                            self.add_cell(x_c, y_c, Wall(x_c, y_c, self.environment.light), [16, i, j])
            if event.type == pygame.QUIT:  # if press close button
                self.run = False

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
        """
        change colors on the screen;
        change light argument in the environment;
        """
        self.environment.light = not self.environment.light
        if self.environment.light:
            self.environment.set_light(True)
            self.display_image = Background("images/blue_bg.png", [0, 0]).image
            self.menu_color = (255, 255, 255)
        else:
            self.environment.set_light(False)
            self.display_image = Background("images/green_bg.png", [0, 0]).image
            self.menu_color = (30, 50, 50)

    def add_cell(self, x, y, cell, size=None):
        """
        check (x, y) coordinates;
        add cells to the grid and queue if coordinates is correct;
        """
        if cell.cell_type == 'wall':
            if x < GUI.DISPLAY_X - GUI.MENU_SIZE - size[0] or y <= GUI.DISPLAY_Y:
                self.environment.set_cell(x // self.coeff, y // self.coeff, cell)
                if size[1] == -1 and size[2] == -1:
                    self.queue_cell.append([(x // self.coeff, y // self.coeff)])
                else:
                    self.queue_cell[-1].append((x // self.coeff, y // self.coeff))
        else:
            if x < GUI.DISPLAY_X - GUI.MENU_SIZE or y < GUI.DISPLAY_Y:
                self.environment.set_cell(x // self.coeff, y // self.coeff, cell)
                self.queue_cell.append([(x // self.coeff, y // self.coeff)])
                return True
        return False

    def main(self):
        """
        draw all objects that could be changed
        """
        time_start = time.time()
        while self.run:
            GUI.SCREEN.blit(self.display_image, (0, 0))
            for width in self.environment.grid:
                for cell in width:
                    if cell.cell_type != 'empty':
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

            # Erase button
            if self.erase_button.is_on and self.erase_button.draw(GUI.SCREEN):
                self.erase = False
                self.erase_button.turn_off()
            if self.erase_button.draw(GUI.SCREEN):
                self.erase = True
                self.erase_button.turn_on()

            # Quit button
            if self.quit_button.draw(GUI.SCREEN):
                self.run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    self.run = False

            clock.tick(FPS)


            GUI.SCREEN.blit(self.font.render('Generation X', False, (10, 20, 10)), (10, 10))
            GUI.SCREEN.blit(
                self.font.render(f'Time: {str(datetime.timedelta(seconds=round(time.time() - time_start)))}',
                                 False, (10, 20, 10)), (10, 10 + 25))

            pygame.display.update()


if __name__ == '__main__':
    display = GUI(Environment(55, 42))
    display.main()
