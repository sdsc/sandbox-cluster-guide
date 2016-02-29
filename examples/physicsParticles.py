#!/usr/bin/env python
import pygame
import random
import math

def addVectors((angle1,length1),(angle2,length2)):
  x = math.sin(angle1) * length1 + math.sin(angle2) * length2
  y = math.cos(angle1) * length1 + math.sin(angle2) * length2 
  length = math.hypot(x,y)   
  angle = 0.5 * math.pi - math.atan2(y,x)
  return (angle, length)


def collide(p1, p2):
  dx = p1.x - p2.x
  dy = p1.y - p2.y

  tangent = math.atan2(dy, dx)
  distance = math.hypot(dx, dy)
  angle = 0.5 * math.pi + tangent

  if distance < p1.size + p2.size:
    print 'BANG!'
    angle = math.atan2(dy, dx) + 0.5 * math.pi
    total_mass = p1.mass + p2.mass

    (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
    (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi,2*p1.speed*p1.mass/total_mass))
    #p1.angle = 2*tangent - p1.angle
    #p2.angle = 2*tangent - p2.angle
    #(p1.speed, p2.speed) = (p2.speed, p1.speed)
    elasticity = p1.elasticity * p2.elasticity
    p1.speed *= elasticity
    p2.speed *= elasticity

    overlap = 0.5*(p1.size + p2.size - distance+1)
    p1.x += math.sin(angle)*overlap
    p1.y -= math.cos(angle)*overlap

    p2.x -= math.sin(angle)*overlap
    p2.y += math.cos(angle)*overlap


class Environment:
  def __init__(self, (width, height)):
    self.width = width*2
    self.height = height*2
    self.particles = []
  
    self.colour = (255,255,255)
    self.mass_of_air = 0.2
    self.elasticity = 0.75
    self.acceleration = None
    self.particle_functions1 = []
    self.particle_functions2 = []
    self.function_dict =  {
    'move': (1,lambda p: p.move()),
    'drag': (1,lambda p: p.experienceDrag()),
    'bounce': (1,lambda p: self.bounce(p)),
    'accelerate': (1,lambda p: p.accelerate(self.acceleration)),
    'collide': (2, lambda p1, p2: collide(p1,p2))}

  def addParticles(self, n=1, **kargs):
    for i in range(n):
      size = kargs.get('size',random.randint(10,20))
      mass = kargs.get('mass',random.randint(100,10000))
      x = kargs.get('x', random.uniform(size, self.width-size))
      y = kargs.get('y', random.uniform(size, self.height-size))
      p = Particle((x,y), size, mass)
      p.speed = kargs.get('speed', random.random())
      p.angle = kargs.get('angle', random.uniform(0,math.pi*2))
      p.colour = kargs.get('colour', (0,0,255))
      p.drag = (p.mass/(p.mass + self.mass_of_air)) ** p.size
   
      self.particles.append(p)

  def update(self):
    #for particle in self.particles:
    #  particle.move()
    #  if self.mass_of_air != 0:
    #    for particle in self.particles:
    #      particle.experienceDrag()
    #  if self.acceleration:
    #    for particle in self.particles:
    #      particle.accelerate(self.acceleration)
    #  if self.hasBoundaries:
    #    for particle in self.particles:
    #      self.bounce(particle)
    for i, particle in enumerate(self.particles):
        #for f in self.particle_functions1:
        #  f(particle)
        #for particle2 in self.particles[i+1:]:
        #  for f in self.particle_functions2:
        #    f(particle, particle2)
        particle.move()
        if self.acceleration:
          particle.accelerate(self.acceleration)
        self.bounce(particle)
        for particle2 in self.particles[i+1:]:
          collide(particle, particle2)

  def bounce(self, particle):
    if particle.x > self.width - particle.size:
      particle.x = 2*(self.width - particle.size) - particle.x
      particle.angle = - particle.angle
      particle.speed *= self.elasticity
    elif particle.x < particle.size:
      particle.x = 2*particle.size - particle.x
      particle.angle = - particle.angle
      particle.speed *= self.elasticity
    if particle.y > self.height - particle.size:
      particle.y = 2*(self.height - particle.size) - particle.y
      particle.angle = math.pi - particle.angle
      particle.speed *= self.elasticity
    elif particle.y < particle.size:
      particle.y = 2*particle.size - particle.y
      particle.angle = math.pi - particle.angle  
      particle.speed *= self.elasticity

  def findParticle(self, (x, y)):
    for p in self.particles:
      if math.hypot(p.x-x,p.y-y) <= p.size:
        return p
    return None

  def addFunctions(self, function_list):
    for f in function_list:
      #if f in self.function_dict:
      #  self.particle_functions.append(self.function_dict[f])
      (n,f) = self.function_dict.get(f, (-1,None))
      if n == 1:
        self.particle_functions1.append(f)
      elif n == 2:
        self.particle_functions2.append(f)
      else:
        print "No such function: %s" % f


class Particle:
  def __init__(self,(x,y),size, mass=1):
    self.x = x
    self.y = y
    self.size = size
    self.mass = mass
    self.mass_of_air = 0.2
    self.speed = 0.09
    self.angle = math.pi/2
    self.colour = (0,0,255)
    self.thickness = 1
    self.drag = (self.mass/(self.mass + self.mass_of_air))
    self.elasticity = 0.9

  def display(self):
    pygame.draw.circle(screen, self.colour, (int(self.x),int(self.y)), self.size, self.thickness)

  def move(self):
    self.x += math.sin(self.angle) * self.speed
    self.y -= math.cos(self.angle) * self.speed
    #(self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
    self.speed *= self.drag

  def mouseMove(self,(x,y)):
    dx = x - self.x
    dy = y - self.y
    self.angle = 0.5*math.pi + math.atan2(dy,dx)
    self.speed = math.hypot(dx,dy) * 0.1

  def accelerate(self, vector):
    (self.angle, self.speed) = addVectors((self.angle, self.speed), vector)

  def experienceDrag(self):
    self.speed *= self.drag
  

#(width,height) = (400,400)
#background_colour = (255,255,255)
#gravity = (math.pi, 0.002)
#drag = 0.999
#elasticity = 0.75
#mass_of_air = 0.2

#screen = pygame.display.set_mode((width,height))
#pygame.display.set_caption('Physics Game')
#screen.fill(background_colour)

#number_of_particles = 3
#my_particles = []

#for n in range(number_of_particles):
#  size = random.randint(10,20)
#  density = random.randint(1,20)
#  x = random.randint(size, width - size)
#  y = random.randint(size, height - size)
 
#  particle = Particle((x,y), size, density*size**2)
#  particle.speed = random.random()
#  particle.angle = random.uniform(0,math.pi*2) 

#  my_particles.append(particle)
  #first_particle = Particle((x,y),size)
#first_particle.display()

#running = True
#selected_particle = None
#while running:
#  for i, particle in enumerate(my_particles):
#    if particle != selected_particle:
#      particle.move()
#      particle.bounce()
#    for particle2 in my_particles[i+1:]:
#      collide(particle, particle2)
#    particle.colour = (200-density*10, 200-density*10,255)
#    particle.display()
#  pygame.display.flip()
#  for event in pygame.event.get():
#    if event.type == pygame.QUIT:
#      running = False
#    if event.type == pygame.MOUSEBUTTONDOWN:
#      (mouseX, mouseY) = pygame.mouse.get_pos()
#      selected_particle = findParticle(my_particles, mouseX, mouseY)
#      if selected_particle:
#        (mouseX, mouseY)  = pygame.mouse.get_pos()
#        dx = mouseX - selected_particle.x
#        dy = mouseY - selected_particle.y
#        selected_particle.angle = math.atan2(dy,dx) + 0.5*math.pi
#        selected_particle.speed = math.hypot(dx,dy) * 0.1
#        selected_particle.colour = (255,0,0)
#    elif event.type == pygame.MOUSEBUTTONUP:
#      selected_particle = None


