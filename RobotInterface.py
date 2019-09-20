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
BUTTONS = 165
####################################################################
# State Opcodes
####################################################################
START = 128
RESET = 7
STOP = 173
PASSIVE = 128
SAFE = 131
####################################################################
# Drive Opcode 137
# Serial sequence: [137] [Velocity high byte] [Velocity low byte] 
#                  [Radius high byte] [Radius low byte]
#
# Right wheel velocity (-500 to 500 mm/s)
# Left wheel velocity (-500 to 500 mm/s)
#
####################################################################
DRIVE = 137


class RobotInterface:
    def __init__(self):
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
        if state == "STOP":
	    self.connection.Write(chr(STOP))
        elif state == "RESET":
            self.connection.Write(chr(RESET))
        elif state == "START":
            self.connection.Write(chr(START))
        elif state == "PASSIVE":
            self.connection.Write(chr(PASSIVE))
        elif state == "SAFE":
            self.connection.Write(chr(SAFE))
        else:
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
        return (button & struct.unpack('B', button_input))

    def Drive(self, velocity, radius):
	data = struct.pack('>B2H', DRIVE, velocity, radius)
        # Pack all of the bytes at once.
        self.connection.Write(data)
	    
