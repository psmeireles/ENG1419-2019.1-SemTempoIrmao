#ifndef _DEFINITIONS_H
#define _DEFINITIONS_H

#include <LinkedList.h>

struct Process{
    unsigned long startTime;
    unsigned long lastInteraction;
    int interval;
    int duration; // -1 for processes that last until the game ends
    bool (*action)(Process *proc); // Returns true if process is over
};

LinkedList<Process*> processes;


#endif