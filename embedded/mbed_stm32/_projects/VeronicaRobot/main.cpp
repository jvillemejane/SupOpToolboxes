/**
 * FILENAME :        main.cpp          
 *
 * DESCRIPTION :
 *       Robot 2 wheels / with Temp and Hum sensors.
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    13/mar/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#include "mbed.h"
#include "main_lib.h"

// MCC Motor
DigitalOut  Mx_en(PB_3);
PwmOut      M2_D1(PB_14);
PwmOut      M2_D2(PB_13);
InterruptIn M2_A(PB_2);
InterruptIn M2_B(PB_1);

PwmOut      M3_D1(PC_9);
PwmOut      M3_D2(PB_8);
InterruptIn M3_A(PB_4);
InterruptIn M3_B(PB_10);

MCC_motor   my_mcc2(&M2_D1, &M2_D2);
MCC_motor   my_mcc3(&M3_D1, &M3_D2);

/// Debugging display
Ticker      displayTik;
void        ISR_displayCnt(void){
    sprintf(charStr, "CNT = %d.\r\n", my_mcc2.getCoderCnt());
    my_pc.write(charStr, strlen(charStr));    
}

/// control
bool        controlEnable = false;
float       rc_setpoint = 0.7;
float       rc_gain = 1/1000.0;
Ticker      controlTik;
AnalogOut   controlError(A2);
void        ISR_controlSpeed(void){
    int     error = my_mcc2.getCoderCnt()-my_mcc3.getCoderCnt();
    float   errorF = 0.5 + error * rc_gain;
    /// Displaying on A2
    controlError.write(errorF);

    /// Gain control
    float rc3 = rc_setpoint;
    float rc2 = rc_setpoint + errorF * rc_gain;
    if(rc2 < 0.5) rc2 = 0.5;
    if(rc2 > 1.0) rc2 = 1.0;

    if(controlEnable){
        my_mcc2.rotate(rc2);
        my_mcc2.rotate(rc3);
    }

}


// MAIN FUNCTION
int main()
{
    my_pc.baud(115200);
    sprintf(charStr, "Mbed OS %d.%d.%d.\r\n", MBED_MAJOR_VERSION, MBED_MINOR_VERSION, MBED_PATCH_VERSION);
    my_pc.write(charStr, strlen(charStr));

    //testConversion();
    initNRF24(2450);

    my_mcc2.setEnablePin(&Mx_en, true);
    my_mcc2.setCoderPin(&M2_A, &M2_B);
    my_mcc3.setCoderPin(&M3_A, &M3_B);

    displayTik.attach(&ISR_displayCnt, 200ms);
    controlTik.attach(&ISR_controlSpeed, 20ms);

    while (true)
    {
        my_mcc2.goForward(0.7);
        my_mcc3.goForward(0.7);
        thread_sleep_for(3*WAIT_TIME_MS);
        my_mcc2.stop();
        my_mcc3.stop();
        thread_sleep_for(2*WAIT_TIME_MS);
        my_mcc2.goBackward(0.5);
        my_mcc3.goBackward(0.5);
        thread_sleep_for(4*WAIT_TIME_MS);
        my_mcc2.stop();
        my_mcc3.stop();
        thread_sleep_for(3*WAIT_TIME_MS);
        /*
        my_sensor.readTRH(&temperature, &humidity);
        sprintf(charStr, "%f degres\r\n", temperature);
        my_pc.write(charStr, strlen(charStr));
        
        my_sensor.floatToBytes(&temperature, (uint8_t *)dataToSend);
        transmitNRF24(dataToSend);
        uint8_t  nb_data = receiveNRF24(dataReceived);
        sprintf(charStr, "nb_data = %d\r\n", nb_data);
        my_pc.write(charStr, strlen(charStr));
        if(nb_data != 0){
            temperatureI2C = my_sensor.bytesToFloat((uint8_t *)dataReceived);
            sprintf(charStr, "New Temp = %f\r\n", temperatureI2C);
            my_pc.write(charStr, strlen(charStr));

        }
        thread_sleep_for(WAIT_TIME_MS);
        */
    }
}
