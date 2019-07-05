#include "modules.h"
#include "definitions.h"
#include <Math.h>
#include <Ultrasonic.h>
#include <stdio.h>

#define PIN_A 5
#define PIN_B 2.5
#define PIN_C 0


Ultrasonic ultrasonic(US_TRIGGER_PIN, US_ECHO_PIN);

Process *countdown;

int countdownLastPrint;
int lightLastPrint;
float distLastPrint;
unsigned long lastHit = 0;

void hit() { // This function will be called each time the player fails a challenge
  if(millis() - lastHit > 250){
    Serial.println("hit");
    lastHit = millis(); 
  }
}

bool processCountdown(Process *proc) {
  unsigned long now = millis();

  if (proc->duration != -1 && (now - proc->startTime) / 1000 >= proc->duration) {
    // Process is over
    Serial.println("finished countdown");
    return true;
  }

  if ((now - proc->lastInteraction) / 1000 > proc->interval) {
    proc->lastInteraction = now;
    Serial.println("lost countdown");
    return true;
  }


  int t = proc->interval - (now - proc->lastInteraction) / 1000;

  if(t != countdownLastPrint){
    tft.setCursor(TFT_COUNT_X, TFT_COUNT_Y);
    tft.fillRect(TFT_COUNT_X + 120, TFT_COUNT_Y, 100, 20, TFT_BLACK);
    tft.setTextColor(TFT_WHITE);
    tft.print("Countdown: " + String(t));
    countdownLastPrint = t;
  }
  
  return false;
}

void resetCountdown(JKSButton &botaoPressionado){
  countdown->lastInteraction = millis();
}

void initializeCountdown(int seconds, int duration) {
  Process *countdownProc = (Process*) malloc(sizeof(Process));
  countdownProc->startTime = millis();
  countdownProc->lastInteraction = countdownProc->startTime;
  countdownProc->interval = seconds;
  countdownProc->duration = duration;
  countdownProc->action = processCountdown;
  processes.add(countdownProc);
  countdown = countdownProc;
  button.setPressHandler(resetCountdown);
  countdownLastPrint = 0;
}

bool processWires(Process *proc) {
  unsigned long now = millis();

  if (proc->duration != -1 && (now - proc->startTime) / 1000 >= proc->duration) {
    // Process is over
    bool result = checkWires(proc);
    if (result) {
      Serial.println("finished wires");
    }
    else {
      Serial.println("lost wires");
      lastHit = millis(); 
    }
    return true;
  }

  if (digitalRead(WIRES_BTN) == HIGH) {
    bool result = checkWires(proc);
    if (result) {
      Serial.println("finished wires");
      return true;
    }
    else {
      hit();
    }
  }

  return false;
}

bool checkWires(Process *proc) {
  float pinReads[] = {analogRead(WIRES_1) * 5 / 1024.0, analogRead(WIRES_2) * 5 / 1024.0, analogRead(WIRES_3) * 5 / 1024.0};
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

void initializeWires(int pinA, int pinB, int pinC) {
  Process *wiresProc = (Process*) malloc(sizeof(Process));
  wiresProc->startTime = millis();
  wiresProc->lastInteraction = wiresProc->startTime;
  wiresProc->interval = -1;
  wiresProc->duration = -1;
  wiresProc->params = (int *) malloc(3 * sizeof(int));
  wiresProc->params[0] = pinA;
  wiresProc->params[1] = pinB;
  wiresProc->params[2] = pinC;
  wiresProc->action = processWires;
  processes.add(wiresProc);
}

bool processDistance(Process *proc) {
  unsigned long now = millis();

  float distance = ultrasonic.read();

  if(((int)distance) != ((int)distLastPrint)){
    tft.setCursor(TFT_DIST_X, TFT_DIST_Y);
    tft.fillRect(TFT_DIST_X + 110, TFT_DIST_Y, 100, 120, TFT_BLACK);
    tft.setTextColor(TFT_WHITE);
    tft.print("Distance: " + String(distance)); 
    distLastPrint = distance;
  }
  
  // 5 seconds tolerance to start checking
  if (proc->startTime < now) {
    if (distance > proc->params[1] || distance < proc->params[0]) {
      Serial.println("lost distance");
      lastHit = millis(); 
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
  distLastPrint = 0;
}


bool processLight(Process *proc) {
  unsigned long now = millis();

  int lightValue = analogRead(LIGHT_PIN);

  if(abs(lightValue - lightLastPrint) >= 5){
    tft.setCursor(TFT_LIGHT_X, TFT_LIGHT_Y);
    tft.fillRect(TFT_LIGHT_X + 80, TFT_LIGHT_Y, 100, 30, TFT_BLACK);
    tft.setTextColor(TFT_WHITE);
    tft.print("Light: " + String(analogRead(LIGHT_PIN)));
    lightLastPrint = lightValue;
  }
  
  // 5 seconds tolerance to start checking
  if (proc->startTime < now) {
    if (lightValue > proc->params[1] || lightValue < proc->params[0]) {
      Serial.println("lost light");
      lastHit = millis(); 
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
  lightLastPrint = 0;
}

bool processGenius(Process *proc) {
  unsigned long now = millis();
  int colors[3] = {LED_R, LED_Y, LED_G};

  // Blinking LEDS
  if (((now - proc->startTime)) % proc->interval < 10 && proc->params[6] != 6) {
    int ledIndex = proc->params[6];
    digitalWrite(colors[0], LOW);
    digitalWrite(colors[1], LOW);
    digitalWrite(colors[2], LOW);
    if(proc->params[6] != 5)
      digitalWrite(colors[proc->params[ledIndex]], HIGH);
    //Serial.println("Acendeu o " + String(colors[proc->params[ledIndex]]));
    proc->params[6]++; 
  }

  //Checking buttons
  if((now - proc->startTime) > 5*proc->interval && (now - proc->lastInteraction) >= 500){
    int btnR = digitalRead(BTN_R);
    int btnY = digitalRead(BTN_Y);
    int btnG = digitalRead(BTN_G);

    int currIndex = proc->params[5];

    
    if (btnR == HIGH){
      proc->lastInteraction = millis();
      if (proc->params[currIndex] == 0){
        proc->params[5]++;
      }
      else{
        proc->params[5] = 0;
        proc->params[6] = 0; 
        proc->startTime = millis();
        hit();
      }
    }
    else if (btnY == HIGH){
      proc->lastInteraction = millis();
      if (proc->params[currIndex] == 1){
        proc->params[5]++;
      }
      else{
        proc->params[5] = 0;
        proc->params[6] = 0; 
        proc->startTime = millis();
        hit();
      }
    }
    else if (btnG == HIGH){
      proc->lastInteraction = millis();
      if (proc->params[currIndex] == 2){
        proc->params[5]++;
      }
      else{
        proc->params[5] = 0;
        proc->params[6] = 0; 
        proc->startTime = millis();
        hit();
      }
    }
  }

  if(proc->params[5] == 5){
    Serial.println("finished genius");
    return true;
  }
  return false;
}

void initializeGenius(int sequence[5], int lightInterval) {
  Process *geniusProc = (Process*) malloc(sizeof(Process));
  geniusProc->startTime = millis();
  geniusProc->lastInteraction = geniusProc->startTime;
  geniusProc->interval = lightInterval;
  geniusProc->duration = -1;
  geniusProc->params = (int *) malloc(7 * sizeof(int));
  geniusProc->params[0] = sequence[0];
  geniusProc->params[1] = sequence[1];
  geniusProc->params[2] = sequence[2];
  geniusProc->params[3] = sequence[3];
  geniusProc->params[4] = sequence[4];
  geniusProc->params[5] = 0;  // Current button to be pressed
  geniusProc->params[6] = 0;  // Current LED to blink
  geniusProc->action = processGenius;
  processes.add(geniusProc);
}
