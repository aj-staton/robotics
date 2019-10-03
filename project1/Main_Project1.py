####################################################################
# This the main program that will be running and interacting
# with the robot in Project 1. 
#
# Written by: Robert Carff, Austin Statin, Miles Ziemer 
#			-- September 15th, 2019
#
####################################################################
# Magic number Variables
_n_ = 5 #this is number of sides for the polygon

_degrees_ = 360 #this is in degrees
_length_ = 2000 #this is in milimeters
_sleepTime_ = 0.0125 #this time is in seconds (12.5 miliseconds)
_velocity_ = 150 # in mm/s 
_omega_ = 1.2766 # 2*_velocity_/235

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
####################################################################

###############################################################
# driveSide() calculates the Side lengths based off the
# total perimeter of 2000mm, and the drives for the 
# correct amount of time asuming 150 mm/s veloctiy.
#		   
###############################################################	
def driveSide(roomba, n):
	sideLength = float(_length_)/n
	driveTime = float(sideLength)/_velocity_
	roomba.drive(_velocity_, 0)
	time.sleep(driveTime)
	roomba.drive(0, 0)

###############################################################
#  rotate() uses the drive() function, but only rotates
#  one wheel, allowing us to turn counter-clockwise.
#		   
###############################################################	
def rotate(roomba, n):
	rotateTime = float(2*math.pi/n)/_omega_
	roomba.drive(_velocity_, 1)
	time.sleep(rotateTime)
	roomba.drive(0, 0)

###############################################################
#  regularPolygon() Once the robot is powered on, this method
#  waits for the clean button to be pressed.
#  Once pressed - it drives the length of a 
#  side and turns. Repeats this N times.
#		   
###############################################################	
def regularPolygon(roomba, n):
	for i in range (n):
		driveSide(roomba, n)
                # We use this conditional to prevent to robot
                # from rotating after the last side.
		if(i == (n - 1)):
		    break
		rotate(roomba, n)


###############################################################
#  main() controls all actions of execution, including calling
#  for the drawing of the N-sided polygon for Project 1.
#		   
###############################################################	
def main():
    roomba = RobotInterface()
    roomba.setState("SAFE")
    x = True
    # Listen for the press of the Clean button, which will begin
    # the drawing of the polygon.
    while (x):
	if(roomba.readButton(_CLEAN_)):
		x = False
    #TODO: need to read button state (even when robot is moving)
    regularPolygon(roomba, _n_)


main()
