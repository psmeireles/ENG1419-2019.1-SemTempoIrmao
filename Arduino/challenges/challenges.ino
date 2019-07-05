#include "definitions.h"
#include "modules.h"

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(20);
  pinMode(LED_R, OUTPUT);
  pinMode(LED_Y, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  tft.begin( tft.readID() );
  tft.fillScreen(TFT_BLACK);
  button.init(&tft, &touch, 120, 70, 200, 100, TFT_WHITE, TFT_RED,
TFT_WHITE, "Start", 2);
  button.setPressHandler(startGame);
}



void loop() {
  String text = Serial.readString();
  text.trim();

  button.process();

  if(!text.equals("end") && !text.equals("")){
    tone(BUZZER, 750, BUZZER_TIME);
  }
  
  if (text.startsWith("countdown")) {
    int seconds = text.substring(10, 12).toInt();
    int duration = text.substring(13).toInt();
    initializeCountdown(seconds, duration);
  }
  else if (text.startsWith("wires")) {
    int pinA = text.substring(6, 7).toInt();
    int pinB = text.substring(8, 9).toInt();
    int pinC = text.substring(10).toInt();
    initializeWires(pinA, pinB, pinC);
  }
  else if (text.startsWith("distance")) {
    int minDist = text.substring(9, 11).toInt();
    int maxDist = text.substring(12, 14).toInt();
    int duration = text.substring(15).toInt();
    initializeDistance(minDist, maxDist, duration);
  }
  else if (text.startsWith("light")) {
    int minLight = text.substring(6, 10).toInt();
    int maxLight = text.substring(11, 15).toInt();
    int duration = text.substring(16).toInt();
    initializeLight(minLight, maxLight, duration);
  }
  else if (text.startsWith("genius")) {
    int sequence[5];
    sequence[0] = text.substring(7, 8).toInt() - 1;
    sequence[1] = text.substring(9, 10).toInt() - 1;
    sequence[2] = text.substring(11, 12).toInt() - 1;
    sequence[3] = text.substring(13, 14).toInt() - 1;
    sequence[4] = text.substring(15, 16).toInt() - 1;
    int lightInterval = text.substring(17).toInt();
    initializeGenius(sequence, lightInterval);
  }
  else if(text.startsWith("end")){
    processes.clear();
    tft.fillScreen(TFT_BLACK);
    button.init(&tft, &touch, 120, 70, 200, 100, TFT_WHITE, TFT_RED,
  TFT_WHITE, "Start", 2);
    button.setPressHandler(startGame);
  }


  for (int i = 0; i < processes.size(); i++) {
    Process *proc = processes.get(i);
    bool terminate = proc->action(proc);
    if (terminate) {
      processes.remove(i);
      free(proc);
    }
  }
}

void startGame(){
  Serial.println("start");
  tft.fillScreen(TFT_BLACK);
  button.init(&tft, &touch, 120, 70, 200, 100, TFT_WHITE, TFT_RED,
TFT_WHITE, "Countdown", 2);
  button.setPressHandler(NULL);
  tft.setTextSize(2);
  tft.setTextColor(TFT_WHITE);
  tft.setCursor(TFT_COUNT_X, TFT_COUNT_Y);
  tft.print("Countdown:");
  tft.setCursor(TFT_LIGHT_X, TFT_LIGHT_Y);
  tft.print("Light:");
  tft.setCursor(TFT_DIST_X, TFT_DIST_Y);
  tft.print("Distance:");
}
