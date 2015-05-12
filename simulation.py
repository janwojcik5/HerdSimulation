import random
import pygame
import math
import time
from pygame.locals import *

MAX_POSITION_X=800
MIN_POSITION_X=0

MAX_POSITION_Y=600
MIN_POSITION_Y=0

MAX_VELOCITY=5
MIN_VELOCITY=-5

white = 255,255,255

class Boid(object):
  
  #pozycja i predkosc sa listami dwuelementowymi0
  def __init__(self,position,velocity,sight_range=224):
    self.position=position
    self.velocity=velocity
    self.sight_range=sight_range
    
  def __str__(self):
    return str(self.position)+" "+str(self.velocity)
  
  def __repr__(self):
    return str(self.position)+" "+str(self.velocity)
  
  #sprawdzanie, czy dwa boidy leza w swoim zasiegu
  def in_range(self,another_boid):
    if math.sqrt(math.pow(self.position[0]-another_boid.position[0],2) 
    	+ math.pow(self.position[1]-another_boid.position[1],2)) < self.sight_range:
      return True
    return False

  def is_tooClose(self,another_boid):
    if math.sqrt(math.pow(self.position[0]-another_boid.position[0],2) 
    	+ math.pow(self.position[1]-another_boid.position[1],2)) < 17:
      return True
    return False
    
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

  def rule1(self,boid):
    count=0.0
    s=[0.0,0.0]
    for boid2 in self.boids:
      if boid.in_range(boid2):
	       s[0]+=boid2.position[0]
	       s[1]+=boid2.position[1]
	       count+=1.0
    if count == 0.0:
      return [0.0,0.0]
    s[0]/=count
    s[1]/=count
    s[0]-=boid.position[0]
    s[1]-=boid.position[1]
    s[0]/=100
    s[1]/=100
    return s
  
  def rule2(self,boid):
    c = [0,0]
    for another_boid in self.boids:
      if another_boid != boid:
        if boid.is_tooClose(another_boid):
          c[0] = c[0] - ( another_boid.position[0]-boid.position[0]) 
          c[1] = c[1] - ( another_boid.position[1]-boid.position[1])
    return c 

  def rule3(self,boid):
    count=0.0
    s=[0.0,0.0]
    for boid2 in self.boids:
      if boid.in_range(boid2):
	       s[0]+=boid2.velocity[0]
	       s[1]+=boid2.velocity[1]
	       count+=1.0
    if count == 0.0:
      return [0.0,0.0]
    s[0]/=count
    s[1]/=count
    s[0]/=8
    s[1]/=8
    return s

  def move_all_boids_to_new_positions(self):
    for boid in self.boids:
      
      #kazda z funkcji zwraca tuple ze skladowymi x i y predkosci
      rule1_velocity=self.rule1(boid)
      rule2_velocity= self.rule2(boid)
      rule3_velocity=self.rule3(boid)
      print rule1_velocity
      print rule2_velocity
      print rule3_velocity  
      print " "    

      newVelocityX = boid.velocity[0]+rule1_velocity[0]+rule2_velocity[0]+rule3_velocity[0]
      if abs(newVelocityX) > MAX_VELOCITY:
        newVelocityX= math.copysign(MAX_VELOCITY,newVelocityX) 
      newX = abs((boid.position[0]+newVelocityX)%MAX_POSITION_X)
      boid.position[0] = newX
      boid.velocity[0] = newVelocityX

      newVelocityY = boid.velocity[1]+rule1_velocity[1]+rule2_velocity[1]+rule3_velocity[1]
      if abs(newVelocityY) > MAX_VELOCITY:
        newVelocityY= math.copysign(MAX_VELOCITY,newVelocityY) 
      newY = boid.position[1] + newVelocityY 
      newY = abs((boid.position[1]+newVelocityY)%MAX_POSITION_Y)
      boid.position[1] = newY 
      boid.velocity[1] = newVelocityY
     
      print boid.velocity


  
  def draw_boids(self):
    self.display.clean_screen()
    for i in self.boids:
      self.display.draw_object(i,"./img/boid-red.png")

#Klasa reprezentujaca okno, w ktorym wyswietlamy boidy
class Display():
  
  def __init__(self):
    self.screen=pygame.display.set_mode((MAX_POSITION_X-MIN_POSITION_X,MAX_POSITION_Y-MIN_POSITION_Y),DOUBLEBUF)
    #flyweight pattern
    self.image_dictionary={}
    
  def draw_object(self,obj,object_image):
    if not object_image in self.image_dictionary:
      self.image_dictionary[object_image]=pygame.image.load(object_image)
    if (obj.velocity[0]!=0.0 and obj.velocity[1]!=0.0):
      rotated=pygame.transform.rotate(self.image_dictionary[object_image],-90-(180/math.pi)*math.atan2(obj.velocity[1],obj.velocity[0]))
      # print str((180/math.pi)*math.atan2(obj.velocity[1],obj.velocity[0]))+" "+str(obj.velocity[1])+" "+str(obj.velocity[0])
    self.screen.blit(rotated,(obj.position[0],obj.position[1]))
    pygame.display.flip()

  def clean_screen(self):
    self.screen.fill(white)
    

#glowna petla: tu sie bedzie wszystko wykonywalo
def loop(world):
  while True:
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
	pygame.quit()
    world.move_all_boids_to_new_positions()
    world.draw_boids()
    time.sleep(0.1)
  
world=World(50,Display())
# print world

loop(world)