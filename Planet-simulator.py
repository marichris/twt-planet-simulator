# -*- coding: utf-8 -*-

import pygame
import math
pygame.init()

WIDTH, HEIGTH = 800, 800
WIN = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption('Planet Simulation')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
MEDIUM_BLUE = (0, 120, 146)
LIGHT_BLUE = (172, 229, 238)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
LIGHT_BROWN = (210, 180 ,140)

FONT = pygame.font.SysFont("arial", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 12.5 / AU
    TIME_STEP = 3600*24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGTH/2

        if len(self.orbit) > 2:
            updated_points= []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGTH/2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 1)    

        pygame.draw.circle(win, self.color, (x,y),self.radius)

        #if not self.sun:
        #  distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)} km", 1, WHITE)
        #  win.blit(distance_text, (x - distance_text.get_width()/2, y- distance_text.get_height()/2))

    def attraction(self, other):
        #distancia de dois objetos
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        #forca de atracao
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIME_STEP
        self.y_vel += total_fy / self.mass * self.TIME_STEP

        self.x += self.x_vel * self.TIME_STEP
        self.y += self.y_vel * self.TIME_STEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 696350000*Planet.SCALE, YELLOW, 1.98892*10**30)
    sun.sun = True

    mercury = Planet(-0.387*Planet.AU, 0, 2439000*Planet.SCALE, DARK_GREY, 3.30*10**23)
    mercury.y_vel = 47.4*1000

    venus = Planet(-0.723*Planet.AU, 0, 6000000*Planet.SCALE, WHITE, 4.8685*10**24)
    venus.y_vel = 35.02*1000

    earth = Planet(-1*Planet.AU, 0, 6378000*Planet.SCALE, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783*1000

    mars = Planet(-1.524*Planet.AU, 0, 3393500*Planet.SCALE, RED, 6.39*10**23)
    mars.y_vel = 24.077*1000

    jupiter = Planet(-5.20*Planet.AU, 0, 71400000*Planet.SCALE, LIGHT_BROWN, 1.8986*10**27)
    jupiter.y_vel = 13.07*1000

    saturn = Planet(-9.53*Planet.AU, 0, 60300000*Planet.SCALE, LIGHT_BROWN, 5.683*10**26)
    saturn.y_vel = 9.69*1000

    uranus = Planet(-19.10*Planet.AU, 0, 25900000*Planet.SCALE, LIGHT_BLUE, 8.681*10**25)
    uranus.y_vel = 6.81*1000

    neptune = Planet(-30.00*Planet.AU, 0, 24550000*Planet.SCALE, MEDIUM_BLUE, 1.024*10**26)
    neptune.y_vel = 5.43*1000
    
    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()

main()


