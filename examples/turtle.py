from turtle import *

setup(500, 500)
Screen()
title("Turtle Keys")
move = Turtle()
#showturtle()

#Functions for the keyboard input
def k1():
    move.forward(45)

def k2():
    move.left(45)

def k3():
    move.right(45)

def k4():
    move.back(45)

#Calls the functions when it detects a certain keyboard input
onkey(k1, "Up")
onkey(k2, "Left")
onkey(k3, "Right")
onkey(k4, "Down")

#Program listens for the keyboard inputs
listen()
#Mainloop prevents the program from closing the window itself
mainloop()
