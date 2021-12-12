#include <Adafruit_MotorShield.h>
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

//setup motors
Adafruit_DCMotor *rightMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *leftMotor1 = AFMS.getMotor(2);
Adafruit_DCMotor *backMotor1 = AFMS.getMotor(3);
Adafruit_DCMotor* leftMotorArray[] {leftMotor1};
Adafruit_DCMotor* rightMotorArray[] {rightMotor1};

//define base speeds
float baseSpeed = 255;
float rightSpeed = baseSpeed;
float leftSpeed = baseSpeed;
float backSpeed = baseSpeed;
//error will be added to the left side and subtracted from right, + = turn right
int error = 0;
float errorMultiplier = .45;

String input = "";

void setup() {
  //start serial
  Serial.begin(115200);
  //check coms with motor shield
  if (!AFMS.begin()) {   
    Serial.println("Failed to find motor shield");
    while (1);
  } 
}

void loop() {
  // get serial input to change parameters
  if(Serial.available() > 0){
    input = Serial.readStringUntil('\n');
    // modify turn speed
    if (input[0] == 'e') {
      error = (input.substring(1)).toFloat();
      //adjust speed based on input
      if (error != 0){
        leftSpeed = baseSpeed + baseCorrection - (error*errorMultiplier);
        rightSpeed = baseSpeed + (error*errorMultiplier);
        backSpeed = baseSpeed;
      }
      //stop robot if error exactly 0
      else{
        leftSpeed = 0;
        rightSpeed = 0;
        backSpeed = 0;
      }

    }
    else if (input[0] == 's') {
      //modify base speed
      baseSpeed = (input.substring(1)).toFloat();
      leftSpeed = baseSpeed - (error*errorMultiplier);
      rightSpeed = baseSpeed + (error*errorMultiplier);
      backSpeed = baseSpeed;
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

  //run back motor at base speed
  backMotor1->setSpeed(-1*255);
  backMotor1->run(FORWARD);

}
