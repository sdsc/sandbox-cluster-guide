#! /usr/bin/env python 

"""
Run this using
  mpirun -np <tasks> ./mandelbrot.py <rows> <columns>
where rows*columns <= tasks
"""

import os
import sys
import math
import time
from PIL import Image
from mpi4py import MPI
import pygame

#Gets row and column (starting at 0,0 for top left) for window, based on rank, assuming rank is ordered by left to right, top to bottom.
def get_rowcolumn(rank, rows, columns):
	count = 0
	for x in xrange(columns):
		for y in xrange(rows):
			if rank == count:
				return y, x
			else:
				count += 1	
#Gets all points in window from column, row coordinates
def get_points(column, columns, row, rows, width, height):
	startx = (width/columns)*column
	finishx = (width/columns)*(column+1)
	starty = (height/rows)*row
	finishy = (height/rows)*(row+1)
	return startx, starty, finishx, finishy

#Detects if in Mandelbrot Set. Change Limit higher for more accuracy
def in_set(x, y, width, height):
	x = (x-.5*width)/(.25*width)
	y = (y-.5*height)/(.25*width)
	c = complex(x,y)
	z = 0
	on = 0
	limit = 100
	while on < limit:
		z = z*z +c
		if math.fabs(z.real) > 2:
			on += limit
		on += 1
	if on == limit:
		return True, 255
	else:
		return True, int((on - limit)/(limit*1.0)*255)


#Goes through all points from given square(in form of x, y, coordinates)
def go_through_points(startx, starty, finishx, finishy, width, height):	
	list = []	
	for x in range(startx, finishx):
		for y in range(starty, finishy):
			prop = in_set(x,y,width,height)
			if prop[0]:
				list.append((x,y,prop[1]))
	return list

start_time = time.time()

os.environ['DISPLAY'] = ':0.0'

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

rows = int(sys.argv[1])
columns = int(sys.argv[2])

pygame.display.init()
disp_info = pygame.display.Info()
width = disp_info.current_w*columns  #total width of all screens
height = disp_info.current_h*rows   #total height of all screens

#Checks if there are enough windows/screens/processors for given rows and columns(squares)
#if comm.Get_size() != rows*columns:
#	print("ERROR:| incorrect settings | programs:%s | squares:%s |\r\nHint: programs should = squares, squares = rows*columns"%(comm.Get_size(), rows*columns))
#	exit()

#Main stud
rowcol = rows*columns
if rows*columns < comm.Get_size():
	columns, rows = 1*columns , comm.Get_size()/columns
try:
	row , column = get_rowcolumn(rank, rows, columns)
except TypeError:
	print "TypeError \r\nrank: " + str(rank)
	comm.Barrier()
startx, starty, finishx, finishy = get_points(column, columns, row, rows, width, height)

# assume that tasks are ordered by compute node
a, b = get_rowcolumn(rank/(rowcol*comm.Get_size()), int(sys.argv[1]), int(sys.argv[2]))
os.environ['SDL_VIDEO_WINDOW_POS'] = str(startx - disp_info.current_w*column) + "," + str(starty - disp_info.current_h*b)


list_of_points = go_through_points(startx, starty, finishx, finishy, width, height)

#create image
im = Image.new('RGB', (width/columns, height/rows))
for point in list_of_points:
	y = point[1]-starty
	x = point[0]-startx
	try:
		im.putpixel((x,y), (point[2], point[2], point[2]))
	except IndexError:
		im.putpixel((0,0), (255,255,255))
		print("ERROR:| IndexError | rank: %s | point: %s |"%(rank, str(point)))
#im.show()
im.save(str(rank)+"image.png")

comm.Barrier()
if rank == 0:
        end_time = time.time()
        print("Total time using %d tasks was %4.2f seconds" % (comm.Get_size(), end_time - start_time))
#Pygame displays saved image
img = pygame.image.load(str(rank)+"image.png")
size = img.get_rect().width,img.get_rect().height
sscr = pygame.display.set_mode((size), pygame.NOFRAME)
rect0 = pygame.Rect(startx, starty, width, height)
# add border around each task's window
pygame.draw.rect(sscr, (255,255,255), (startx, starty, width, height), 10)
sscr.blit(img, (0,0))
pygame.display.update()
time.sleep(10)
