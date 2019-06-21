#include "definitions.h"
#include "modules.h"

// void button1Pressed() {
// 	Serial.println("Timer restarted!");
// 	Timer1.restart();
// }

// void timerExpired() {
// 	Serial.println("BOOM!");
// 	Timer1.stop();
// }

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(A1, INPUT);
  pinMode(A3, INPUT);
  pinMode(A8, INPUT);
  pinMode(A9, INPUT);
  pinMode(A10, INPUT);
}

void loop() {
  String text = Serial.readString();
  text.trim();

  //button1.process();

  if (text.startsWith("countdown")) {
    int seconds = text.substring(10).toInt();
    Serial.println("Initializing countdown! " + String(seconds) + " seconds");
    initializeCountdown(seconds, -1);
  }
  else if (text.startsWith("wires")) {
    int pinA = text.substring(6,7).toInt();
    int pinB = text.substring(8,9).toInt();
    int pinC = text.substring(10,11).toInt();
    int duration = text.substring(12,14).toInt();
    initializeWires(pinA, pinB, pinC, duration);
  }
  else if (text.startsWith("distance")) {
    int minDist = text.substring(9,11).toInt();
    int maxDist = text.substring(12,14).toInt();
    int duration = text.substring(15).toInt();
    initializeDistance(minDist, maxDist, duration);
  }
  else if (text.startsWith("light")) {
    int minLight = text.substring(6,10).toInt();
    int maxLight = text.substring(11,15).toInt();
    int duration = text.substring(16).toInt();
    initializeLight(minLight, maxLight, duration);
  }
  

  for (int i = 0; i < processes.size(); i++) {
    Process *proc = processes.get(i);
    bool terminate = proc->action(proc);
    if (terminate) {
      processes.remove(i);
    }
  }
}
