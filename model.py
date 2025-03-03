import math
from random import randint, uniform

import vectors
from vectors import distance
import numpy as np


# def segments_intersect(a, b, c, d):
#     # 判断两线段是否相交
#     def ccw(a, b, c):
#         return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
#
#     return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def standard_form(a, b):
    return b[1] - a[1], a[0] - b[0], a[0] * b[1] - a[1] * b[0]


def intersection(a, b, c, d):
    a1, b1, c1 = standard_form(a, b)
    a2, b2, c2 = standard_form(c, d)
    m = np.array([[a1, b1], [a2, b2]])
    c = np.array([c1, c2])
    return np.linalg.solve(m, c)


def segments_intersect(a, b, c, d):
    d1 = distance(a, b)
    d2 = distance(c, d)
    try:
        x, y = intersection(a, b, c, d)
        return (distance(a, (x, y)) <= d1
                and distance(b, (x, y)) <= d1
                and distance(c, (x, y)) <= d2
                and distance(d, (x, y)) <= d2)
    except np.linalg.LinAlgError:
        return False


class PolygonModel():
    def __init__(self, points: list):
        self.points = points
        self.rotation = 0
        self.x = 0
        self.y = 0

    def rotate_point(self, x, y):
        # 旋转点
        return (
            x * math.cos(self.rotation) - y * math.sin(self.rotation),
            x * math.sin(self.rotation) + y * math.cos(self.rotation)
        )

    def transformed(self):
        # 计算旋转后的点
        rotated_points = [self.rotate_point(x, y) for x, y in self.points]
        return [(x + self.x, y + self.y) for x, y in rotated_points]

    def does_intersect(self, line):
        # 判断当前多边形是否与线段相交
        for i in range(0, len(self.points)):
            start = self.transformed()[i]
            end = self.transformed()[(i + 1) % len(self.points)]
            if segments_intersect(start, end, line[0], line[1]):
                return True


class ShipModel(PolygonModel):
    def __init__(self):
        super().__init__([
            (-0.5, -0.5),
            (0.5, -0.5),
            (0, 0.7)
        ])

    def laser_segment(self):
        dist = 10.
        x, y = self.transformed()[2]
        return (
            (x, y),
            (x + dist * math.sin(-self.rotation), y + dist * math.cos(-self.rotation))
        )


class Asteroid(PolygonModel):
    def __init__(self):
        sides = randint(5, 9)
        vs = [vectors.to_cartesian((uniform(0.5, 1), 2 * math.pi * i / sides)) for i in range(0, sides)]
        super().__init__(vs)
        self.x = randint(-10, 10)
        self.y = randint(-10, 10)
