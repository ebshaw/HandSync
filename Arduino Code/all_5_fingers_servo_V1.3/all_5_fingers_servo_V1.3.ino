// I include the Servo library because it handles the servo control signal for me.
#include <Servo.h>


// These are the five servo objects.
// Each object represents one physical servo motor.
Servo thumbServo;
Servo pointerServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;


// These are the pins each servo signal wire is connected to.
int thumbPin = 5;
int pointerPin = 7;
int middlePin = 6;
int ringPin = 4;
int pinkyPin = 3;


// These store the current angle of each servo.
// I start them all at 0 because my mechanical setup starts open at 0 degrees.
int thumbPos = 0;
int pointerPos = 0;
int middlePos = 0;
int ringPos = 0;
int pinkyPos = 0;


// These store where each servo is trying to go.
// The important idea is that commands only change the target, not the servo instantly.
int thumbTarget = 0;
int pointerTarget = 0;
int middleTarget = 0;
int ringTarget = 0;
int pinkyTarget = 0;


// This controls how many degrees each servo moves per update.
// Smaller number means smoother and slower motion.
int stepSize = 1;


// This controls how much time passes between each movement update.
// Bigger number means slower servo motion.
int moveDelay = 5;


// This stores the last time I moved the servos.
// I use this instead of delay() so the Arduino does not get stuck.
unsigned long lastMoveTime = 0;


void setup() {

  // I attach each servo object to the pin its signal wire is plugged into.
  thumbServo.attach(thumbPin);
  pointerServo.attach(pointerPin);
  middleServo.attach(middlePin);
  ringServo.attach(ringPin);
  pinkyServo.attach(pinkyPin);

  // I start serial communication so Arduino can receive messages from Python.
  Serial.begin(9600);

  // I reduce how long Arduino waits when reading a serial command.
  // This helps keep the servo motion responsive.
  Serial.setTimeout(5);

  // I physically send all servos to their open starting position.
  thumbServo.write(0);
  pointerServo.write(0);
  middleServo.write(0);
  ringServo.write(0);
  pinkyServo.write(0);
}


void loop() {

  // This checks if Python has sent any command over USB.
  if (Serial.available() > 0) {

    // This reads one full command until it reaches the newline character.
    String command = Serial.readStringUntil('\n');

    // This removes hidden spaces or carriage returns from the command.
    command.trim();


    // If Python says the thumb is down, I set the thumb target to 180.
    if (command == "THUMB_DOWN") {
      thumbTarget = 180;
    }

    // If Python says the thumb is up, I set the thumb target back to 0.
    else if (command == "THUMB_UP") {
      thumbTarget = 0;
    }

    // If Python says the pointer is down, I set the pointer target to 180.
    else if (command == "POINTER_DOWN") {
      pointerTarget = 180;
    }

    // If Python says the pointer is up, I set the pointer target back to 0.
    else if (command == "POINTER_UP") {
      pointerTarget = 0;
    }

    // If Python says the middle finger is down, I set the middle target to 180.
    else if (command == "MIDDLE_DOWN") {
      middleTarget = 180;
    }

    // If Python says the middle finger is up, I set the middle target back to 0.
    else if (command == "MIDDLE_UP") {
      middleTarget = 0;
    }

    // If Python says the ring finger is down, I set the ring target to 180.
    else if (command == "RING_DOWN") {
      ringTarget = 180;
    }

    // If Python says the ring finger is up, I set the ring target back to 0.
    else if (command == "RING_UP") {
      ringTarget = 0;
    }

    // If Python says the pinky is down, I set the pinky target to 180.
    else if (command == "PINKY_DOWN") {
      pinkyTarget = 180;
    }

    // If Python says the pinky is up, I set the pinky target back to 0.
    else if (command == "PINKY_UP") {
      pinkyTarget = 0;
    }
  }


  // This checks whether enough time has passed to move the servos one small step.
  // I use millis() instead of delay() so Arduino can keep reading new commands.
  if (millis() - lastMoveTime >= moveDelay) {

    // I update the last movement time.
    lastMoveTime = millis();

    // Each servo moves one small step toward its own target.
    // This is what makes the motion simultaneous and interruptible.
    moveServoTowardTarget(thumbServo, thumbPos, thumbTarget);
    moveServoTowardTarget(pointerServo, pointerPos, pointerTarget);
    moveServoTowardTarget(middleServo, middlePos, middleTarget);
    moveServoTowardTarget(ringServo, ringPos, ringTarget);
    moveServoTowardTarget(pinkyServo, pinkyPos, pinkyTarget);
  }
}


// This function moves one servo a little bit toward its target.
// I use a function so I do not have to repeat the same movement logic five times.
void moveServoTowardTarget(Servo &servo, int &currentPos, int targetPos) {

  // If the servo is below its target, I move it upward by stepSize.
  if (currentPos < targetPos) {

    // This increases the current position.
    currentPos = currentPos + stepSize;

    // This prevents the servo from overshooting the target.
    if (currentPos > targetPos) {
      currentPos = targetPos;
    }

    // This sends the updated angle to the physical servo.
    servo.write(currentPos);
  }

  // If the servo is above its target, I move it downward by stepSize.
  else if (currentPos > targetPos) {

    // This decreases the current position.
    currentPos = currentPos - stepSize;

    // This prevents the servo from going below the target.
    if (currentPos < targetPos) {
      currentPos = targetPos;
    }

    // This sends the updated angle to the physical servo.
    servo.write(currentPos);
  }
}