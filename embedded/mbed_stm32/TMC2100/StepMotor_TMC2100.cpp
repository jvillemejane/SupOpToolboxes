/**
 * FILENAME :        StepMotor_TMC2100.cpp          
 *
 * DESCRIPTION :
 *       StepMotor_TMC2100 / Step Motor controller module library.
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    09/mar/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 * @see https://learn.watterott.com/silentstepstick/pinconfig/tmc2100/
 */

 #include "StepMotor_TMC2100.h"

 StepMotor_TMC2100::StepMotor_TMC2100(DigitalOut *en, DigitalOut *dir, PwmOut *step, bool config){
    this->_enable = false;
    /* Initialisation of enable output */
    if (en){ delete __en; }
    __en=en;
    this->__en->write(1);
    /* Initialisation of direction output */
    if (dir){ delete __dir; }
    __dir=dir;
    this->__dir->write(0);
    /* Initialisation of step output */
    if (step){ delete __step; }
    __step=step;
    this->__step->period(1);
    this->__step->write(0);
    this->_notConfig = config;
    thread_sleep_for(10);      // 10 ms
 }

void StepMotor_TMC2100::updateMotorState(void){
    this->__dir->write(this->_direction);
    this->__step->period(1.0/this->_frequency);
    if(this->_enable){
        this->__step->write(0.5);
        this->__en->write(0);
    }
    else{
        this->__step->write(0);
        this->__en->write(1);
    }
}

void StepMotor_TMC2100::goForward(float stepsPerSeconds){
    this->_direction = 1;
    this->_enable = true;
    this->_frequency = stepsPerSeconds;
    this->updateMotorState();
}

void StepMotor_TMC2100::goBackward(float stepsPerSeconds){
    this->_direction = 0;
    this->_enable = true;
    this->_frequency = stepsPerSeconds;
    this->updateMotorState();  
}

void StepMotor_TMC2100::stop(void){
    this->_enable = false;
    this->updateMotorState();  
}
