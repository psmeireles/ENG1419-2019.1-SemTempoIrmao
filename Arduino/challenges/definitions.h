#ifndef _DEFINITIONS_H
#define _DEFINITIONS_H

#include <LinkedList.h>
#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h> 

#define LIGHT_PIN A14
#define US_ECHO_PIN 41
#define US_TRIGGER_PIN 39
#define WIRES_BTN 51
#define WIRES_1 A8
#define WIRES_2 A9
#define WIRES_3 A10
#define LED_R 34
#define LED_Y 36
#define LED_G 38
#define BTN_R 42
#define BTN_Y 44
#define BTN_G 46


#define TFT_COUNT_X 20
#define TFT_COUNT_Y 150
#define TFT_DIST_X 20
#define TFT_DIST_Y 200
#define TFT_LIGHT_X 20
#define TFT_LIGHT_Y 250



struct Process{
    unsigned long startTime;
    unsigned long lastInteraction;
    int interval; // -1 for non periodic processes
    int duration; // -1 for processes that last until the game ends
    int *params;
    bool (*action)(Process *proc); // Returns true if process is over
};

LinkedList<Process*> processes;
TouchScreen touch(6, A1, A2, 7, 300); 
MCUFRIEND_kbv tft;
JKSButton button; 

#endif
