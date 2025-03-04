import logging
import math

import pygame.draw
from pygame.color import THECOLORS

from model import ShipModel, Asteroid

SCREEN_SIZE = 600


def to_pixel_points(x, y):
    return x * 30 + SCREEN_SIZE / 2, -y * 30 + SCREEN_SIZE / 2


def draw_polygon(screen, polygon, color=THECOLORS['blue']):
    pixel_points = [to_pixel_points(x, y) for x, y in polygon.transformed()]
    pygame.draw.aalines(screen, color, True, pixel_points)


def draw_segment(screen, segment, color=THECOLORS['blue']):
    start, end = segment
    pygame.draw.aaline(screen, color, to_pixel_points(*start), to_pixel_points(*end))


def init_ship():
    ship = ShipModel()
    return ship


def init_asteroids():
    return [Asteroid() for _ in range(0, 20)]


def render():
    ship = init_ship()
    asteroids = init_asteroids()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Arcade Game")
    clock = pygame.time.Clock()

    while True:
        loop(screen, clock, ship, asteroids)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


acceleration = 3


def loop(screen, clock, ship, asteroids):
    screen.fill(THECOLORS['white'])

    milliseconds = clock.get_time()

    # 绘制陨石
    for asteroid in asteroids:
        asteroid.move(milliseconds)
        draw_polygon(screen, asteroid, THECOLORS['red'])

    keys = pygame.key.get_pressed()
    # 控制飞船的旋转
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        pass
    else:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship.rotation += 0.03
            if ship.rotation > 2 * math.pi:
                ship.rotation -= 2 * math.pi
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship.rotation -= 0.03
            if ship.rotation < 0:
                ship.rotation += 2 * math.pi

    # 控制飞船的移动
    ship_color = THECOLORS['blue']
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        # 计算飞船的方向
        ax = acceleration * math.sin(-ship.rotation)
        ay = acceleration * math.cos(-ship.rotation)
        ship.vx += ax * milliseconds / 1000.0
        ship.vy += ay * milliseconds / 1000.0
        ship_color = THECOLORS['green']

    # 绘制飞船
    ship.move(milliseconds)
    draw_polygon(screen, ship, ship_color)

    # 发射激光
    if keys[pygame.K_SPACE]:
        laser = ship.laser_segment()
        draw_segment(screen, laser, THECOLORS['green'])
        # 检查激光是否击中陨石
        for asteroid in asteroids:
            if asteroid.does_intersect(laser):
                logging.info('Hit!')
                asteroids.remove(asteroid)

    pygame.display.flip()
    clock.tick(30)
