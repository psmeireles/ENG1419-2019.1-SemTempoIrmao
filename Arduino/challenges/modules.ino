#include "modules.h"
#include "definitions.h"

void hit(){ // This function will be called each time the player fails a challenge
    Serial.println("hit");
}

bool processCountdown(Process *proc){
    unsigned long now = millis();
    
    if(proc->duration != -1 && (now - proc->startTime) / 1000 >= proc->duration){
        // Process is over
        return true;
    }

    if((now - proc->lastInteraction) / 1000 >= proc->interval){
        proc->lastInteraction = now;
        hit();
        return true;
    }
    else if(digitalRead(A1) == HIGH){
        proc->lastInteraction = now;
    }

    return false;
}


void initializeCountdown(int seconds, int duration){
    Process *countdownProc = (Process*) malloc(sizeof(Process));
    countdownProc->startTime = millis();
    countdownProc->lastInteraction = countdownProc->startTime;
    countdownProc->interval = seconds;
    countdownProc->duration = -1;
    countdownProc->action = processCountdown;
    processes.add(countdownProc);
}