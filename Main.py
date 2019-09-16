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
driveSpeed = 150 #this is the speed in mm/s
n = 5 #this is number of sides for the polygon
sleepTime = 0.0125 #this time is in seconds (12.5 miliseconds)
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
import RobotInterface
####################################################################
class main:
	#drive direct at 150 mm/s speed 
	def drive(time):
		roomba.driveDirect()
		time.sleep(time)

	#rotating at a specified speed COUNTER CLOCKWISE
	def rotate():
		roomba.rotate()

	#calculate the polygon and drive
	def regularPolygon(n):
		Angle = degrees - degrees/n
		sideLength = Length/n
		driveTime = sideLength/driveSpeed
		
		for n
			#driving for the calculated time
			drive(driveTime)
			#rotating specific degree amount
			rotate()
			time.sleep(driveTime)

	def main():
		# (A) initialize a connection
	    roomba = SerialInterface()
	    # (A) set in passive and safe mode
	    roomba.setState("SAFE")
	    roomba.setState("PASSIVE") #I dont think we have passive declared yet
	    if (ReadButton(CLEAN))
		    # (B) Given an input N move counter clockwise
		    regularPolygon()
	    
