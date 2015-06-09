import random
import pygame
import math
import time
from pygame.locals import *

# CONSTANTS

MAX_POSITION_X = 800
MIN_POSITION_X = 0
MAX_POSITION_Y = 600
MIN_POSITION_Y = 0

white = 255, 255, 255

# PARAMETERS

MAX_VELOCITY = 5
SIGHT_RANGE = 350
TOO_CLOSE_RANGE = 20

RULE1_DIVIDER = 100
RULE3_DIVIDER = 8

SEE_ANGLE = 120

WAIT_TIME = 0.1

MIN_VELOCITY = -MAX_VELOCITY

IS_RUNNING = False

class Boid(object):
    # pozycja i predkosc sa listami dwuelementowymi
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __str__(self):
        return str(self.position) + " " + str(self.velocity)

    def __repr__(self):
        return str(self.position) + " " + str(self.velocity)

    def is_in_angle(self,another_boid):
    	k1 = math.atan2(self.velocity[1],self.velocity[0])
     	k2 = math.atan2((another_boid.position[1]-self.position[1]),(another_boid.position[0]-self.position[0]))

    	if abs(k1-k2) < SEE_ANGLE:
    		return True
    	return False


    # sprawdzanie, czy dwa boidy leza w swoim zasiegu
    def in_range(self, another_boid):
        if math.sqrt(math.pow(self.position[0] - another_boid.position[0], 2)
                + math.pow(self.position[1] - another_boid.position[1], 2)) < SIGHT_RANGE and self.is_in_angle(another_boid) :
            return True
        return False

    def is_tooClose(self, another_boid):
        if math.sqrt(math.pow(self.position[0] - another_boid.position[0], 2)
                + math.pow(self.position[1] - another_boid.position[1], 2)) < TOO_CLOSE_RANGE and self.is_in_angle(another_boid):
            return True
        return False


class World(object):
    # display - zmienna reprezentujaca okno, na ktorym wyswietlamy boidy
    def __init__(self, number_of_boids, display=None):
        self.number_of_boids = number_of_boids
        self.boids = []
        for i in range(number_of_boids):
            position = [random.uniform(MIN_POSITION_X, MAX_POSITION_X), random.uniform(MIN_POSITION_Y, MAX_POSITION_Y)]
            velocity = [random.uniform(MIN_VELOCITY, MAX_VELOCITY), random.uniform(MIN_VELOCITY, MAX_VELOCITY)]
            self.boids.append(Boid(position, velocity))
        self.display = display


    def __str__(self):
        return str(self.boids)

    def rule1(self, boid):
        count = 0.0
        s = [0.0, 0.0]
        for boid2 in self.boids:
            if boid.in_range(boid2):
                s[0] += boid2.position[0]
                s[1] += boid2.position[1]
                count += 1.0
        if count == 0.0:
            return [0.0, 0.0]
        s[0] /= count
        s[1] /= count
        s[0] -= boid.position[0]
        s[1] -= boid.position[1]
        s[0] /= RULE1_DIVIDER
        s[1] /= RULE1_DIVIDER
        return s

    def rule2(self, boid):
        c = [0, 0]
        for another_boid in self.boids:
            if another_boid != boid:
                if boid.is_tooClose(another_boid):
                    c[0] = c[0] - ( another_boid.position[0] - boid.position[0])
                    c[1] = c[1] - ( another_boid.position[1] - boid.position[1])
        return c

    def rule3(self, boid):
        count = 0.0
        s = [0.0, 0.0]
        for boid2 in self.boids:
            if boid.in_range(boid2):
                s[0] += boid2.velocity[0]
                s[1] += boid2.velocity[1]
                count += 1.0
        if count == 0.0:
            return [0.0, 0.0]
        s[0] /= count
        s[1] /= count
        s[0] /= RULE3_DIVIDER
        s[1] /= RULE3_DIVIDER
        return s

    def move_all_boids_to_new_positions(self):
        for boid in self.boids:

            # kazda z funkcji zwraca tuple ze skladowymi x i y predkosci
            rule1_velocity = self.rule1(boid)
            rule2_velocity = self.rule2(boid)
            rule3_velocity = self.rule3(boid)
            # print rule1_velocity
            # print rule2_velocity
            # print rule3_velocity
            # print " "

            new_velocity_x = boid.velocity[0] + rule1_velocity[0] + rule2_velocity[0] + rule3_velocity[0]
            if abs(new_velocity_x) > MAX_VELOCITY:
                new_velocity_x = math.copysign(MAX_VELOCITY, new_velocity_x) * 0.75
            new_x = abs((boid.position[0] + new_velocity_x) % MAX_POSITION_X)
            boid.position[0] = new_x
            boid.velocity[0] = new_velocity_x

            new_velocity_y = boid.velocity[1] + rule1_velocity[1] + rule2_velocity[1] + rule3_velocity[1]
            if abs(new_velocity_y) > MAX_VELOCITY:
                new_velocity_y = math.copysign(MAX_VELOCITY, new_velocity_y) * 0.75
            new_y = abs((boid.position[1] + new_velocity_y) % MAX_POSITION_Y)
            boid.position[1] = new_y
            boid.velocity[1] = new_velocity_y


    def draw_boids(self):
        self.display.clean_screen()
        for i in self.boids:
            self.display.draw_object(i, "./img/boid-red.png")


# Klasa reprezentujaca okno, w ktorym wyswietlamy boidy
class Display():
    def __init__(self):
        self.screen = pygame.display.set_mode((MAX_POSITION_X - MIN_POSITION_X, MAX_POSITION_Y - MIN_POSITION_Y),
                                              DOUBLEBUF)
        # flyweight pattern
        self.image_dictionary = {}

    def draw_object(self, obj, object_image):
        if not object_image in self.image_dictionary:
            self.image_dictionary[object_image] = pygame.image.load(object_image)
        if obj.velocity[0] != 0.0 and obj.velocity[1] != 0.0:
            rotated = pygame.transform.rotate(self.image_dictionary[object_image],
                                              -90 - (180 / math.pi) * math.atan2(obj.velocity[1], obj.velocity[0]))
        self.screen.blit(rotated, (obj.position[0], obj.position[1]))
        pygame.display.flip()

    def clean_screen(self):
        self.screen.fill(white)


def loop(world):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        world.move_all_boids_to_new_positions()
        world.draw_boids()
        # time.sleep(WAIT_TIME) # if we need sleep for slower simulation


def start():
    world = World(30, Display())
    loop(world)


if __name__ == "__main__":
    IS_RUNNING = True
    start()