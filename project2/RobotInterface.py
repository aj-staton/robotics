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
# Bit Number:  7    6   5   4   3   2   1   0
# Bit Number Value: CLOCK SCHEDULE DAY HOUR MINUTE DOCK SPOT CLEAN
####################################################################
_BUTTONS_ = 165
####################################################################
# Opcodes
####################################################################
_START_ = 128
_RESET_ = 7
_PLAY_ = 141
_STOP_ = 173
_PASSIVE_ = 128
_SAFE_ = 131
_FULL_ = 132 
_DRIVE_ = 137
_DRIVE_DIRECT_ = 145
_SENSORS_ = 142
###################################
# The use of _SENSORS_ is followed
# with the packet ID of the needed
# sensor data. These IDs are below:
###################################
_idBUMPSANDDROPS_ = 7
_idBUTTONS_ = 18
_idDISTANCE_ = 19
_idANGLE_ = 20
_idCLIFFLEFT_ = 9
_idCLIFFRIGHT_ = 12
_idCLIFFFRONTRIGHT_ = 10
_idCLIFFFRONTLEFT_ = 11
##########################################################
# Read the state of the sensors.
#  every 15 ms.  Do not send these commands more
#  frequently than that.
_DELAY_ = 0.015 # 15 ms = 0.015 s
###########################################################

class RobotInterface:
    def __init__(self):
        self.connection = SerialInterface()
        ################################################################
        # Flags for sensor states
        ################################################################
        self.isDriving = True
        self.bumpLeft = False
        self.bumpRight = False
        self.wheelDropLeft = False
        self.wheelDropRight = False

    ################################################################
    # getDistance() returns the distance that the Roomba has travel-
    # ed, in millimeters, since the last time the distance was re-
    # quested. So, getDistance() must be called at initalization.
    # 
    # This fuction will return the distance traveled, in mm.
    ################################################################
    def getDistance(self):
        # Send the request for data.
        sentData = struct.pack('>B2H', _SENSORS_, _idDISTANCE_)
        self.connection.write(sentData)
        # Retrieve the data.
        distanceBin = self.connection.read(2)[0]
        time.sleep(_DELAY_)
        # Interpret the bytes, where the 2^15 bit is the sign.
        distanceInt = struct.unpack('>h', distanceBin)
        # **How do I read a signed pair of bits??

    ################################################################
    # Setters for driving
    ################################################################
    def setDriving(self):
        self.isDriving = not isDriving

    ################################################################
    # Setters for Bumpers
    ################################################################
    def setBumpLeft(self):
        self.bumpLeft = not bumpLeft

    def setBumpRight(self):
        self.bumpRight = not bumpRight

    ################################################################
    # Setters for wheel drops
    ################################################################
    def setWheelDropLeft(self):
        self.wheelDropLeft = not wheelDropLeft

    def setWheelDropRight(self):
        self.wheelDropRight = not wheelDropRight

    ################################################################
    # Setters for CliffPackets here?
    ################################################################

    ################################################################
    #  setState() will change the mode of operation on the iRobot. A 
    #  string will be inputted into the function to enhance the 
    #  readability in other files using this interface. The Robot
    #  Interface will handle the conversion of this state, inputted 
    #  as string, to the bitwise representation needed by the iRobot.
    #  This will be done using the predefined opcodes within this file.
    #
    #  Param: state -- The robot's state in plain english, as a 
    #                  string.
    #
    #
    ################################################################
    def setState(self, state): 
        if state == "STOP":
            self.connection.write(chr(_STOP_))
            print "iRobot Mode: STOP"
        elif state == "RESET":
            self.connection.write(chr(_RESET_))
            print "iRobot Mode: RESET"
        elif state == "START":
            self.connection.write(chr(_START_))
            print "iRobot Mode: START"
        elif state == "PASSIVE":
            self.connection.write(chr(_PASSIVE_))
            print "iRobot Mode: PASSIVE"
        elif state == "SAFE":
            self.connection.write(chr(_SAFE_))
            print "iRobot Mode: SAFE"
        elif state == "FULL":
            self.connection.write(chr(_FULL_))
            print "iRobot Mode: FULL"
        else:
            print "Invalid state input in the setState() function"
            sys.exit()

    ###############################################################
    #  readButton() reads the byte that is returned from the iRobot
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
    def readButton(self, button):
        # Send a request to read the pressed button.
        self.connection.write(chr(_SENSORS_) + chr(_idBUTTONS_))
        button_input = self.connection.read(1)
        return bool(struct.unpack('B', button_input)[button])

    ###############################################################
    # readBumper() takes in the Packet ID we need from the sensors 
    # **** It returns a byte that we need to still unpack
    ###############################################################
    def readBumper(self):
        # Send a request to read the pressed button.
        self.connection.write(chr(_SENSORS_) + chr(_idBUMPSANDDROPS_))
        bumper = self.connection.read(1)
        # Set boolean sensor values based on the respective bit values. 
        reading = (struct.unpack('B', bumper)[0])
        print(reading)
        bumpRight = bool(reading & 0x00)
        print("BR: " + str(bumpRight))
        bumpLeft = bool(reading & 0x01)
        print("BL: " + str(bumpLeft))
        wheelDropRight = bool(reading & 0x02)
        print("WDR: " + str(wheelDropRight))
        wheelDropLeft = bool(reading & 0x03)
        print("WDL: " + str(wheelDropLeft))
        print()

        time.sleep(0.015)
        '''
        now we have our states set and we can just thread this method
        then we just check in main:
            if(WheelDropLeft):
                turn 45 right
            if(WheelDropRight):
                turn 45 left
        '''
    ###############################################################
    #  we need to read cliff sensors, 9-13
    # they return a 1 bit value (as a byte though)
    # no need to decode byte
    ###############################################################

    # TODO FIGURE OUT THIS METHOD
    def readCliff(self, ID):
        # the ID should be 9-13, can run it through a loop
        self.connection.write(chr(_SENSORS_) + chr(ID))
        cliff = self.connection.read(1)
        # how do we want to declare the cliff global variables
        # array?
        cliff[ID] = struct.unpack('B', cliff)

    ###############################################################
    # drive() is the main fucntion of movement for the Roomba. It 
    # will accept values for velocity(mm/s) and turning radius(mm).
    # To turn in place clockwise, -1 is the value to send as the
    # turning radius. A value of 1 is sent for a clockwise turn in
    # place.
    #
    # Limitations: The iRobot Create2 can only accept values
    #              between [-500,500] for the velocity of the robot. 
    # 
    # Params: velocity -- the speed and direction of motion that
    #                     the roomba should travel (between -500
    #                     and 500, inclusive).
    # 
    #         radius   -- the amount to turn the robot (in mm). The
    #                     radius is measured from the center of the
    #                     turning circle to the center of the
    #                     roomba.
    ###############################################################
    def drive(self, velocity, radius):
        if (velocity >= -500 or velocity <= 500):
            data = struct.pack('>B2H', _DRIVE_, velocity, radius)
            self.connection.write(data)
        else:
            print("Invalid Drive() speed given.")
            sys.exit()
        
    ###############################################################
    # This method will implement driveDirect for Project 2
    #
    ###############################################################
    def driveDirect(self, velocity, radius):
        if (velocity >= -500 or velocity <= 500):
            data = struct.pack('>B2H', _DRIVE_DIRECT_, velocity, radius)
            self.connection.write(data)
        else:
            print("Invalid Drive() speed given.")
            sys.exit()
    
    ###############################################################
    # playSong() will tell the rommba to play a song. iRobots have
    # pre-made songs to choose from, which people can select.
    # 
    # Params: songNumber -- an integer from [0, 4] which represents
    #                       the song for the roomba to play.
    ###############################################################
    def playSong(self, songNumber):
        if (songNumber >= 0 and songNumber <= 4):
            data = struct.pack('>B2H', _PLAY_, songNumber)
            self.connection.write(data)
    


