'''
This file's purpose is to define an interface to communicate with the
iRobot Roomba Create2 robot. This will include changing the mode of operation
on the robot, reading input from the robot's physical buttons, and moving
the robot.
Written by: Miles Ziemer, Robby Carff, and Austin Staton for use in CSCE 274
Date: November 4th, 2019
'''
import time
import sys
from SerialInterface import *
import struct
import logging
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
_SONG_ = 140
_STOP_ = 173
_PASSIVE_ = 128
_SAFE_ = 131
_FULL_ = 132 
_DRIVE_ = 137
_DRIVE_DIRECT_ = 145
_SENSORS_ = 142
_CLEAN_ = 0
#########################################################
# The use of _SENSORS_ is followed with the packet ID of
# the needed sensor data. These IDs are below:
#########################################################
_idBUMPSANDDROPS_ = 7
_idBUTTONS_ = 18
_idDISTANCE_ = 19
_idANGLE_ = 20
_idINFRAREDLEFT_ = 48
_idINFRAREDRIGHT_ = 51
_idDOCKGREEN_ = 52
_idDOCKRED_ = 53
_idOMNI_ = 17
_idCHARGINGSTATE_ = 21

##########################################################
#  Read the sensor state of the Roomba every 15 ms.  Do
#  not send these commands more frequently than that.
##########################################################
_DELAY_ = 0.015 # 15 ms = 0.015 s

logging.basicConfig(level=logging.DEBUG,\
            filename="execution.log",filemode="w")

class RobotInterface:
    def __init__(self):
        self.connection = SerialInterface()
        self.writeSong()
        self.getDistance()
        self.getAngle()
        logging.basicConfig(level=logging.DEBUG,\
            filename="execution.log",filemode="w")
        ###########################
        # Flags for sensor states
        ###########################
        self.isDriving = True
        self.buttonPressed = False
        self.bumpLeft = False
        self.bumpRight = False
        self.wheelDropLeft = False
        self.wheelDropRight = False
        self.leftIRSensor = 0
        self.rightIRSensor = 0
        self.charLeft = 0
        self.charRight = 0
        self.charOmni = 0
        self.chargingState = 0
        self.dockFound = False
        self.isCharging = False


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
    #           radius -- the amount to turn the robot (in mm). The
    #                     radius is measured from the center of the
    #                     turning circle to the center of the
    #                     roomba.
    ############################################################### 
    def drive(self, velocity, radius):
        if (velocity >= -500 or velocity <= 500):
            data = struct.pack('>Bhh', _DRIVE_, velocity, radius)
            self.connection.write(data)
            # WE CAN SET THE DRIVING BOOL HERE
            # setDriving(True)
        else:
            print("Invalid drive() speed given.")
            sys.exit()
      
    ###############################################################
    # driveDirect() is different than drive(). While each moves the
    # iRobot, drive() sets a velocity for both wheels and using the
    # passed parameter of turning radius, turns the roomba.
    # This function passes in two separate velcities for the left
    # and right wheels of the roomba; the turning radius calcultion
    # is delegated to the user of this API.
    #
    # Params: rightVelocity -- the angular velocity of the right
    #                          wheel (range [-500, 500]).
    #               
    #          leftVelocity -- the angular velocity of the left
    #                          wheel (range [-500,500]).
    ###############################################################
    def driveDirect(self, rightVelocity, leftVelocity):
        # for right
        if (rightVelocity >= 500):
            rightVelocity = 500
        if (leftVelocity >= 500):
            leftVelocity = 500
        # for left
        if (rightVelocity <= -500):
            rightVelocity = -500
        if (leftVelocity <= -500):
            leftVelocity = -500
        data = struct.pack('>Bhh', _DRIVE_DIRECT_, rightVelocity, leftVelocity)
        self.connection.write(data)

    ################################################################
    # getAngle() returns the angle that the Roomba has turned,
    # in degrees, since the last time the angle was re-
    # quested. So, getAngle() must be called at initalization.
    # 
    # This fuction will return the angle turned, in degrees.
    ################################################################
    def getAngle(self):
        # Send the request for data.
        sentData = struct.pack('Bb', _SENSORS_, _idANGLE_)
        self.connection.write(sentData)
        # Retrieve the data.
        reading = self.connection.read(2)
        time.sleep(_DELAY_)
        # Interpret the bytes, where the 2^15 bit is the sign.
        angle = struct.unpack('h', reading)[0]
        logging.info("ANGLE: " + str(angle))
        return angle

    ################################################################
    # getDistance() returns the distance that the Roomba has travel-
    # ed, in millimeters, since the last time the distance was re-
    # quested. So, getDistance() must be called at initalization.
    # 
    # This fuction will return the distance traveled, in mm.
    ################################################################
    def getDistance(self):
        # Send the request for data.
        sentData = struct.pack('Bb', _SENSORS_, _idDISTANCE_)
        self.connection.write(sentData)
        # Retrieve the data.
        reading = self.connection.read(2)
        time.sleep(_DELAY_)
        # Interpret the bytes, where the 2^15 bit is the sign.
        distance = struct.unpack('h', reading)[0]
        logging.info("DIST: " + str(distance))
        return distance

    ###############################################################
    # playSong() will tell the rommba to play a song. iRobots have
    # require you to create your own song. See writeSong() to view
    # this created song. This function will have song number '0'
    # pre-programmed in, since we are only composing one song in
    # writeSong()
    ###############################################################
    def playSong(self):
        songNumber = 0
        data = struct.pack('BB', _PLAY_, songNumber)
        self.connection.write(data)

    ###############################################################
    # readBumper() gets the value for the iRobot's front left and
    # right bumper, along with the left and right wheel drops.
    # The bit order is:
    #   7    6    5    4     3     2      1       0
    #   X    X    X    X    WDL   WDR   BumpL   BumpR
    # This function does not return these values; rather, it sets
    # the RobotInterface class variables.
    ###############################################################
    def readBumper(self):
        # Send a request to read the pressed button.
        self.connection.write(chr(_SENSORS_) + chr(_idBUMPSANDDROPS_))
        bumper = self.connection.read(1)
        # Set boolean sensor values based on the respective bit values. 
        reading = (struct.unpack('B', bumper))[0]
        #print(reading)
        self.bumpRight = bool(reading & 0x01)
        #print("BR: " + str(bumpRight))
        self.bumpLeft = bool(reading & 0x02)
        #print("BL: " + str(bumpLeft))
        self.wheelDropRight = bool(reading & 0x04)
        #print("WDR: " + str(wheelDropRight))
        self.wheelDropLeft = bool(reading & 0x08)
        #print("WDL: " + str(wheelDropLeft))
        #print("*********")
        if (self.wheelDropLeft or self.wheelDropRight or self.bumpRight or self.bumpLeft == True):
            print("Bumper")
            logging.info("UNSAFE BUMPER")
        time.sleep(_DELAY_)
      
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
        pressed = bool(struct.unpack('B',button_input)[button])
        if(pressed):
            self.buttonPressed = True
            print("Button")
            logging.info("BUTTON")
        return pressed

    ###############################################################
    #  setPressed() is used to flip the boolean value of whether or 
    #  not a button has been pressed (i.e. -- when the clean button
    #  is pressed, the value is true).
    ###############################################################
    def setPressed(self, pressed):
        self.buttonPressed = pressed

    ###############################################################
    #  readDockGreen/Red/Omni() is used to read the Green
    #  (Facing-Dock Left) and Red (Facing-Dock Right) sensors from
    #  the roomba to be able to dock the iRobot Create2.
    ###############################################################
    def readCharLeft(self):
        self.connection.write(chr(_SENSORS_) + chr(_idDOCKGREEN_))
        data = self.connection.read(1)
        self.charLeft = struct.unpack('B', data)[0]
        print("LEFT: " + str(self.charLeft))
    def readCharRight(self):
        self.connection.write(chr(_SENSORS_) + chr(_idDOCKRED_))
        data = self.connection.read(1)
        self.charRight = struct.unpack('B', data)[0]
        print("RIGHT: " + str(self.charRight))
    def readCharOmni(self):
        self.connection.write(chr(_SENSORS_) + chr(_idOMNI_))
        data = self.connection.read(1)
        self.charOmni = struct.unpack('B', data)[0]
        # if (self.charOmni == 161):
        #    self.charOmni = -1
        print("OMNI: " + str(self.charOmni))

    ###############################################################
    # readInfraredRight() returns the 2-byte
    # number from the left and right IR sensors on the Create2.
    ###############################################################
    def readInfraredRight(self):
        self.connection.write(chr(_SENSORS_)+chr(_idINFRAREDRIGHT_))
        data = self.connection.read(2)
        # print(data)
        data1 = struct.unpack('H', data)[0]
        self.rightIRSensor = data1
        # print("RIGHT: " + str(data1))

    #############################################
    # Accessors for the above IR sensors.
    ############################################
    def getRightIR(self):
        return self.rightIRSensor


    ###############################################################
    # readChargingState()
    ###############################################################
    def readChargingState(self):
        self.connection.write(chr(_SENSORS_)+chr(_idCHARGINGSTATE_))
        data = self.connection.read(1)
        data1 = struct.unpack('B', data)[0]
        self.chargingState = data1

    ###############################################################
    # readSensors() is the function that will consolidate the other
    # Create2 sensing functions. This function is called in its own
    # thread outside of the interface to read all sensors indefin-
    # itvely. 
    ###############################################################
    def readSensors(self):
        self.readButton(_CLEAN_)
        self.readBumper()
        self.readInfraredRight()
        self.readCharLeft()
        self.readCharOmni()
        self.readCharRight()
        self.readChargingState()

    ################################################################
    # Setters for Bumpers
    ################################################################
    def setBumpLeft(self, TorF):
        self.bumpLeft = bool(TorF)
    def setBumpRight(self, TorF):
        self.bumpRight = bool(TorF)

    ################################################################
    # Setters for driving
    ################################################################
    def setDriving(self, TorF):
        self.isDriving = bool(TorF)
        
    ################################################################
    # Setters for wheel drops
    # 
    # Param: ToF -- The boolean value to set the state class
    #               variable.
    ################################################################
    def setWheelDropLeft(self, ToF):
        self.wheelDropLeft = bool(TorF)
    def setWheelDropRight(self, TorF):
        self.wheelDropRight = bool(TorF)

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

    #################################################################
    # writeSong() will make the song for the playSong() function to
    # retrieve. This function will write the song to the Roomba's
    # song index of 0.
    #################################################################
    def writeSong(self):
        # Three note song, therefore it will be 7 bytes to write.
        # Hence, the 7 B's for signifying 7 unsigned character bytes.
        songNumber = 0
        songLength = 3 # length of the song, as a quantitify of notes
        songNote1 = 75
        songNote1Length = 60
        songNote2 = 55
        songNote2Length = 30
        # Create the 3-note song.
        data = struct.pack('>BBBBBBBBB', _SONG_, songNumber, songLength,\
                          songNote1, songNote1Length, songNote2, \
                          songNote2Length, songNote1, songNote1Length)
        self.connection.write(data)
      
