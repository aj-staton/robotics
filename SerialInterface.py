'''
' This class will interface with the Serial Connection. Very basic,
' passthrough opertaions.
'
' Written by: IJ Salman
' Typed by: Austin Staton -- September 9th, 2019
'''
import serial
import time # Needed to sleep between commands.


class SerialInterface:
    def __init__(self):
        # Accesses needed port and sets data transfer rate.
        self.connection = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

    def Close(self):
        self.connection.close()

    # This function will read data from the serial connection.
    # Param: data -- specifes the number of bytes to be read back. 
    def Read(self, data):
        return self.connection.read(data)
    
    # This function sends data thorugh a serial connection. 
    # Param: data -- the bits to send. 
    def Write(self, data):
        self.connection.write(data)
        time.sleep(0.0125)
