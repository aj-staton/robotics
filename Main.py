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

high = 00000000 # calculated for 150 mm/s
low = 10110110 # calculated for 150 mm/s
driveSpeed = 150 # in mm/s 
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
    ###############################################################
    #  Drive() Calculates the Side lengths based off the
    # 		   total perimeter of 2000mm, and the drives for the 
    #		   correct amount of time asuming 150 mm/s veloctiy.
    #		   
    ###############################################################	
    def driveSide():
		sideLength = Length/n
		driveTime = sideLength/driveSpeed
		roomba.driveDirect(high,low,high,low)
		time.sleep(driveTime)

    ###############################################################
    #  Rotate() Uses the driveDirect function, but only rotates
    # 		    one wheel, allowing us to turn
    #		   
    #		   
    ###############################################################	
    def rotate():
		Angle = degrees - degrees/n
		rotateTime = angle/drivespeed
		roomba.driveDirect(high,low,high,high) #passing in high b/c its 0s
		time.sleep(10) # we can adjust this/figure our rotate time

	
	###############################################################
    #  regularPolygon() Once the robot is powered on, this method
    # 		   			waits for the clean button to be pressed.
    #		   			Once pressed - it drives the length of a 
    #					side and turns. Repeats this N times.
    #		   
    ###############################################################	
	def regularPolygon(n):
		while (ReadButton(CLEAN))
			for n
				driveSide()
				rotate()


###############################################################
#  Main() Sets the robot into safe and passive mode, and then
# 		   runs our draw regularPolygon() method
#		   
#		   
###############################################################	
if __name__ == "__main__":
	    roomba = SerialInterface()
	    roomba.setState("SAFE")
	    #roomba.setState("PASSIVE") #I dont think we have passive declared yet

	   	#Just drive here, and see if we can get the drive function working
	    driveSide()


	
