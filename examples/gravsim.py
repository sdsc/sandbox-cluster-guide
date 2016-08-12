#! /usr/bin/env python

#Run program using mpirun -np [tasks] gravsim.py [rows] [columns]
#    eg. mpirun 4 gravsim.py 2 2
#
#Controls:
#    left-click
import os
import time
import pygame
from pygame.locals import *
import math
from mpi4py import MPI
import sys

os.environ['DISPLAY'] = ':0.0'
####################   Pygame and MPI Setup ###################
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
rows = int(sys.argv[1])
columns = int(sys.argv[2])
pygame.display.init()
disp_info = pygame.display.Info()
width = disp_info.current_w*columns  #total width of all screens
height = disp_info.current_h*rows   #total height of all screens
pygame.init()
screen = pygame.display.set_mode((width/columns, height/rows), pygame.NOFRAME)
pygame.display.set_caption('GravitySim%s'%(comm.Get_rank()))
pygame.mouse.set_visible(False)


################  Functions to get windows true range  ##################
def get_rowcolumn(rank, rows, columns):
	count = 0
	for x in xrange(columns):
		for y in xrange(rows):
			if rank == count:
				return y, x
			else:
				count += 1	
def get_points(column, columns, row, rows, width, height):
	startx = (width/columns)*column
	finishx = (width/columns)*(column+1)
	starty = (height/rows)*row
	finishy = (height/rows)*(row+1)
	return startx, starty, finishx, finishy
############
row , column = get_rowcolumn(rank, rows, columns)
startx, starty, finishx, finishy = get_points(column, columns, row, rows, width, height)
print startx, starty, rank

#####################   dictates movement and size of balls   #####################
class bal():
	def __init__(self, x, y, mass, velocity, is_mobile):
		self.mass = mass
		self.x = x
		self.y = y
		self.velocity = velocity
		self.velocity1 = velocity
		self.last_time = time.time()
		self.in_box = True
		self.is_mobile = is_mobile
	def change_velocity(self, ball2):
		if self.is_mobile:
			self.velocity1 = self.velocity
			difx = ball2.x-self.x
			dify = ball2.y-self.y
			distance = math.sqrt(difx**2+dify**2)
			if distance == 0:
				distance = 1
			force = (2)*(self.mass*ball2.mass)/(distance**2)
			try:
				mdifx = math.fabs(difx)
				mdify = math.fabs(dify)
				direction = [(mdifx)/max(mdifx, mdify)*(mdifx/difx), (mdify)/max(mdifx,mdify)*(mdify/dify)]
			except:
				direction = 0,0
				
			self.velocity1[0] += direction[0]*(force/self.mass)
			self.velocity1[1] += direction[1]*(force/self.mass)
	def get_pos(self):
		self.velocity = self.velocity1
		current_time = time.time()
		self.x += self.velocity[0]*(current_time-self.last_time)
		self.y += self.velocity[1]*(current_time-self.last_time)
		self.last_time = current_time
		return int(self.x), int(self.y)

#Blit's mouse across entire program
def manage_mouse(s, mx, my):
	if mx == None:
		x,y = pygame.mouse.get_pos()
		pygame.draw.circle(screen, (255,255,255), (x*columns,y*rows), int(math.sqrt(s/3)))
		return x*columns, y*rows
	else:
		pygame.draw.circle(screen, (255,255,255), (mx-(column*(width/columns)),my-(row*(height/rows))), int(math.sqrt(s/3)))

#Decides whether ball is in_range (within screen). Set second = True to decide whether it should be seen
def in_range(ball, startx, starty, finishx, finishy, second):
	if ball.x > startx and ball.x < finishx and ball.y > starty and ball.y < finishy:
		return True
	if (ball.x+int(math.sqrt(ball.mass/3)) > startx or ball.x-int(math.sqrt(ball.mass/3)) < finishx) and (ball.y+int(math.sqrt(ball.mass/3)) > starty or ball.y-int(math.sqrt(ball.mass/3)) < finishy) and second:
		return True
#Decides whether ball can be seen by any screens
def in_entire(ball, width, height):
	if int(ball.x)  in range(0,width) and int(ball.y) in range(0,height):
		return False
	else:
		return True
#######################################################
if rank < comm.Get_size()/2:
		os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'#str(startx) + "," + str(starty)
else:
		os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'#str(startx - disp_info.current_w) + "," + str(starty)

#################   Main Loop   #######################3
list_of_balls = []
size_of_input = 100
x = 0
y = 0
while True:
	screen.fill((0,0,0))
	if rank == 0:
		x, y = manage_mouse(size_of_input, None, None)
		#print mousex, mousey
	else:
		manage_mouse(size_of_input, x, y)
	#if rank == 0:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 4:
				size_of_input *= 2
			elif event.button == 5:
				if size_of_input >= 30:
					size_of_input /= 2
			elif event.button == 1 or  event.button == 3:
				x2, y2 = x, y
		if event.type == MOUSEBUTTONUP:
			if event.button == 1:
				x3, y3 = x, y
				list_of_balls.append(bal(x3+(column*(width/columns)), y3+(row*(height/rows)), size_of_input, [(x3-x2),(y3-y2)], True))
			if event.button == 3:
				x3, y3 = x, y
				list_of_balls.append(bal(x3+(column*(width/columns)), y3+(row*(height/rows)), size_of_input, [(x3-x2),(y3-y2)], False))
	######   MPI Communications   ######################
	if rank == 0:
		list_of_all = []
		list_of_all += list_of_balls
		for p in range(size-1):
			list_of_all += comm.recv(source=p+1,tag=11)
		comm.bcast(list_of_all, 0)
		comm.bcast((x, y, size_of_input), 0)
	else:
		comm.send(list_of_balls, dest=0, tag=11)
		list_of_all = comm.bcast(None, 0)
		x, y, size_of_input = comm.bcast(None, 0)
	##########  In Box Calculations  #######################
	list_of_balls = []
	for ball in list_of_all:
		if in_range(ball, startx, starty, finishx, finishy, False):
			ball.in_box = True			
			list_of_balls.append(ball)		
			for ball2 in list_of_all:
				if ball != ball2:
					ball.change_velocity(ball2)
					if ball.mass <= 0:
						list_of_all.remove(ball)
						list_of_balls.remove(ball)
			if in_range(ball, startx, starty, finishx, finishy, False):
				coord = ball.get_pos()
				pygame.draw.circle(screen, (255,255,255), (coord[0]-(column*(width/columns)),coord[1]-(row*(height/rows))), int(math.sqrt(ball.mass/3)), int(math.sqrt(ball.mass/3))/2)
		elif in_range(ball, startx, starty, finishx, finishy, True):
			coord = ball.get_pos()
			pygame.draw.circle(screen, (255,255,255), (coord[0]-(column*(width/columns)),coord[1]-(row*(height/rows))), int(math.sqrt(ball.mass/3)), int(math.sqrt(ball.mass/3))/2)
	########################################################
	comm.Barrier()
	pygame.display.update()
