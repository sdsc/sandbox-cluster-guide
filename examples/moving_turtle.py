from turtle import *
import pygame
from mpi4py import MPI

img = pygame.image.load('gingerbreadman.jpg')
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
white = (255,255,255)
w = img.get_rect().width
h = img.get_rect().height
size=(w,h)
halfWidth = w/2
halfHeight = h/2
screen = pygame.display.set_mode((halfWidth,halfHeight))
screen.fill((white))
screen.blit(img, (0,0))

pygame.display.update()
#title("Turtle Keys")
pygame.display.get_init

move =Turtle()
#showturtle()
move.goto(100,100)
move.shape('turtle')

def k1():
    move.forward(45)

def k2():
    move.left(45)

def k3():
    move.right(45)

def k4():
    move.back(45)

onkey(k1, "Up")
onkey(k2, "Left")
onkey(k3, "Right")
onkey(k4, "Down")

In = 1
rect0 = pygame.Rect(0,0,halfWidth,halfHeight)
rect1 = pygame.Rect(halfWidth, 0, halfWidth, halfHeight)
rect2 = pygame.Rect(0, halfHeight, halfWidth, halfHeight)
rect3 = pygame.Rect(halfWidth, halfHeight, halfWidth, halfHeight)
while In:
	screen.fill((white))
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

listen()
mainloop()
