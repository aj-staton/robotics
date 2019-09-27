####################################################################
# This the main program that will be running and Interacting
# with the robot
#
# Typed by: Robert Carff, Austin Statin, Miles Ziemer 
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
CLEAN = 0
SPOT = 1
DOCK = 2
MINUTE = 3
HOUR = 4
DAY = 5
SCHEDULE = 6
CLOCK = 7

####################################################################
# Imports
from RobotInterface import *
from time import sleep
import math
####################################################################

###############################################################
#  Drive() Calculates the Side lengths based off the
# 		   total perimeter of 2000mm, and the drives for the 
#		   correct amount of time asuming 150 mm/s veloctiy.
#		   
###############################################################	
def driveSide(roomba, n):
	sideLength = float(_length_)/n
	driveTime = float(sideLength)/_velocity_
	# TODO: Do the math to convert velocity (mm/s) to (mm)
	roomba.drive(_velocity_, 0)
	time.sleep(driveTime)
	roomba.drive(0, 0)

###############################################################
#  Rotate() Uses the driveDirect function, but only rotates
# 		    one wheel, allowing us to turn
#		   
#		   
###############################################################	
def rotate(roomba, n)
	AngleRadians = math.pi - float(2*math.pi)/n
	rotateTime = float(AngleRadians)/_omega_
	roomba.drive(150, 1)
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
		rotate(roomba, n)


###############################################################
#  Main() Sets the robot into safe and passive mode, and then
# 		   runs our draw regularPolygon() method
#		   
#		   
###############################################################	
def main():
    roomba = RobotInterface()
    roomba.setState("SAFE")
    #roomba.setState("PASSIVE") #I dont think we have passive declared yet
    #Just drive here, and see if we can get the drive function working
    x = True
    while (x):
	if(readButton(CLEAN)):
		x = False
    regularPolygon(roomba, _n_)

main()
