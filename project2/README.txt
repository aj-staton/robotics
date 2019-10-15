--------------------
-CSCE 274 Project -
--------------------
The primary goal of the first project was to ... 

All work was completed by Robert Carff, Miles Ziemer, and
Austin Staton for this assignment. The teaching assistant,
Ibrahim Salman, offered some guidance; however, any sub-
stance to this work was performed by the formerly mentioned
contributers.

-------
-Files-
-------
Each needed file is listed and described below:
  SerialInterface.py -- this file transfers data to the
                     iRobot Create2 via Serial Communi-
                     cation. It serves as the interface
                     for reading and writing data, as
                     well as opening and closing the
                     initial Serial data connection. 

  RobotInterface.py -- the Robot Interface is the link of
                    communication to the iRobot. This in-
                    cludes, but is not limited to, 
                    controlling the robot's: movement, mode
                    of opertaion, sensors, and actuators.

  Main_Project2.py --

-----------
-Execution-
-----------
Limitations:
** I am assuming the user is on a Debian-based Linux
   operating system. If this prerequisite is not met, the
   below actions will not preoduce their desired result.

To execute this program, thus instructing the iRobot to
create a polygon, do the following:
  1. Ensure that all listed files (above) are stored in the
     same folder/directory. We have not accounted for the
     manueverability of files.

  2. Connect an ethernet (Cat-5/6) cord to the Raspberry Pi
     located on top of the iRobot Create2. Ensure the
     Rasperry Pi is powered on.

  3. Transfer all needed files (again, they're listed above)
     to the Raspberry Pi via secure copy. This is done with
     the below command in the terminal:
       $ scp SerialInterface.py RobotInterface.py
             Main_Project1.py pi@192.168.1.1:~/

  4. Establish a connection with the Raspberry Pi through a
     secure shell. This is done by typing the below into
     the terminal:
       $ ssh pi@192.168.1.1
     4a. Provide all needed credentials upon request.

  5. Now, the user should have control of the files on the
     Raspberry Pi. Validate this.

  6. Upon establishing a successful, verified connection,
     ensure that all needed files are in the Raspberry Pi's
     home directory (the way the secure copy was given, all
     files should be located here).

  7. Run the program on the Raspberry Pi. By doing so,
     the iRobot will be recieving data from the Raspberry
     Pi (see 'SerialInterface.py' above). Do this by
     typing the following into the Raspberry Pi's terminal
     (controlled with the SSH):
       $ python Main_Project2.py
