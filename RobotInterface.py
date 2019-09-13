####################################################################
# Button Opcode 165
# Bit:	7	6	5	4	3	2	1	0
# value: CLOCK SCHEDULE DAY HOUR MINUTE DOCK SPOT CLEAN
####################################################################
Buttons = 165
####################################################################
# State Opcodes
####################################################################
START = 128
RESET = 7
STOP = 173
PASSIVE = 
SAFE = 131
####################################################################
# Drive Opcode 137
# Serial sequence: [137] [Velocity high byte] [Velocity low byte] 
# [Radius high byte] [Radius low byte]
#
# Velocity (-500 – 500 mm/s)
# Radius (-2000 – 2000 mm)
#
####################################################################
Drive = 137
####################################################################
# DriveDirect Opcode 145
# Serial sequence: [137] [Velocity high byte] [Velocity low byte] 
# [Radius high byte] [Radius low byte]
#
# Right wheel velocity (-500 – 500 mm/s)
# Left wheel velocity (-500 – 500 mm/s)
#
####################################################################
DriveDirect = 145

class RobotInterface:

		def __Init__(self):
				Serial = SerialInterface()

		def SetState(self, setState):
			if (setState == "start") 
				Serial.write(STATE)
			else if (setState == "reset")
				Serial.write(RESET)
			else if (setState == "stop")
				Serial.write(STOP)
			else if (setState == "SAFE")
				Serial.write(SAFE)









