#!/usr/bin/env python

"""
Calculate pi using the Simpson's rule.

$ mpirun -np 32 ./cpi.py
"""

from mpi4py import MPI
import os
import time
import numpy
import pygame

# get number of tasks and my rank
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

w = int(800./size)
h = 800
window_size = (w, h)
os.environ['DISPLAY'] = ':0.0'
os.environ['SDL_VIDEO_WINDOW_POS'] = str(rank*(w+10)+40) + ",40"
pygame.display.init()
screen = pygame.display.set_mode((window_size), pygame.NOFRAME)

# fill the screen with white background
white = (255,255,255)
screen.fill((white))
pygame.display.update()

# 100 elements per task
# each task does its own section
N = 100
dx = 1.0/(N*float(size))
s = 0.0
start = rank*1.0/size
for i in range(0, N):
    x = start + dx * (i + 0.5)
    s += 4.0 / (1.0 + x**2)
    pygame.draw.rect(screen, (0,0,255), (i*8./size, h-h/(1.0 + x**2), 8./size+1, h/(1.0 + x**2)))
    pygame.display.update()
    time.sleep(0.1)

piseg = numpy.array(s * dx, dtype='d')
# sum up the results across tasks
pi = numpy.array(0.0, 'd')
comm.Reduce([piseg, MPI.DOUBLE], [pi, MPI.DOUBLE],
            op=MPI.SUM, root=0)

if rank == 0:
    print "pi = %0.16f, error is %0.16e" % (pi, numpy.fabs(pi - numpy.pi))
time.sleep(5)
