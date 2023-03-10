/**
 * FILENAME :        main_StepMotor_TMC2100.cpp          
 *
 * DESCRIPTION :
 *       StepMotor_TMC2100 / Program for testing Step Motor controller module library.
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    09/mar/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 * @see https://learn.watterott.com/silentstepstick/pinconfig/tmc2100/
 */

#include "mbed.h"
#include <string.h>
#include "StepMotor_TMC2100.h"

#define WAIT_TIME_MS 500
UnbufferedSerial    my_pc(USBTX, USBRX);
char            charStr[128];

// Step Motor 1
DigitalOut      en(PB_13);
DigitalOut      dir(PB_3);
PwmOut          step(PA_10);
StepMotor_TMC2100   my_motor(&en, &dir, &step, false);
DigitalOut      M1_CFG1(PB_14);
DigitalOut      M1_CFG2(PB_15);

int main()
{
    sprintf(charStr, "Mbed OS %d.%d.%d.\n", MBED_MAJOR_VERSION, MBED_MINOR_VERSION, MBED_PATCH_VERSION);
    my_pc.write(charStr, strlen(charStr));

    // 1/4 step
    M1_CFG1 = 0;
    M1_CFG2 = 1;

    while (true)
    {
        my_motor.goForward(1200);
        thread_sleep_for(5000);      // 1 s
        my_motor.stop();
        thread_sleep_for(1000);      // 1 s
        my_motor.goBackward(1600);
        thread_sleep_for(5000);      // 1 s
        my_motor.stop();
        thread_sleep_for(1000);      // 1 s
    }
}
