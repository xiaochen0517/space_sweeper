import logging
import math

import pygame.draw
from pygame.color import THECOLORS

from model import ShipModel, Asteroid

SCREEN_SIZE = 600


def to_pixel_points(x, y):
    return x * 20 + SCREEN_SIZE / 2, -y * 20 + SCREEN_SIZE / 2


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


def loop(screen, clock, ship, asteroids):
    screen.fill(THECOLORS['white'])

    # 绘制飞船和陨石
    draw_polygon(screen, ship)
    for asteroid in asteroids:
        draw_polygon(screen, asteroid, THECOLORS['red'])

    # 发射激光
    laser = ship.laser_segment()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        draw_segment(screen, laser, THECOLORS['green'])
        # 检查激光是否击中陨石
        for asteroid in asteroids:
            if asteroid.does_intersect(laser):
                logging.info('Hit!')
                asteroids.remove(asteroid)
    elif keys[pygame.K_LEFT]:
        ship.rotation += 0.03
        if ship.rotation > 2 * math.pi:
            ship.rotation -= 2 * math.pi
    elif keys[pygame.K_RIGHT]:
        ship.rotation -= 0.03
        if ship.rotation < 0:
            ship.rotation += 2 * math.pi

    pygame.display.flip()
    clock.tick(30)
