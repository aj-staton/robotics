####################################################################
#This the main program that will be running and Interacting
# with the robot
#
# Typed by: Robert Carff -- September 15th, 2019
#
####################################################################
# Magic number Variables
degrees = 360 #this is in degrees
Length = 2000 #this is in milimeters
driveSpeed = 150 #this is the speed in mm/s
n = 5 #this is number of sides for the polygon
####################################################################
# Imports
import RobotInterface
####################################################################
class main:
	#drive direct at 150 mm/s speed 
	def drive():
		roomba.driveDirect()
		
	#rotating at a specified speed COUNTER CLOCKWISE
	def rotate():
		roomba.rotate()

	#calculate the polygon and drive
	def regularPolygon(n):
		Angle = degrees/n
		sideLength = Length/n
		driveTime = sideLength/driveSpeed
		for n
			#driving for the calculated time
			drive()
			rotate()

	def main():
		# (A) initialize a connection
	    roomba = SerialInterface()
	    # (A) set in passive and safe mode
	    roomba.setState("SAFE")
	    roomba.setState("PASSIVE") #I dont think we have passive declared yet

	    # (B) Given an input N move counter clockwise
	    regularPolygon()
	    #
