#include <GFButton.h>
#include <TimerOne.h>

GFButton button1(A1);

void button1Pressed(){
    Serial.println("Timer restarted!");
    Timer1.restart();
}

void timerExpired(){
    Serial.println("BOOM!");
    Timer1.stop();
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  
}

void loop() {
  String text = Serial.readString();
  text.trim();

  button1.process();

    if(text.startsWith("countdown")){
        int seconds = text.substring(10).toInt();
        Serial.println("Initiating countdown! " + String(seconds) + " seconds");
        Timer1.initialize(seconds * 1000000);
        Timer1.attachInterrupt(timerExpired); 
        button1.setPressHandler(button1Pressed);
    }
}