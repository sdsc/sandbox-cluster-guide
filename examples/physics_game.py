import pygame
import physicsParticles
import math

pygame.display.set_caption('TEST')
(width,height) = (400,400)
screen = pygame.display.set_mode((width, height))

env = physicsParticles.Environment((width,height))
env.addFunctions(['move','accelerate', 'drag'])
env.acceleration = (math.pi, 0.002)
env.addParticles(5)

running = True
selected_particle = None
while running:
  screen.fill(env.colour)
  for p in env.particles:
    pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)),p.size, p.thickness)
  env.update()
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
    
