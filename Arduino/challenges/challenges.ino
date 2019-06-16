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

	for(int i = 0; i < processes.size(); i++) {
		Process *proc = processes.get(i);
		bool terminate = proc->action(proc);
		if(terminate){
			processes.remove(i);
		}
	}
}