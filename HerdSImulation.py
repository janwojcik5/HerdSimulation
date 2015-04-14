import sys, pygame
from pygame.locals import *
from math import ceil
from math import cos, sin
from random import randint
# For linear algebra
import numpy as np
import pygame 

from copy import deepcopy 


def saturate(value, max_value):
    if abs(value) > max_value:
        return np.sign(value)*max_value
    return value

class Boid:
    def __init__(self, x, y, angle, image_surface):
        
        self.pos = np.array([x, y]) 
        self.angle = angle 
                
        self.vel = np.array([0.,0.])
        self.rot_vel = 0.0
        
        self.accel = np.array([0.0, 0.0])
        self.a2 = np.array([0.,0.])
        
        self.image_surface = image_surface
        self.surf = pygame.Surface((51,51),flags=pygame.SRCALPHA)
        self.surf.set_alpha(0)
        tmp_rect = self.image_surface.get_rect()
        self.pos_rect = pygame.Rect((16,16,17,17))
        self.surf.blit(image_surface, self.pos_rect)
        
        self.max_vel = np.array([25., 20.])
        self.max_accel = np.array([12., 5.]) 
        self.repulsion_coef = 0.5
        self.max_rot_vel = 5
        
    def __repr__(self):
        return "%.0f,%.0f:%.0f,%.0f " % (self.pos[0], self.pos[1], self.vel[0], self.vel[1]) 
    
    def draw(self):
        render_angle = -(self.angle+90)
        render_surf = pygame.transform.rotozoom(self.surf, render_angle, 1.0)
        rot_rect = render_surf.get_rect(center=(self.pos[0], self.pos[1]))
      
        screen.blit(render_surf, rot_rect)
    
    def update(self, neighbors, close_neighbors, goal, predators=[]):
        self.accel = np.array([0., 0.])

        if len(predators):
            a0 = self.__avoid(predators)
        else:
            a0 = np.array([0.,0.])
        a1 = self.__avoid(close_neighbors)
        a2 = self.__seekgoal(goal)
        a3 = self.__centering(neighbors)
        a4, rot_vel = self.__velocity(neighbors)

        self.accel = 100*a0 

        if np.linalg.norm(self.accel) < self.max_accel[0]:
           new_accel = self.accel + 10*a1
           if np.linalg.norm(self.accel) < self.max_accel[0]:
               self.accel = new_accel

        if np.linalg.norm(self.accel) < self.max_accel[0]:
           new_accel = self.accel + 0.02*a2
           if np.linalg.norm(self.accel) < self.max_accel[0]:
               self.accel = new_accel
        if np.linalg.norm(self.accel) < self.max_accel[0]:
            new_accel = self.accel + 0.02*a3
            if np.linalg.norm(new_accel) < self.max_accel[0]:
                self.accel = new_accel
        if np.linalg.norm(self.accel) < self.max_accel[0]:
            new_accel = self.accel + 0.02*a4
            if np.linalg.norm(new_accel) < self.max_accel[0]:
                self.accel = new_accel
        
        self.vel = self.accel# + 0.1*self.vel

        if np.linalg.norm(self.vel) > self.max_vel[0]:
            self.vel /= np.linalg.norm(self.vel)
            self.vel *= self.max_vel[0]
        
        if np.linalg.norm(self.vel) != 0:
            dir_mvt = np.rad2deg(np.arctan2(self.vel[1],self.vel[0]))
            self.angle = dir_mvt
            self.angle %= 360
       
        self.pos += self.vel

        self.pos[0] %= 1024 
        self.pos[1] %= 768 
    

    def __avoid(self, close_neighbors):
        xdot = np.array([0.,0.])
        for i in close_neighbors:
            if i[1] == 0:
                xdot -= i[0].vel
            else:
                xdot -= (i[0].pos-self.pos)/i[1]*(1.0/(i[1])) 
        return xdot

    def __velocity(self, neighbors):
        if len(neighbors) == 0:
            return self.vel, self.rot_vel

        sum_vel = np.array([0.,0.])
        sum_rot_vel = 0.

        for i in neighbors:
            sum_vel += i[0].vel
            sum_rot_vel += i[0].rot_vel

        sum_vel /= len(neighbors)
        sum_rot_vel /= len(neighbors)
        
        return sum_vel, sum_rot_vel

    def __centering(self, neighbors):
        center = np.array([0.,0.])
        
        if len(neighbors) == 0:
            return center
            
        for i in neighbors:
            center += i[0].pos
        
        center /= len(neighbors)
        accel_request = (center - self.pos) 
        
        return accel_request

    def __seekgoal(self, goal):
        accel_request = (goal-self.pos)
        
        if np.linalg.norm(accel_request) < 500:
        	return accel_request
        if np.linalg.norm(accel_request) != 0:
           accel_request /= np.linalg.norm(accel_request)
        else:
           accel_request = np.array([0.,0.],dtype=np.float64)
        return accel_request
    
class Flock:

    def __init__(self, count, safe_distance, neighbor_distance):
        self.image_surface = pygame.image.load("img/boid-red.png").convert_alpha()
        self.safe_distance = safe_distance
        self.neighbor_distance = neighbor_distance
        self.boid_list = [ Boid(randint(1,1023), randint(1,768), randint(0,360), self.image_surface) for i in range(count) ]
        self.goal = np.array([0.0, 0.0], dtype=np.float64)
        self.mouse_pos = (0,0) 
        self.mouse_predator = False


    def draw(self):
        for i in self.boid_list:
            i.draw()

        pygame.draw.circle(screen, (0,255,0), self.goal.astype(int), 10) 

        if self.mouse_predator is True:
            pygame.draw.circle(screen, (255,0,0), self.mouse_pos, 10)
        
    def update(self, mouse_pos, mouse_predator):
        static_boid_list = self.boid_list[:] 
        self.mouse_predator = mouse_predator
        self.mouse_pos = mouse_pos
        for i in self.boid_list:

            close_neighbors = []
            neighbors = []
            predators = []
            
            if self.mouse_predator:
                predator = Boid(mouse_pos[0], mouse_pos[1], 0,  self.image_surface)
                vector_diff = i.pos - predator.pos
                distance = np.linalg.norm(vector_diff)
                if distance < self.safe_distance:
                    predators.append( (predator, distance) )
            else:
                self.goal[0] = mouse_pos[0]
                self.goal[1] = mouse_pos[1]
            for j in static_boid_list:
                vector_diff = i.pos-j.pos
                distance = np.linalg.norm(vector_diff)
                if j == i:
                    continue
                if distance < self.safe_distance:
                    close_neighbors.append( (j, distance) )
                if distance < self.neighbor_distance:
                    neighbors.append( (j,distance) )

            i.update(neighbors, close_neighbors, self.goal, predators)



pygame.init()
fpsClock = pygame.time.Clock()

width = 1024
height = 768
size = (width, height)

black = 1.0, 1.0, 1.0
white = 255,255,255
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Herd Simulation")


f = Flock(30, 100., 500.) # [number of boids], [avoidance_distance], [neighborhood_distance]
f.draw()
pygame.display.flip()

g_mouse_predator = False


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
        if event.type == pygame.MOUSEBUTTONDOWN:
            g_mouse_predator = not g_mouse_predator
    if True:
                screen.fill(white)
                f.update(pygame.mouse.get_pos(), g_mouse_predator)
                f.draw()
                pygame.display.flip()
