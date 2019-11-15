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
_LEFT_ = 150
_RIGHT_  = 150
# Lets assuming we're driving at 150 mm/s still
_rotateLowTime_ = float(2.356)/_omega_ #time for 135 degrees in radians
_rotateHighTime_ = float(3.926)/_omega_ #Time of 225 degrees in radians
_DELAY_ = 0.015 # 15 ms = 0.015 s
# PID CONTROLER VARIABLES
_S_ = 7000
_KP_ = 1 
_KD_ = 1
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
    turnTime = .25
    time.sleep(turnTime)
    stopRoomba()
    roomba.drive(_velocity_,_NOROTATE_)

def PID():
    ####################### PID ####################################
    _PREVERROR_ = 0
    _CURRENTERROR_ = 0
    _PREVERROR_ = _CURRENTERROR_ #intial value will be 0
    _CURRENTERROR_ = roomba.getRightIR() - _S_
    # read sensors
    # TODO: Create PID logic
    U = _KP_ * _CURRENTERROR_ + (_CURRENTERROR_ - _PREVERROR_)/_DELAY_# 15 ms = 0.015 s
    # using 
    print("Error: " + str(U))
    return U

###############################################################
# driveLogic() will read all of the bumpers on the roomba
# collectively. When one of these bumpers is hit, the roomba
# will turn as needed.
###############################################################
def driveLogic():
    # _PREVERROR_ = _CURRENTERROR_ #intial value will be 0
    if(roomba.isDriving):

        if (PID() > 0):
            roomba.driveDirect((right - u) , (left + u) )

        elif (PID() < 0):
            roomba.driveDirect((right + u) , (left - u) )
        ####################### PID ####################################
        
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
