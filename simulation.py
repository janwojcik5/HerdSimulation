#import simpy
import random
import pygame
import math
import time

MAX_POSITION_X=1024
MIN_POSITION_X=0

MAX_POSITION_Y=768
MIN_POSITION_Y=0

MAX_VELOCITY=-5
MIN_VELOCITY=5

white = 255,255,255

class Boid(object):
  
  #pozycja i predkosc sa listami dwuelementowymi
  def __init__(self,position,velocity):
    self.position=position
    self.velocity=velocity
    
  def __str__(self):
    return str(self.position)+" "+str(self.velocity)
  
  def __repr__(self):
    return str(self.position)+" "+str(self.velocity)
  
  #sprawdzanie, czy dwa boidy leza w swoim zasiegu
  def in_range(self,another_boid):
    #tymczasowe rozwiazanie
    return True
    
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
    self.display=display
      
      
  def __str__(self):
    return str(self.boids)
  
  def move_all_boids_to_new_positions(self):
    for boid in self.boids:
      
      #kazda z funkcji zwraca tuple ze skladowymi x i y predkosci
      rule1_velocity=self.rule1(boid)
      rule2_velocity=self.rule2(boid)
      print rule2_velocity
      rule3_velocity=self.rule3(boid)
      
      newX = boid.position[0]+boid.velocity[0]
      if 0 > newX or newX > MAX_POSITION_X:
        newX = boid.position[0]-boid.velocity[0]
        boid.velocity[0]= -boid.velocity[0]
      boid.position[0] = newX 

      newY = boid.position[1]+boid.velocity[1]
      if 0 > newY or newY > MAX_POSITION_Y:
        newY = boid.position[1]-boid.velocity[1]
        boid.velocity[1]= -boid.velocity[1]
      boid.position[1] = newY 

  def rule1(self,boid):
    count=0.0
    s=[0.0,0.0]
    for boid2 in self.boids:
      if boid.in_range(boid2):
	s[0]+=boid2.position[0]
	s[1]+=boid2.position[1]
	count+=1.0
    s[0]/=count
    s[1]/=count
    return s
  
  def rule2(self,boid):
    c = [0,0];
    for another_boid in self.boids:
      if another_boid != boid:
        if boid.in_range(another_boid):
          c[0] = c[0] - ( another_boid.position[0]-boid.position[0])
          c[1] = c[1] - ( another_boid.position[1]-boid.position[1])
    return c

  def rule3(self,boid):
    pass
  
  def draw_boids(self):
    self.display.clean_screen()
    for i in self.boids:
      self.display.draw_object(i,"./img/boid-red.png")

#Klasa reprezentujaca okno, w ktorym wyswietlamy boidy
class Display():
  
  def __init__(self):
    self.screen=pygame.display.set_mode((MAX_POSITION_X-MIN_POSITION_X,MAX_POSITION_Y-MIN_POSITION_Y))
    #flyweight pattern
    self.image_dictionary={}
    
  def draw_object(self,obj,object_image):
    if not object_image in self.image_dictionary:
      self.image_dictionary[object_image]=pygame.image.load(object_image)
    if (obj.velocity[0]!=0.0 and obj.velocity[1]!=0.0):
      rotated=pygame.transform.rotate(self.image_dictionary[object_image],-90-(180/math.pi)*math.atan2(obj.velocity[1],obj.velocity[0]))
      print str((180/math.pi)*math.atan2(obj.velocity[1],obj.velocity[0]))+" "+str(obj.velocity[1])+" "+str(obj.velocity[0])
    self.screen.blit(rotated,(obj.position[0],obj.position[1]))
    pygame.display.flip()

  def clean_screen(self):
    self.screen.fill(white)
    pygame.display.flip()
    
    
#glowna petla: tu sie bedzie wszystko wykonywalo
def loop(world):
  while True:
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
	pygame.quit()
    world.move_all_boids_to_new_positions()
    world.draw_boids()
    time.sleep(0.1)
  
world=World(5,Display())
print world

loop(world)