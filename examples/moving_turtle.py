import pygame

pygame.init()

display_width = 800
display_height = 800

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("TEST")

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
image = pygame.image.load('turtle.png')

def turtle(x,y):
	gameDisplay.blit(image, (x,y))

x = (display_width * 0.45)
y = (display_height * 0.8)
x_change = 0
y_change = 0
running = 1

while not crashed:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			x_change = -5
		elif event.key == pygame.K_RIGHT:
			x_change = 5
		elif event.key == pygame.K_UP:
			y_change = -5
		elif event.key == pygame.K_DOWN:
			y_change = 5
	if event.type == pygame.KEYUP:
			y_change = 0
			x_change = 0

	x += x_change
	y += y_change
	pygame.display.update()

	gameDisplay.fill(white)
	turtle(x,y)

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
