#include <Adafruit_MotorShield.h>
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor *rightMotor2 = AFMS.getMotor(1);
Adafruit_DCMotor *leftMotor2 = AFMS.getMotor(2);
Adafruit_DCMotor *rightMotor1 = AFMS.getMotor(3);
Adafruit_DCMotor *leftMotor1 = AFMS.getMotor(4);

Adafruit_DCMotor* leftMotorArray[] {leftMotor1, leftMotor2};
Adafruit_DCMotor* rightMotorArray[] {rightMotor1, rightMotor2};

float baseSpeed = 30;
float rightSpeed = baseSpeed;
float leftSpeed = baseSpeed;
//speed difference will be added to the left side and subtracted from right, + = turn right
int speedDifference = 5;

String input = "";

void setup() {
  Serial.begin(115200);
  //check coms with motor shield
  if (!AFMS.begin()) {   
    Serial.println("Failed to find motor shield");
    while (1);
  } 
}

void loop() {
  // get serial input to change parameters
  if(Serial.available()){
    input = Serial.readStringUntil('\n');
    // modify turn speed
    if (input[0] == 'd') {
      speedDifference = (input.substring(1)).toFloat();
      //adjust speed based on input
      leftSpeed = baseSpeed + speedDifference;
      rightSpeed = baseSpeed + speedDifference;
    }
    else if (input[0] == 's') {
      //modify base speed
      baseSpeed = (input.substring(1)).toFloat();
      leftSpeed = baseSpeed + speedDifference;
      rightSpeed = baseSpeed + speedDifference;
    }
    else {
      Serial.println("Invalid Input");
    }
    // output value for record
    Serial.print("got: ");
    Serial.println(input);
  }
  

  //run each motor at left or right speed respectively
  for (int motor=0; motor<sizeof(leftMotorArray); motor++){
    rightMotorArray[motor]->setSpeed(rightSpeed);
    leftMotorArray[motor]->setSpeed(leftSpeed);
    rightMotorArray[motor]->run(FORWARD);
    leftMotorArray[motor]->run(FORWARD);
  }

}
