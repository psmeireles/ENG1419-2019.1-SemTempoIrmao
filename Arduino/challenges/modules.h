#ifndef _MODULES_H
#define _MODULES_H

bool processCountdown(Process *proc);
void initializeCountdown(int seconds, int duration);
bool processWires(Process *proc);
void initializeWires(int pinA, int pinB, int pinC, int duration);
bool processDistance(Process *proc);
void initializeDistance(int minDist, int maxDist, int duration);

#endif
