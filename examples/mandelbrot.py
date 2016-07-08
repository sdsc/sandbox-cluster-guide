import math
import time
import Image
from mpi4py import MPI

#Gets row and column (starting at 0,0 for top left) for window, based on rank, assuming rank is ordered by left to right, top to bottom.
def get_rowcolumn(rank, rows, columns):
	count = 0
	for x in xrange(columns):
		for y in xrange(rows):
			if rank == count:
				return x,y
			else:
				count += 1	

#Gets all points in window from column, row coordinates
def get_points(column, columns, row, rows, width, height):
	startx = (width/columns)*column
	finishx = (width/columns)*(column+1)
	starty = (height/rows)*row
	finishy = (height/rows)*(row+1)
	return startx, starty, finishx, finishy

#Detects if in Mandelbrot Set. Change limit higher for more accuracy
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
			on = limit + 1
		on += 1
	if on == limit:
		return True


#Goes through all points from given square(in form of x, y, coordinates)
def go_through_points(startx, starty, finishx, finishy, width, height):	
	list = []	
	for x in range(startx, finishx):
		for y in range(starty, finishy):
			if in_set(x,y,width,height):
				list.append((x,y))
	return list


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

rows = 2
columns = 2
width = 500    #total width of all screens
height = 500   #total height of all screens

#Checks if there are enough windows/screens/processors for given rows and columns(squares)
if comm.Get_size() != rows*columns:
	print("ERROR:| incorrect settings | programs:%s | squares:%s |\r\nHint: programs should = squares, squares = rows*columns"%(comm.Get_size(), rows*columns))
	exit()

#Main stud
row , column = get_rowcolumn(rank, rows, columns)
startx, starty, finishx, finishy = get_points(column, columns, row, rows, width, height)
list_of_points = go_through_points(startx, starty, finishx, finishy, width, height)

#create image
im = Image.new('RGB', (width/columns, height/rows))
for point in list_of_points:
	y = point[1]-starty
	x = point[0]-startx
	try:
		im.putpixel((x,y), (0, 255, 100))
	except IndexError:
		im.putpixel((0,0), (255,255,255))
		print("ERROR:| IndexError | rank: %s | point: %s |"%(rank, str(point)))
im.show()
#im.save(str(rank)+"image.png")
time.sleep(5)	


		


