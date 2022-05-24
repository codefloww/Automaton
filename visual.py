import pygame, sys
DISPLAY_X = 1000
DISPLAY_Y = 700


class Object:
    def __init__(self, x, y):
        self.coordinate_x = x
        self.coordinate_y = y


class Cell(Object):
    pass


class Plant(Object):
    pass


class Wall(Object):
    pass


class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))  # create a screen
        pygame.display.set_caption('Evolution Game')
        pygame.display.set_icon(pygame.image.load('../Automaton/images/evolution.png'))  # program image

    def main(self):
        while True:
            self.screen.fill((70, 80, 80))
            mx, my = pygame.mouse.get_pos()
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if press close button
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()


display = GUI()
display.main()

