####################################################################
# This the main program that will be interacting
# with the robot in Project 3.
#
# Written by: Robert Carff, Austin Statin, Miles Ziemer
#           -- November 25th, 2019
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
    roomba.drive(_velocity_, direction)
    # pick a random wait time for 135-225 degrees
    turnTime = random.uniform(_rotateLowTime_,_rotateHighTime_)
    time.sleep(turnTime)
    stopRoomba()
    roomba.drive(_velocity_,_NOROTATE_)

###############################################################
#  PDControl() implements Proportional, Derivative Control for
#  the iRobot's right infrared sensor.
#
#  Returned Value: U -- the error of the current state from S,
#                       the set point wrt PD control.
###############################################################
def PDControl():
    S = 17000 # Set Point (i.e. -- the "ideal" sensor value)
    KP = 0.002 # Proportial Gain 
    KD = 0.002 # Derivative Gain
    PREV_ERROR = 0 
    CURRENT_ERROR = 0
    PREV_ERROR = CURRENT_ERROR
    CURRENT_ERROR = roomba.getRightIR() - S
    # The error, wrt PD control, is 'U'
    U = KP * CURRENT_ERROR + KD*(CURRENT_ERROR - PREV_ERROR)
    # Since this error value is used to alter driveDirect()
    # velocities, it must have a maximun and minumum, or else
    # there will be overflow within driveDirect(). 
    if (U > 100):
        U = 100
    elif (U < -100):
        U = -100
    return U


###############################################################
# TODO: This should only happen on the clean button press
# PIDLogic() will calculate the state error of the iRobot when
# the 'CLEAN' button is pressed, and our robot must exhibit a 
# wall-following behavior.
###############################################################
# DOCK SENSOR STATES #
ForceField = 161
Green_Buoy = 164
Green_Buoy_ForceField = 165
Red_Buoy = 168
Red_Buoy_ForceField = 169
Red_Buoy_and_Green = 168

def PIDLogic():
    if(not roomba.dockFound and roomba.isDriving):
        if (PDControl() > 0):
            roomba.driveDirect((_RIGHT_ + abs(PDControl())) , (_LEFT_ - abs(PDControl())))
        elif (PDControl() < 0):
            roomba.driveDirect((_RIGHT_ - abs(PDControl())) , (_LEFT_ + abs(PDControl())))

        if(roomba.charOmni > 0):  #or roomba.charRight > 0): # if anything is picked up
            roomba.dockFound = True
            findDock()
    # If the dock is found, stop following the wall.
    elif(roomba.dockFound and roomba.isDriving):
        findDock()

def findDock():
    while (roomba.chargingState == 0):
        print("FUCK")
        # The case for if the roomba is aligned perfectly with the dock.
        # This is the IDEAL case.
        if (roomba.charOmni == 172):
            roomba.driveDirect(60,60)
        # If the omni character is reading the RED (right) buoy from the dock,
        # we know it needs to move left.
        elif (roomba.charOmni == 168):
            roomba.driveDirect(40, 60)
        # If the omni character is reading the GREEN (left) buoy from the dock,
        # we know the roomba shuld move right.
        elif (roomba.charOmni == 164):
            roomba.driveDirect(60, 40)
        else:
            roomba.driveDirect(10,-10)
        time.sleep(_DELAY_)

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
        PIDLogic()

###############################################################
###############################################################
#  main() controls all actions of execution, including calling
#  for the drawing of the N-sided polygon for Project 1.
###############################################################
###############################################################
def main():
    roomba.setState("START")
    roomba.setState("SAFE")
    roomba.playSong()
    logging.basicConfig(level=logging.DEBUG,filename="output.log",filemode="w")
    check = Thread(target=readSensors)
    # Listen for the press of the Clean button, which will begin
    # the drawing of the polygon.
    started = False
    while (not started):
        if(roomba.readButton(_CLEAN_)):
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
        if (roomba.chargingState > 0):
            check.join()
            roomba.playSong()
            break
        time.sleep(_DELAY_)
    # End our threads and stop the roomba.
    #check.join()
    stopRoomba()
    sys.exit()
main()
