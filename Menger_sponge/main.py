import pygame as pg
from pygame.locals import *
import sys
from Cube import *


# global variables
WIDTH = 1260
HEIGHT = 900
FPS = 30
BLACK = (0, 0, 0)

SCALE = 486
SCALE_HALF = SCALE / 2


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Menger Sponge")
        self.clock = pg.time.Clock()
        self.surface = pg.display.get_surface()

        self.angle = 0

        self.cubes = {(SCALE_HALF, SCALE_HALF, SCALE_HALF):
                        Cube(SCALE_HALF, SCALE_HALF, SCALE_HALF,  WIDTH / 2, HEIGHT / 2, SCALE)}

        self.rotation_z = np.matrix([
            [cos(self.angle), -sin(self.angle), 0],
            [sin(self.angle), cos(self.angle), 0],
            [0, 0, 1],
        ]).astype(float)

        self.rotation_y = np.matrix([
            [cos(self.angle), 0, sin(self.angle)],
            [0, 1, 0],
            [-sin(self.angle), 0, cos(self.angle)],
        ]).astype(float)

        self.rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(self.angle), -sin(self.angle)],
            [0, sin(self.angle), cos(self.angle)],
        ]).astype(float)

    def game_loop(self):
        while True:
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONUP:
                    new_cubes = {}
                    for cube in self.cubes.values():
                        new_cubes.update(cube.update())
                    self.cubes = new_cubes

            self.screen.fill(BLACK)

            for cube in self.cubes.values():
                cube.draw(self.surface, self.rotation_x, self.rotation_y, self.rotation_z)
            self.angle += 0.02

            x = cos(self.angle)
            y = sin(self.angle)

            self.rotation_z[0, 0] = x
            self.rotation_z[0, 1] = -y
            self.rotation_z[1, 0] = y
            self.rotation_z[1, 1] = x

            self.rotation_y[0, 0] = x
            self.rotation_y[0, 2] = y
            self.rotation_y[2, 0] = -y
            self.rotation_y[2, 2] = x

            self.rotation_x[1, 1] = x
            self.rotation_x[1, 2] = -y
            self.rotation_x[2, 1] = y
            self.rotation_x[2, 2] = x

            pg.display.flip()


game = Game()
game.game_loop()
