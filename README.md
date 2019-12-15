## Robotic Applications and Design 
---
This repository houses projects using the iRobot Create2 in Robotic Applications and Design at the University of South Carolina.
All projects are written in Python and reference the [iRobot Interface Spec](https://www.irobotweb.com/~/media/MainSite/PDFs/About/STEM/Create/iRobot_Roomba_600_Open_Interface_Spec.pdf?la=en).

### Project_One
[The robot](https://drive.google.com/file/d/1qV1KdgdLvN7GdSB7fDuzNeR2KqT55yui/view) drives around a regular polygon of N sides. The number of sides of this polygon could change, for all valid inputs of
side numbers. The program works in conjunction with two interfaces and a main function to produce this desired result.

### Project_Two
[The robot](https://drive.google.com/file/d/17pS6uIGC5stqJetbmv9jQ1DKY17KgW3i/view) reads and interprets its sensors. The goal of project two was to implement the “random move” function for a roomba. To accomplish this, the ability to read the Create2’s bump, wheel drop, and cliff sensors were added to the polygon's interface. In our main function, a single thread that calls each sensor reading method was created. A limitation of the Create2 is that it can only return data from its sensors in 15 ms intervals. This approach worked around this limitation.

### Project_Three
[The robot](https://drive.google.com/file/d/1RzoDoG3izRddcIuEF-j1B52c0YjJthWL/view) implements a PD controller to demonstrate a wall-following behavior. This was done using an infrared (IR) sensor on the right side of the robot. The robot was
intended to read the IR sensor value as it was driving alongside a barricade, to be able to appropriately “follow” the barricade at an appropriate distance. When a turn in the barricade is sensed, the iRobot uses its PD control logic to adjust its direction.

### Project_Four
[The robot](https://drive.google.com/file/d/1EhvBXYeJgKimL22GS0Wtsyu0TkXgzaNn/view) finds its docking station to charge. The robot initally moves using wall-following behavior; then, once the robot is in range of its dock, the robot will begin the movement towards the dock. 

### Credits
This course, Robotic Applications and Design, was taught by [Marios Xanthidis](https://sites.google.com/view/mariosx).

The Group for this project included Robby Carff, Miles Ziemer, and Austin Staton.
