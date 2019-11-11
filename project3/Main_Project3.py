####################################################################
# This the main program that will be interacting
# with the robot in Project 3.
#
# Written by: Robert Carff, Austin Statin, Miles Ziemer
#           -- November 4th, 2019
####################################################################
####################################################################
# Imports
from RobotInterface import *
from time import sleep
import math
from threading import Thread, Lock
import random
import logging
from simple_pid import PID

####################################################################
# Magic number Variables
_degrees_ = 360 #this is in degrees
_length_ = 2000 #this is in milimeters
_sleepTime_ = 0.0125 #this time is in seconds (12.5 miliseconds)
_velocity_ = 150 # in mm/s
_l_ = 235 #distance between wheels
_omega_ = float(2*_velocity_)/_l_ #angular velocity
_ROTATECW_ = 1 #Tells the roomba to rotate
_ROTATECCW_ = - 1 #Tells the roomba to rotate
_NOROTATE_ = 0 #Tells the roomba to not rotate
# Lets assuming we're driving at 150 mm/s still
_rotateLowTime_ = float(2.356)/_omega_ #time for 135 degrees in radians
_rotateHighTime_ = float(3.926)/_omega_ #Time of 225 degrees in radians
_DELAY_ = 0.015 # 15 ms = 0.015 s
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

roomba = RobotInterface() #Initialize the robot interface
lock = Lock() #Initialize lock variable

###############################################################
# stopRoomba() sends the drive command with zero velocity and
# zero turning radius, thus, stopping the robot.
###############################################################
def stopRoomba():
    roomba.driveDirect(0,0)

###############################################################
#  rotate() uses the drive() function, but only rotates
#  one wheel, allowing us to turn counter-clockwise.
#
#   we need to turn 180, and then +-45
#   so turn (135 - 225)
###############################################################
def rotate(direction):
    # TODO: make this more directed to correction, not a random
    # value. 
    
    roomba.driveDirect(_velocity_, direction)
    # pick a random wait time for 135-225 degrees
    turnTime = random.uniform(_rotateLowTime_,_rotateHighTime_)
    #theta = turnTime * _omega_
    # turn for that amount of time
    print("Rotate: " + str(turnTime) + " ms")
    time.sleep(turnTime)
    stopRoomba()
    roomba.drive(_velocity_,_NOROTATE_)

###############################################################
# driveLogic() will read all of the bumpers on the roomba
# collectively. When one of these bumpers is hit, the roomba
# will turn as needed.
###############################################################
def driveLogic():
    time.sleep(_DELAY_) # Used to minorly delay sensor reading.
    if(roomba.isDriving):

    # TODO: Interpret IR sensor readings, which is already done
    # in roomba.readSensors() (called by readSensors).
    # roomba.leftIRSensor...
    # roomba.rightIRSensor...
    # TODO: Create PID logic

        if(roomba.bumpLeft and roomba.bumpRight):
            stopRoomba()
            roomba.getDistance()
            rotate(_ROTATECW_)
            roomba.getAngle()

        if(roomba.bumpLeft):
            stopRoomba()
            roomba.getDistance()
            rotate(_ROTATECCW_)
 	        roomba.getAngle()

        if(roomba.bumpRight):
            stopRoomba()
            roomba.getDistance()
            rotate(_ROTATECW_)
            roomba.getAngle()

        if (roomba.wheelDropLeft or roomba.wheelDropRight):
            stopRoomba()
            roomba.playSong()
            print("WheelDrop--Playing Song")

###############################################################
# readSensors() iteratively reads all the needed sensors on
# the roomba. Since sensors cannot be read more frequently than
# dt = 0.15 ms, a design decision was made to consolidate these
# into thier own thread.
# This function ALSO controls the logic for driving, based off
# of these sensor readings.
###############################################################
def readSensors():
    while(True):
        time.sleep(_DELAY_)
        roomba.readSensors()
        driveLogic()
        right = roomba.readInfraredRight()
        print("RIGHT: " + right)
        left = roomba.readInfraredLeft()
        print("LEFT: " + left)

###############################################################
#  main() controls all actions of execution, including calling
#  for the drawing of the N-sided polygon for Project 1.
###############################################################
def main():
    roomba.setState("START")
    roomba.setState("SAFE")
    logging.basicConfig(level=logging.DEBUG,filename="output.log",filemode="w")
    
    check = Thread(target = readSensors)

    # Listen for the press of the Clean button, which will begin
    # the drawing of the polygon.
    started = False
    while (not started):
        if(roomba.readButton(_CLEAN_)):
            roomba.drive(_velocity_,_NOROTATE_)      
            roomba.setDriving(True)
            started = True
            roomba.setPressed(False)
        time.sleep(_DELAY_)

    check.start()
    print("STARTING")

    # This while loop reads the 'Clean' button and starts/stops the roomba. 
    while(True):
        if(roomba.buttonPressed and roomba.isDriving):
            roomba.setPressed(False)
            roomba.setDriving(False)
            stopRoomba()
        elif(roomba.buttonPressed and not(roomba.isDriving)):
            roomba.setPressed(False)
            roomba.setDriving(True)
            roomba.driveDirect(_velocity_,_NOROTATE_)
        time.sleep(_DELAY_)

    # End our threads and stop the roomba.
    check.join()
    stopRoomba()
    sys.exit()

main()
