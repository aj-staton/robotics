####################################################################
# This the main program that will be interacting
# with the robot in Project 2. 
#
# Written by: Robert Carff, Austin Statin, Miles Ziemer 
#           -- October 5th, 2019
#
####################################################################
####################################################################
# Imports
from RobotInterface import *
from time import sleep
import math
from threading import Thread
import random
####################################################################
# Magic number Variables
_N_ = 4 #this is number of sides for the polygon
_degrees_ = 360 #this is in degrees
_length_ = 2000 #this is in milimeters
_sleepTime_ = 0.0125 #this time is in seconds (12.5 miliseconds)
_velocity_ = 150 # in mm/s
_l_ = 235 #distance between wheels
_omega_ =  float(2*_velocity_)/_l_ #angular velocity
_ROTATECW_ = 1 #Tells the roomba to rotate
_ROTATE_ = 1 #Tells the roomba to rotate
_NOROTATE_ = 0 #Tells the roomba to not rotate
_sideLength_ = float(_length_)/_N_ #Side length of polygon
_driveTime_ = float(_sideLength_)/_velocity_ #Time of driving along a side
_rotateTime_ = float(2*math.pi/_N_)/_omega_ #Time of rotating

# Lets assuming we're driving at 150 mm/s still
_rotateLowTime_ = float(2.356)/_omega_ #time for 135 degrees in radians
_rotateHighTime_ = float(3.926)/_omega_ #Time of 225 degrees in radians



roomba = RobotInterface() #Initialize the robot interface
#_isDriving_ = True #The state of the roomba, if it is driving or not
####################################################################
# Button Opcode 165
# Bit Number:  7    6   5   4   3   2   1   0
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

###############################################################
# stopRoomba() sends the drive command with zero velocity and
# zero turning radius, thus, stopping the robot.
#
############################################################### 
def stopRoomba():
    roomba.drive(0,0)

###############################################################
# driveSide() calculates the Side lengths based off the
# total perimeter of 2000mm, and the drives for the 
# correct amount of time asuming 150 mm/s veloctiy.
#                  
############################################################### 
def driveSide():
    roomba.drive(_velocity_, _NOROTATE_)
    time.sleep(_driveTime_)
    while(not roomba.isDriving):
        time.sleep(.012)
    stopRoomba()

###############################################################
#  rotate() uses the drive() function, but only rotates
#  one wheel, allowing us to turn counter-clockwise.
#  
#   we need to turn 180, and then +-45
#   so turn (135 - 225)
############################################################### 
def rotateRandom():
    roomba.drive(_velocity_, 1)
    # pick a random number between 135-225 degrees
    for x in range(_rotateLowTime_,_rotateHighTime_):
        turnTime = random.randint(1,101)
    # turn for that amount of time    
    time.sleep(_rotateTime_)
    stopRoomba()

###############################################################
# mainDrive() continuously checks the boolean values of our 
# sensors to see if they have been pressed. If so, an action
# taken.         
############################################################### 
def mainDrive():
roomba.setDrive() # setting driving to true
roomba.drive(_velocity_, _NOROTATE_) # actually driving

    while(roomba.isDriving):
        roomba.sleep(.015)
        #WE NEED TO ROTATE LEFT OR RIGHT DEPENDING ON BUMPER
        if(leftBumperPressed):
            write(getDistance) # this method write to output
            rotateRandom()
            roomba.drive(_velocity_, _NOROTATE_)
        else if(rightBumperPressed):
            write(getDistance) # this method write to output
            rotateRandom()
            roomba.drive(_velocity_, _NOROTATE_)


        else if (clean button pressed):
            stopRoomba()
            roomba.setDrive() # setting driving to false
            break
        else:
            continue

###############################################################
#  readCleanButtonThread() is what checks the iRobot's clean button
#  during execution. It does this with threading.
#          
############################################################### 
def readCleanButtonThread():
    while(True):
        #global _isDriving_
        time.sleep(.10)
        if(roomba.readButton(_CLEAN_, chr(18))):
            #_isDriving_ = not _isDriving_
            roomba.setDrive()
            
###############################################################
#  readBumperThread() calls our readBumper method in the Interface 
#  the method in the interface already sets out global variables      
############################################################### 
def readBumperThread():
    while(True):
        time.sleep(.10)
        # this method sets our 4 global variables
        roomba.readBumper()

###############################################################
#  main() controls all actions of execution, including calling
#  for the drawing of the N-sided polygon for Project 1.
############################################################### 
def main():
    # setting states
    roomba.setState("SAFE")
    # declaring threads
    button = Thread(target = readCleanButtonThread)
    bump = Thread(target = readBumperThread) 
    # starting threads
    button.start();
    bump.start();
    # waiting to start 
    x = True
    # Listen for the press of the Clean button, which will begin
    # the drawing of the polygon.
    while (x):
        # ALSO CHECK IF THE WHEEL DROPS AND CLIFFS ARE ACTIVATED
        if(roomba.readButton(_CLEAN_)):
            x = False

    mainDrive() #drive and turn a bunch

    # end our threads and stop the roomba
    button.join()
    bump.join()
    stopRoomba()
    sys.exit()
main()
