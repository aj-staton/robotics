####################################################################
# This the main program that will be running and interacting
# with the robot in Project 1. 
#
# Written by: Robert Carff, Austin Statin, Miles Ziemer 
#			-- September 15th, 2019
#
####################################################################
# Magic number Variables
N = 5 #this is number of sides for the polygon

_degrees_ = 360 #this is in degrees
_length_ = 2000 #this is in milimeters
_sleepTime_ = 0.0125 #this time is in seconds (12.5 miliseconds)
_velocity_ = 150 # in mm/s 
_omega_ = 1.2766 # 2*_velocity_/235
ROTATE = 1
NOROTATE = 0
_sidelength_ = float(_length_)/N
_driveTime_ = float(_sideLength_)/_velocity_
_rotateTime_ = float(2*math.pi/N)/_omega_


roomba = RobotInterface()
####################################################################
# Button Opcode 165
# Bit Number:  7	6	5	4	3	2	1	0
# Bit Number Value: CLOCK SCHEDULE DAY HOUR MINUTE DOCK SPOT CLEAN
####################################################################
_CLEAN_ = 0
_SPOT_ = 1
_DOCK_ = 2
_MINUTE_ = 3
_HOUR_ = 4
_DAY_ = 5
_SCHEDULE_ = 6
_CLOCK_ = 7

####################################################################
# Imports
from RobotInterface import *
from time import sleep
import math
from threading import Thread
####################################################################

###############################################################
# driveSide() calculates the Side lengths based off the
# total perimeter of 2000mm, and the drives for the 
# correct amount of time asuming 150 mm/s veloctiy.
#		   
###############################################################	
def stopRoomba():
	roomba.drive(0,0)

def driveSide():
	roomba.drive(_velocity_, NOROTATE)
	time.sleep(_driveTime_)
	while(not roomba.isDriving):
		time.sleep(.012)
		continue
		stopRoomba()
###############################################################
#  rotate() uses the drive() function, but only rotates
#  one wheel, allowing us to turn counter-clockwise.
#		   
###############################################################	
def rotate():
	roomba.drive(_velocity_, 1)
	time.sleep(rotateTime)
	stopRoomba()
###############################################################
#  regularPolygon() Once the robot is powered on, this method
#  waits for the clean button to be pressed.
#  Once pressed - it drives the length of a 
#  side and turns. Repeats this N times.
#		   
###############################################################	
def regularPolygon():
	for i in range (N):
		driveSide()
		if(i == N-1):
			break
		rotate()

###############################################################
#  this methods checks the buttons for us 
#		   
###############################################################	

def controlThread():
	while(True):
		time.sleep(.10)
		if(roomba.readButton(_CLEAN_)):
			roomba.isDriving = not roomba.isDriving

###############################################################
#  main() controls all actions of execution, including calling
#  for the drawing of the N-sided polygon for Project 1.
###############################################################	
def main():
    roomba.setState("SAFE")
    x = True
    # Listen for the press of the Clean button, which will begin
    # the drawing of the polygon.
    while (x):
        if(roomba.readButton(_CLEAN_)):
            x = False
    button = Thread(target = controlThread)
    button.start();
    #this should check the global flag that is changed within our thread
    regularPolygon(roomba,_n_)
main()
