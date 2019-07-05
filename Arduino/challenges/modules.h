#ifndef _MODULES_H
#define _MODULES_H

void initializeCountdown(int seconds, int duration);
void initializeWires(int pinA, int pinB, int pinC);
void initializeDistance(int minDist, int maxDist, int duration);
void initializeLight(int minLight, int maxLight, int duration);
void initializeGenius(int sequence[5], int lightInterval);

#endif
