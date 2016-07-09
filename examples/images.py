#!/usr/bin/env python

"""
Loads an image and each task displays a quarter.

Run this using
$ mpirun -np 4 python ./images.py <image file>
"""

import os
import sys
import pygame
import time
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# check that image file name was provided
if len(sys.argv) == 1:
    if rank == 0:
        print
        print "Need to provide image file name. E.g.,"
        print "mpirun -np 4 python ./images.py foo.png"
        print
        sys.exit(-1)
    else:
        sys.exit(-1)
elif size != 4:
    # Currently only works with 4 tasks
    if rank == 0:
        print
        print "Only works with 4 tasks. E.g.,"
        print "mpirun -np 4 python ./images.py foo.png"
        print
        sys.exit(-1)
    else:
        sys.exit(-1)
    
# read the image on every task
img = pygame.image.load(sys.argv[1])

# obtain the width and height of the selected file
w = img.get_rect().width
h = img.get_rect().height

# stores the values of half the width and height
# used for window size and position
halfWidth = w/2
halfHeight = h/2
size=(halfWidth, halfHeight)

os.environ['DISPLAY'] = ':0.0'
# set window position based on rank
# Rect selects image segment origin and size
if comm.rank == 0:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
    rect = pygame.Rect(0,0,halfWidth,halfHeight)
elif comm.rank == 1:
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(halfWidth+120) + ",100"
    rect = pygame.Rect(halfWidth, 0, halfWidth, halfHeight)
elif comm.rank == 2:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "100," + str(halfHeight+120)
    rect = pygame.Rect(0, halfHeight, halfWidth, halfHeight)
else:
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(halfWidth+120) + "," + str(halfHeight+120)
    rect = pygame.Rect(halfWidth, halfHeight, halfWidth, halfHeight)
   
# creates a screen that is only a fourth of the full image size
pygame.display.init()
screen = pygame.display.set_mode((size), pygame.NOFRAME)

# fill the screen with white background
white = (255,255,255)
screen.fill((white))

# displays one quarter of the image for 5 seconds and then exit
screen.blit(img, (0,0),rect)
pygame.display.update()
time.sleep(5)

sys.exit(0)
