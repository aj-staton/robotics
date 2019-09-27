####################################################################
# This the main program that will be running and Interacting
# with the robot
#
# Typed by: Robert Carff, Austin Statin, Miles Ziemer 
#			-- September 15th, 2019
#
####################################################################
# Magic number Variables
degrees = 360 #this is in degrees
Length = 2000 #this is in milimeters
n = 5 #this is number of sides for the polygon
sleepTime = 0.0125 #this time is in seconds (12.5 miliseconds)

# TODO: Do we need these turning radii still?
# high = 00000000 # calculated for 150 mm/s
# low = 10110110 # calculated for 150 mm/s

velocity = 150 # in mm/s 
#Omega = 2*velocity/235
Omega = 1.2766
####################################################################
# Button Opcode 165
# Bit Number:  7	6	5	4	3	2	1	0
# Bit Number Value: CLOCK SCHEDULE DAY HOUR MINUTE DOCK SPOT CLEAN
####################################################################
CLEAN = chr(0)
SPOT = chr(1)
DOCK = chr(2)
MINUTE = chr(3)
HOUR = chr(4)
DAY = chr(5)
SCHEDULE = chr(6)
CLOCK = chr(7)
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
def driveSide(roomba):
	sideLength = float(Length)/n
	driveTime = float(sideLength)/velocity
	# TODO: Do the math to convert velocity (mm/s) to (mm)
	roomba.Drive(velocity, 0)
	time.sleep(driveTime)
	roomba.Drive(0, 0)

###############################################################
#  Rotate() Uses the driveDirect function, but only rotates
# 		    one wheel, allowing us to turn
#		   
#		   
###############################################################	
def rotate(roomba):
	'''
	Angle = degrees - degrees/n
	rotateTime = Angle/velocity
        # TODO: do the math to make turning radius (in mm) to deg. 
        # roomba.Drive(velocity, radius) #passing in high b/c its 0s
        time.sleep(rotateTime) # we can adjust this/figure our rotate time
	roomba.Drive(0,0)
	'''
	AngleRadians = math.pi - float(2*math.pi)/n
	rotateTime = float(AngleRadians)/Omega
	roomba.Drive(150, 1)
	time.sleep(rotateTime)
	roomba.Drive(0, 0)


###############################################################
#  regularPolygon() Once the robot is powered on, this method
#  waits for the clean button to be pressed.
#  Once pressed - it drives the length of a 
#  side and turns. Repeats this N times.
#		   
###############################################################	
def regularPolygon(roomba, n):
	for i in range (n):
                driveSide(roomba)
                rotate(roomba)


###############################################################
#  Main() Sets the robot into safe and passive mode, and then
# 		   runs our draw regularPolygon() method
#		   
#		   
###############################################################	
def main():
    roomba = RobotInterface()
    roomba.SetState("SAFE")
    #roomba.setState("PASSIVE") #I dont think we have passive declared yet
    #Just drive here, and see if we can get the drive function working
    regularPolygon(roomba, 6)


main()
