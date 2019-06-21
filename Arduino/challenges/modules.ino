#include "modules.h"
#include "definitions.h"
#include <Math.h>
#include <Ultrasonic.h>

#define PIN_A 5
#define PIN_B 2.5
#define PIN_C 0

#define PTRIGGER 4
#define PECHO 5

int lightSensor = A0;

Ultrasonic ultrasonic(PTRIGGER, PECHO);



void hit() { // This function will be called each time the player fails a challenge
  Serial.println("hit");
}

bool processCountdown(Process *proc) {
  unsigned long now = millis();

  if (proc->duration != -1 && (now - proc->startTime) / 1000 >= proc->duration) {
    // Process is over
    return true;
  }

  if ((now - proc->lastInteraction) / 1000 >= proc->interval) {
    proc->lastInteraction = now;
    hit();
    return true;
  }
  else if (digitalRead(A1) == LOW) {
    proc->lastInteraction = now;
  }

  return false;
}


void initializeCountdown(int seconds, int duration) {
  Process *countdownProc = (Process*) malloc(sizeof(Process));
  countdownProc->startTime = millis();
  countdownProc->lastInteraction = countdownProc->startTime;
  countdownProc->interval = seconds;
  countdownProc->duration = -1;
  countdownProc->action = processCountdown;
  processes.add(countdownProc);
}

bool processWires(Process *proc) {
  unsigned long now = millis();

  if (proc->duration != -1 && (now - proc->startTime) / 1000 >= proc->duration) {
    // Process is over
    bool result = checkWires(proc);
    if (result) {
      Serial.print("finished wires");
    }
    else {
      hit();
    }
    return true;
  }

  if (digitalRead(A3) == LOW) {
    bool result = checkWires(proc);
    if (result) {
      Serial.print("finished wires");
      return true;
    }
    else {
      hit();
    }
  }

  return false;
}

bool checkWires(Process *proc) {
  float pinReads[] = {analogRead(A8) * 5 / 1024.0, analogRead(A9) * 5 / 1024.0, analogRead(A10) * 5 / 1024.0};
  int pinA = proc->params[0];
  int pinB = proc->params[1];
  int pinC = proc->params[2];

  if (abs(pinReads[pinA - 1] - PIN_A) < 1.5
      && abs(pinReads[pinB - 1] - PIN_B) < 1.5
      && abs(pinReads[pinC - 1] - PIN_C) < 1.5) {
    return true;
  }

  return false;
}

void initializeWires(int pinA, int pinB, int pinC, int duration) {
  Process *wiresProc = (Process*) malloc(sizeof(Process));
  wiresProc->startTime = millis();
  wiresProc->lastInteraction = wiresProc->startTime;
  wiresProc->interval = -1;
  wiresProc->duration = duration;
  wiresProc->params = (int *) malloc(3 * sizeof(int));
  wiresProc->params[0] = pinA;
  wiresProc->params[1] = pinB;
  wiresProc->params[2] = pinC;
  wiresProc->action = processWires;
  processes.add(wiresProc);
}

bool processDistance(Process *proc) {
  unsigned long now = millis();

  // 5 seconds tolerance to start checking
  if (proc->startTime < now) {
    float cmMsec;
    cmMsec = ultrasonic.read();
    if (cmMsec > proc->params[1] || cmMsec < proc->params[0]) {
      hit();
      return true;
    }
  }
  else {
    return false;
  }

  if (proc->duration != -1 && (now - proc->startTime) / 1000 >= proc->duration) {
    Serial.println("finished distance");
    return true;
  }

  return false;
}

void initializeDistance(int minDist, int maxDist, int duration) {
  Process *distProc = (Process*) malloc(sizeof(Process));
  distProc->startTime = millis() + 5000;
  distProc->lastInteraction = distProc->startTime;
  distProc->interval = -1;
  distProc->duration = duration;
  distProc->params = (int *) malloc(2 * sizeof(int));
  distProc->params[0] = minDist;
  distProc->params[1] = maxDist;
  distProc->action = processDistance;
  processes.add(distProc);
}


bool processLight(Process *proc) {
  unsigned long now = millis();

  // 5 seconds tolerance to start checking
  if (proc->startTime < now) {
    int lightValue = analogRead(lightSensor);
    if (lightValue > proc->params[1] || lightValue < proc->params[0]) {
      hit();
      return true;
    }
  }
  else {
    return false;
  }

  if (proc->duration != -1 && (now - proc->startTime) / 1000 >= proc->duration) {
    Serial.println("finished light");
    return true;
  }

  return false;
}

void initializeLight(int minLight, int maxLight, int duration) {
  Process *lightProc = (Process*) malloc(sizeof(Process));
  lightProc->startTime = millis() + 5000;
  lightProc->lastInteraction = lightProc->startTime;
  lightProc->interval = -1;
  lightProc->duration = duration;
  lightProc->params = (int *) malloc(2 * sizeof(int));
  lightProc->params[0] = minLight;
  lightProc->params[1] = maxLight;
  lightProc->action = processLight;
  processes.add(lightProc);
}
