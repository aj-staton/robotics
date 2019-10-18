####################################################################
# This the main program that will be interacting
# with the robot in Project 2.
#
# Written by: Robert Carff, Austin Statin, Miles Ziemer
#           -- October 5th, 2019
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
_ROTATE_ = 1 #Tells the roomba to rotate
_NOROTATE_ = 0 #Tells the roomba to not rotate
_rotateTime_ = float(2*math.pi/_N_)/_omega_ #Time of rotating
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
    roomba.drive(0,0)
    logging.info("testing")

###############################################################
#  rotate() uses the drive() function, but only rotates
#  one wheel, allowing us to turn counter-clockwise.
#
#   we need to turn 180, and then +-45
#   so turn (135 - 225)
###############################################################
def rotateRandom(direction): #direction is global CW or CCW
    roomba.drive(_velocity_, direction)
        # pick a random wait time for 135-225 degrees
        turnTime = random.randint(_rotateLowTime_,_rotateHighTime_)
            # turn for that amount of time
            time.sleep(turnTime)
            stopRoomba()

###############################################################
# mainDrive() continuously checks the boolean values of our
# sensors to see if they have been pressed. If so, an action
# taken.
###############################################################
def mainDrive:
    roomba.setDriving(True) # setting driving to true
    roomba.drive(_velocity_, _NOROTATE_) # actually driving

    while(True): # while the roomba is driving
roomba.sleep(_DELAY_)

    #WE NEED TO ROTATE LEFT OR RIGHT DEPENDING ON BUMPE
    if(roomba.bumpLeft && roomba.bumpRight):
        stopRoomba()
            write(getDistance) # this method write to output
            rotateRandom(_ROTATECW_)
            roomba.drive(_velocity_, _NOROTATE_)

if(roomba.bumpLeft):
    stopRoomba()
        write(getDistance) # this method write to output
        rotateRandom(_ROTATECCW_)
        roomba.drive(_velocity_, _NOROTATE_)

    if(roomba.bumpRight):
        stopRoomba()
            write(getDistance) # this method write to output
            rotateRandom()
            roomba.drive(_velocity_, _NOROTATE_)

###############################################################
#  readCleanButtonThread() is what checks the iRobot's clean button
#  during execution. It does this with threading.
###############################################################
'''
    def readCleanButtonThread():
    while(True):
    #global _isDriving_
    time.sleep(.10)
    if(roomba.readButton(_CLEAN_, chr(18)) && not(lock.locked())):
    lock.aquire()
    #_isDriving_ = not _isDriving_
    roomba.setDriving()
    stopRoomba()
    elif(roomba.readButton(_CLEAN_,chr(18)) && lock.locked()):
    lock.release()
    roomba.setDriving()
    roomba.drive(_velocity_,_NOROTATE_)
    '''
###############################################################
#  readBumperThread() calls our readBumper method in the Interface
#  the method in the interface already sets out global variables
###############################################################
def readBumperThread():
    while(True):
        time.sleep(_DELAY_)
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
    drive = Thread(target = mainDrive)
    bump = Thread(target = readBumperThread)
    # declaring our log file
    logging.basicConfig(level=logging.DEBUG,filename="output.log",filemode="w")
    # starting threads
    drive.start()
    bump.start()
    # waiting to start
    x = True
    # Listen for the press of the Clean button, which will begin
    # the drawing of the polygon.
    while (x):
        # ALSO CHECK IF THE WHEEL DROPS AND CLIFFS ARE ACTIVATED
        if(roomba.readButton(_CLEAN_)):
            x = False
    while(True):
        time.sleep(_DELAY_)
        if(roomba.readButton(_CLEAN_) && not(lock.locked())):
        lock.aquire()
        roomba.setDriving()
        stopRoomba()
        elif(roomba.readButton(_CLEAN_) && lock.locked()):
        lock.release()
        roomba.setDriving()
        roomba.drive(_velocity_,_NOROTATE_)             
        stopRoomba()
            #mainDrive() #drive and turn a bunch
                    
        # end our threads and stop the roomba
        drive.join()
        bump.join()
        stopRoomba()
        sys.exit()
#fixed spaces

if __name__ == __main__:
    main()

