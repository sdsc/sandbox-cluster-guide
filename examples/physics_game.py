import pygame
import physicsParticles
import math
import os
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

pygame.display.init()
pygame.display.set_caption('TEST')
(width,height) = (200,200)
screen = pygame.display.set_mode((400, 400))
screen2 = pygame.display.set_mode((400, 400))

env = physicsParticles.Environment((width,height))
env.addFunctions(['move','accelerate', 'drag'])
env.acceleration = (math.pi, 0.002)
env.addParticles(2)

running = True
selected_particle = None
rect1 = pygame.Rect(0,0,200,400)
rect2 = pygame.Rect(200,0,200,400)
canvas = pygame.Surface((400,400))
while running:
#  if comm.rank == 0:
#    screen.fill(env.colour)
#    screen.blit(canvas,(0,0),rect1)
#  if comm.rank == 1:
#    screen2.fill(env.colour)
#    screen2.blit(canvas,(400,0),rect2)
  screen.fill(env.colour)
  sub1 = canvas.subsurface(rect1)
  sub2 = canvas.subsurface(rect2)
  screen.blit(sub1,(0,0))
  screen.blit(sub2,(0,0))

  pygame.draw.line(canvas,(255,255,255),(0,0),(0,200),1)

  for p in env.particles:
    pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)),p.size, p.thickness)
  env.update()
  #if comm.rank == 0:
    #screen.blit(sub1,(0,0))
  #  sub = canvas.subsurface(rect1)
  #if comm.rank == 1:
    #screen2.blit(sub2,(0,0))
  #  sub = canvas.subsurface(rect2)
  
  pygame.display.flip()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      selected_particle = env.findParticle(pygame.mouse.get_pos())
    elif event.type == pygame.MOUSEBUTTONUP:
      selected_particle = None
  if selected_particle:
    selected_particle.mouseMove(pygame.mouse.get_pos())
    
