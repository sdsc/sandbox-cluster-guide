import pygame
import time
from mpi4py import MPI

#Where the image file is stored; need to edit the file name before using
img = pygame.image.load('20140902_200423.jpg')
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

In = 1
pygame.display.init()

white = (255,255,255)
#obtain the width and height of the selected file
w = img.get_rect().width
h = img.get_rect().height
#print w, ",", h
#stores the values of half the width and height
halfWidth = w/2
halfHeight = h/2
#print halfWidth, ",", halfHeight

size=(halfWidth, halfHeight)
#creates a screen that is only a fourth of the image size
screen = pygame.display.set_mode((size))
screen.fill((white))
#segments the image into fourths
rect0 = pygame.Rect(0,0,halfWidth,halfHeight)
rect1 = pygame.Rect(halfWidth, 0, halfWidth, halfHeight)
rect2 = pygame.Rect(0, halfHeight, halfWidth, halfHeight)
rect3 = pygame.Rect(halfWidth, halfHeight, halfWidth, halfHeight)
#screen0.fill((white))
pygame.display.get_init
#pygame.display.update()

while In:
	screen.fill((white))
	#displays each of the fourths in a separate window
	if comm.rank == 0:
		screen.blit(img, (0,0),rect0)
		pygame.display.update()
	elif comm.rank == 1:
		screen.blit(img, (0,0), rect1)
		pygame.display.update()
	elif comm.rank == 2:
		screen.blit(img, (0,0), rect2)
		pygame.display.update()
	else:
		screen.blit(img, (0,0), rect3)
		pygame.display.update()
