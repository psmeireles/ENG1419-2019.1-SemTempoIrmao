#include "definitions.h"
#include "modules.h"

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  String text = Serial.readString();
  text.trim();

  //button1.process();

  if (text.startsWith("countdown")) {
    int seconds = text.substring(10, 12).toInt();
    int duration = text.substring(13).toInt();
    initializeCountdown(seconds, duration);
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
  else if (text.startsWith("genius")) {
    int sequence[5];
    sequence[0] = text.substring(7,8).toInt() - 1;
    sequence[1] = text.substring(9,10).toInt() - 1;
    sequence[2] = text.substring(11,12).toInt() - 1;
    sequence[3] = text.substring(13,14).toInt() - 1;
    sequence[4] = text.substring(15, 16).toInt() - 1;
    int lightInterval = text.substring(17).toInt();
    initializeGenius(sequence, lightInterval);
  }
  

  for (int i = 0; i < processes.size(); i++) {
    Process *proc = processes.get(i);
    bool terminate = proc->action(proc);
    if (terminate) {
      processes.remove(i);
    }
  }
}
