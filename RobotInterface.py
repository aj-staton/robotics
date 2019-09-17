'''
This file's purpose is to define an interface to communicate with the
iRobot Roomba Create2 robot. This will include changing the mode of operation
on the robot, reading input from the robot's physical buttons, and moving
the robot.

Written by: Miles Ziemer, Robby Carff, and Austin Staton for use in CSCE 274
Date: September 15th, 2019
'''
import time
import sys
from SerialInterface import *
import struct

####################################################################
# Button Opcode 165
# Bit Number:  7	6	5	4	3	2	1	0
# Bit Number Value: CLOCK SCHEDULE DAY HOUR MINUTE DOCK SPOT CLEAN
####################################################################
BUTTONS = chr(165)
####################################################################
# State Opcodes
####################################################################
START = chr(128)
RESET = chr(7)
STOP = chr(173)
PASSIVE = chr(128)
SAFE = chr(131)
####################################################################
# DriveDirect Opcode 145
# Serial sequence: [137] [Velocity high byte] [Velocity low byte] 
# [Radius high byte] [Radius low byte]
#
# Right wheel velocity (-500 – 500 mm/s)
# Left wheel velocity (-500 – 500 mm/s)
#
####################################################################
DRIVE = chr(145)


class RobotInterface:
    
    def __Init__(self):
	self.connection = SerialInterface()

    ################################################################
    #  SetState() will change the mode of operation on the iRobot. A 
    #  string will be inputted into the function to enhance the 
    #  readability in other files using this interface. The Robot
    #  Interface will handle the conversion of this state, inputted 
    #  as string, to the bitwise representation needed by the iRobot.
    #  This will be done using the predefined opcodes within this file.
    #
    #  Param: state -- The robot's state in plain english, as a 
    #                  string.
    ################################################################
    def SetState(self, state): 
        if state == "STOP"
	    self.connection.Write(STOP)
        else if state == "RESET":
            self.connection.Write(RESET)
        else if state == "START":
            self.connection.Write(START)
        else if state == "PASSIVE":
            self.connection.Write(PASSIVE)
        else if state == "SAFE":
            self.connection.Write(SAFE)
        else
            print "Invalid state input into the SetState function"
            sys.exit()

    ###############################################################
    #  ReadButton() reads the byte that is returned from the iRobot
    #  when a button on the robot is pressed. This byte will then
    #  be ANDed (bitwise) with the parameter, 'button', which will
    #  pass in the intended button to read. A true/false value for
    #  whether or not the intended button was pressed will be
    #  returned.
    #
    #  Param: button -- The button that is intended to be pressed.
    #                   This will be passed as a hex value to later
    #                   be ANDed with the robot's returned byte.  
    ###############################################################
    def ReadButton(self, button):
        # Send a request to read the pressed button.
        self.connection.Write(BUTTONS)
        button_input = self.connection.Read()
        return(button & struct.unpack('B', button_input))



    #TODO WHAT IF WE MAKE THIS TAKE IN THE FULL 16 BIT NUMBER
    #AND THEN BREAK IT APART INTO TWO PEICES AND PACK IT
    #THAT WAY WE CAN CALL 
    #	(roomba.DriveDirect(leftSpeed,rightSpeed))
    def DriveDirect(self, HighR, LowR, HighL, LowL):
	opcode = struct.pack('B', DRIVE)
	self.connection.Write(opcode) # Can we write a struct??
	time.sleep(0.00675)

	highR = struct.pack('B', HighR)
	self.connection.Write(highR)
	time.sleep(0.00675)
 
	lowR = struct.pack('B', LowR)
	self.connection.Write(lowR)
	time.sleep(0.00675)

	highL = struct.pack('B', HighL)
	self.connection.Write(highL)
	time.sleep(0.00675)

	lowL = struct.pack('B', LowL)
	self.connection.Write(lowL)
	time.sleep(0.00675) 
