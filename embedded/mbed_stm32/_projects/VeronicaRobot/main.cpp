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
    sprintf(charStr, "CNT2 = %d.\r\nCNT3 = %d.\r\n\n", my_mcc2.getCoderCnt(), my_mcc3.getCoderCnt());
    my_pc.write(charStr, strlen(charStr));    
}

/// control
bool        controlEnable = true;
float       rc_setpoint = 0;
float       rc_gain = 1/100.0;
float       display_gain = 1/1000.0;
Ticker      controlTik;
AnalogOut   controlError(A2);

/// Proportional - Integral - Derivative digital controller 
void        ISR_controlSpeed(void){
    int     error;              /// Proportional
    int     error_o = error;    /// Integral - old value of the error
    error = my_mcc3.getCoderCnt()-my_mcc2.getCoderCnt();
    /// Displaying on A2
    float   errorF = 0.5 + error * display_gain;
    controlError.write(errorF);

    /// Gain control
    float rc3 = rc_setpoint;
    float rc2 = rc_setpoint + error * rc_gain;
    //if(rc2 < 0.5) rc2 = 0.5;
    //if(rc2 > 1.0) rc2 = 1.0;

    /// Outputs update
    if(controlEnable){
        my_mcc2.rotate(rc2);
        my_mcc3.rotate(rc3);
    }

}


// MAIN FUNCTION
int main()
{
    my_pc.baud(115200);
    sprintf(charStr, "Mbed OS %d.%d.%d.\r\n", MBED_MAJOR_VERSION, MBED_MINOR_VERSION, MBED_PATCH_VERSION);
    my_pc.write(charStr, strlen(charStr));

    //testConversion();
    //initNRF24(2450);

    my_mcc2.setEnablePin(&Mx_en, true);
    my_mcc2.setCoderPin(&M2_A, &M2_B);
    my_mcc3.setCoderPin(&M3_B, &M3_A);

    displayTik.attach(&ISR_displayCnt, 500ms);
    controlTik.attach(&ISR_controlSpeed, 20ms);

    my_mcc2.setEnable();

    while (true)
    {
        /// Test basics function
        /*
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
        */

        /// Test advanced functions
        /*
        my_mcc2.rotate(-0.7);
        my_mcc3.rotate(-0.7);
        */

        /// Test loop control
        thread_sleep_for(WAIT_TIME_MS);

        /// Sensors
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
