# Strandbeest
## Vision tracking and control code for differential drive strandbeest

This project contains the software to control a small dog sized powered strandbeest. 

### Vision Input

There are two separate methods in which the strandbeest operates - tracking a color target and tracking a person. In either case, the code will identify the target of choice in frame, and calculate the offset of the target from the center of the frame. This value is sent over serial to interact with the arduino code. 

One difference in operation between color tracking and person tracking - if a person is not found in frame, the code will send a halt signal to the arduino. Alternatively if the color target is lost, no signal is sent to the arduino, causing the beest to continue in the same direction as it was prior. 

### Arduino Control

The arduino software powers the beest at a constant forward speed unless given input over serial. Upon being given an offset value, the right and left motor speeds are updated by adding and subtracting respectively the offset multiplied by a scalar value. The motors are powered at these speeds until new input is given. 

### Dependencies

Adafruit Motor Shield V2 Library
Opencv - using 4.5.3
