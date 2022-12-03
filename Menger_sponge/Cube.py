import numpy as np
import pygame as pg
from random import choices
import numba

WHITE = (255, 255, 255)
COLORS = [(255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255), (0, 255, 0)]

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
]).astype(float)


def connect_points(surface, i, j, p):
    pg.draw.line(surface, WHITE, (p[i][0], p[i][1]), (p[j][0], p[j][1]))


@numba.jit(nopython=True)
def get_proj(rot_x, rot_y, rot_z, point):
    rotz = np.dot(rot_z, point.reshape((3, 1)))
    roty = np.dot(rot_y, rotz)
    rotx = np.dot(rot_x, roty)

    return np.dot(projection_matrix, rotx)


class Cube:
    def __init__(self, x, y, z, centerx, centry, length):
        self.centerx = centerx
        self.centery = centry

        self.points = []

        self.points.append(np.matrix([x - length, y - length, z]))
        self.points.append(np.matrix([x, y - length, z]))
        self.points.append(np.matrix([x, y, z]))
        self.points.append(np.matrix([x - length, y, z]))
        self.points.append(np.matrix([x - length, y - length, z - length]))
        self.points.append(np.matrix([x, y - length, z - length]))
        self.points.append(np.matrix([x, y, z - length]))
        self.points.append(np.matrix([x - length, y, z - length]))

        self.x = x
        self.y = y
        self.z = z

        self.projected_points = [
            [n, n] for n in range(len(self.points))
        ]

        self.length = length

        self.color = choices(COLORS)[0]

    def update(self):
        new_cubes = {}
        length_new = self.length / 3

        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if abs(i) + abs(j) + abs(k) <= 1:
                        x_new = self.x - length_new * (i + 1)
                        y_new = self.y - length_new * (j + 1)
                        z_new = self.z - length_new * (k + 1)
                        cube = Cube(x_new, y_new, z_new
                                    , self.centerx, self.centery, length_new)
                        key = tuple((x_new, y_new, z_new))
                        new_cubes[key] = cube

        return new_cubes

    def draw(self, surface, rotation_x, rotation_y, rotation_z):
        i = 0
        for point in self.points:

            projected2d = get_proj(rotation_x, rotation_y, rotation_z, point)
            x = int(projected2d[0][0]) + self.centerx
            y = int(projected2d[1][0]) + self.centery

            #pg.draw.circle(surface, WHITE, (x, y), 5)

            self.projected_points[i] = [x, y]
            i += 1

        for p in range(4):
            connect_points(surface, p, (p+1) % 4, self.projected_points)
            connect_points(surface, p+4, ((p+1) % 4) + 4, self.projected_points)
            connect_points(surface, p, (p+4), self.projected_points)

