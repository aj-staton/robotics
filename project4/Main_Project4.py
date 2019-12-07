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
#  PDRight() implements Proportional, Derivative Control for
#  the iRobot's right infrared sensor.
#
#  Returned Value: U -- the error of the current state from S,
#                       the set point wrt PD control.
###############################################################
def PDRight():
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
    # print("Error: " + str(U))
    return U

GREEN = 164
FORCE = 161
RED = 168
BOTH = 172
_stdspd_ = 50
EMPTY = 0
#############################################################
# driveLogic()
###############################################################
def driveLogic():
    print str(roomba.dockFound)
    ####################
    # Wall Following Behavior
    #####################
    if(roomba.isDriving and  not roomba.dockFound):   
        if (PDRight() > 0):
            roomba.driveDirect((_RIGHT_ + abs(PDRight())) , (_LEFT_ - abs(PDRight())))

        elif (PDRight() < 0):
            roomba.driveDirect((_RIGHT_ - abs(PDRight())) , (_LEFT_ + abs(PDRight())))

        if (roomba.charOmni > 0 ):
            roomba.dockFound = True
            # If the dock is found, but the dock is not in the correct
            # direction of the roomba, find the dock.
            if (roomba.charLeft == EMPTY and roomba.charRight == EMPTY):
                while (roomba.charLeft == EMPTY and roomba.charRight == EMPTY):
                    roomba.driveDirect(-_stdspd_, _stdspd_+2)
    ######################
    # Docking Behavior
    ######################
    elif (roomba.isDriving and roomba.dockFound):
        # Handle if BOTH beams are directed in the center of the roomba.
        if (roomba.charRight == BOTH and roomba.charLeft == BOTH):
            roomba.driveDirect(_stdspd_, _stdspd_)
        elif (roomba.charRight == RED):
            if(roomba.charRight != 172):
                roomba.driveDirect(_stdspd_, _stdspd_)
                time.sleep(_DELAY_ * 30)
            stopRoomba()
        elif (roomba.charLeft == GREEN):
            if(roomba.charLeft != 172):
                roomba.driveDirect(_stdspd_, _stdspd_)
                time.sleep(_DELAY_ * 30)
            stopRoomba()
        # Something went wrong. Fix it.
        elif (roomba.charLeft == 0 and roomba.charRight == 0):
            while (roomba.charLeft == EMPTY and roomba.charRight == EMPTY):
                    roomba.driveDirect(-_stdspd_, _stdspd_+2)
        else:
            roomba.driveDirect(_stdspd_,_stdspd_)
            time.sleep(_DELAY_ * 30 )
            print("nothing")


        '''
        elif (roomba.charRight == GREEN and roomba.charLeft == GREEN):
            while (roomba.charRight != BOTH and rooma.charLeft != BOTH):
                roomba.driveDirect(_stdspd_, -_stdspd_)
        # Handle if right beam is directed at the dock, and left is GREEN
        elif (roomba.charRight == BOTH and roomba.charLeft == GREEN):
            roomba.driveDirect(_stdspd_, _stdspd_)
        # Handle if right beam is in RED and left is directed at the dock.
        elif (roomba.charRight == RED and roomba.charLeft == BOTH):
            roomba.driveDirect(_stdspd_, _stdspd_)
        '''
        

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
        # Stop if on dock and charging
        if (roomba.chargingState != 0):
            print("song1")
            time.sleep(_DELAY_)
            roomba.playSong()
            time.sleep(_DELAY_)
            break
    stopRoomba()


def driveLogicThread():
    while(True):
        driveLogic()
        time.sleep(_DELAY_)
        print("charge state   == " + str(roomba.chargingState))
        # Stop if on dock and charging.
        if (roomba.chargingState != 0):
            print("song2")
            time.sleep(_DELAY_)
            roomba.playSong()
            time.sleep(2*_DELAY_)
            break
    stopRoomba()

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
    check = Thread(target = readSensors)
    driving = Thread(target = driveLogicThread)
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
    driving.start()
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
        
        if (roomba.chargingState != 0):
            break
    # End our threads and stop the roomba.
    roomba.playSong()
    check.join()
    driving.join()
    roomba.playSong()
    stopRoomba()
    sys.exit()

main()
