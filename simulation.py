import simpy
import random

MAX_POSITION=100
MIN_POSITION=100

MAX_VELOCITY=5
MIN_VELOCITY=5

class Boid(object):
  
  #pozycja i predkosc sa wektorami (tuplami) dwuelementowymi
  def __init__(self,position,velocity):
    self.position=position
    self.velocity=velocity
    
class Herd(object):
  
  #display - zmienna do wyswietlania 
  def __init__(self,number_of_boids,display):
    self.number_of_boids=number_of_boids
    self.boids=[]
    for i in range(number_of_boids):
      boids+=boid((random.rand(
      
env=simpy.Environment()
