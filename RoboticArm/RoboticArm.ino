#include <Servo.h>

Servo GripServo;
Servo AngleServo;
Servo PanServo;
Servo LRServo;

int speed = 5;

int GPin = 9;
int APin = 10;
int PPin = 11;
int LRPin = 6;

// int AVal;  // We Dont actually need AVal, as the value of the AngleServo Should match the value of the PanServo, for the claw to remain parrallel to the base.
int PVal=90;
int LRVal=90;

int LR = 0; // = -1,0,1
int Pan = 0; // = -1,0,1
int Grip = 1; // = 0,1

void setup() {
  // initializing the serial connection
  Serial.begin(115200);
  // attaching all the servos
  GripServo.attach(GPin);
  AngleServo.attach(APin);
  PanServo.attach(PPin);
  LRServo.attach(LRPin);

  for(int i = 0; i <= 90; i = i + 2){
     PanServo.write(i);
     delay(20);
   }
   for(int i = 50; i <= 90; i = i + 2){
     LRServo.write(i);
     delay(20);
   }

  GripServo.write(0);

  for(int i = 0; i < 180; i = i++){
     GripServo.write(i);
     delay(5);
   }
  for(int i = 180; i > 0; i = i--){
     GripServo.write(i);
     delay(5);
   }
}

void loop() {

  while(Serial.available() == 0){
  }

  LR = Serial.readStringUntil(':').toInt();
  Pan = Serial.readStringUntil(':').toInt();
  Grip = Serial.readStringUntil('\r').toInt();

  if(LR != 0){
      if(LR == 1){
        LRVal = LRVal + speed;
      }
      else LRVal = LRVal - speed;
      LRVal = constrain(LRVal,0,180);
      LRServo.write(LRVal);
  }
  if(Pan != 0){
    if(Pan == 1){
        PVal = PVal + speed;
      }
      else PVal = PVal - speed;
    PVal = constrain(PVal,0,180);
    PanServo.write(PVal);
    AngleServo.write(PVal);
  }

  int Grip_Val = map(Grip,0,1,0,180);
  GripServo.write(Grip_Val);
}