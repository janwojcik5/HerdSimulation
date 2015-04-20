#import simpy
import random
import pygame
import math

MAX_POSITION_X=1024
MIN_POSITION_X=0

MAX_POSITION_Y=768
MIN_POSITION_Y=0

MAX_VELOCITY=-5
MIN_VELOCITY=5

class Boid(object):
  
  #pozycja i predkosc sa listami dwuelementowymi
  def __init__(self,position,velocity):
    self.position=position
    self.velocity=velocity
    
  def __str__(self):
    return str(self.position)+" "+str(self.velocity)
  
  def __repr__(self):
    return str(self.position)+" "+str(self.velocity)
    
class World(object):
  
  #display - zmienna reprezentujaca okno, na ktorym wyswietlamy boidy 
  def __init__(self,number_of_boids,display=None):
    self.number_of_boids=number_of_boids
    self.boids=[]
    for i in range(number_of_boids):
      position=[]
      position.append(random.uniform(MIN_POSITION_X,MAX_POSITION_X))
      position.append(random.uniform(MIN_POSITION_Y,MAX_POSITION_Y))
      velocity=[]
      velocity.append(random.uniform(MIN_VELOCITY,MAX_VELOCITY))
      velocity.append(random.uniform(MIN_VELOCITY,MAX_VELOCITY))
      self.boids.append(Boid(position,velocity))
      
  def __str__(self):
    return str(self.boids)
  
  def move_all_boids_to_new_positions(self):
    self.boids=[]
    for i in range(self.number_of_boids):
      position=[]
      position.append(random.uniform(MIN_POSITION,MAX_POSITION))
      position.append(random.uniform(MIN_POSITION,MAX_POSITION))
      velocity=[]
      velocity.append(random.uniform(MIN_VELOCITY,MAX_VELOCITY))
      velocity.append(random.uniform(MIN_VELOCITY,MAX_VELOCITY))
      self.boids.append(Boid(position,velocity))    
  
  def draw_boids(self):
    for i in self.boids:
      

#Klasa reprezentujaca okno, w ktorym wyswietlamy boidy
class Display():
  
  def __init__(self):
    self.screen=pygame.display.set_mode((MAX_POSITION_X-MIN_POSITION_X),(MAX_POSITION_Y-MIN_POSITION_Y))
    
  def draw_object(self,obj,object_image):
    pygame_image=pygame.image.load(object_image)
    if obj.velocity[0]!=0.0 and obj.velocity[1]!=0.0:
      pygame.transform.rotate(pygame_image,math.atan2(obj.velocity[0],obj.velocity[1])
    screen.blit(pygame_image,(obj.position[0],obj.position[1]))
    pygame.display.flip()
    
    
#glowna petla: tu sie bedzie wszystko wykonywalo
def loop(env):
  pass
  
herd=Herd(5)
print herd
