/**
 * FILENAME :        StepMotor_TMC2100.h          
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

// TODO : 
//      - setVref
//      - setPinConfig
//      - setConfig

#ifndef __STEP_MOTOR_TMC2100_HEADER_H__
#define __STEP_MOTOR_TMC2100_HEADER_H__

#include <cstdint>
#include <mbed.h>
 
/** Constant definition */
#define     DEBUG_MODE                  1

/**
 * @class StepMotor_TMC2100
 * @brief Control a step motor with a TMC2100 module from MikroE
 */
class StepMotor_TMC2100{
     private:
        /// Step by step Frequency
        float       _frequency;
        /// Direction of the Step Motor
        uint8_t     _direction;
        /// Enable the Step Motor
        bool        _enable;
        /// Configuration Enabling of TMC2100
        bool        _notConfig;

        /// interface to TMC2100 pins 
        DigitalOut  *__en; 
        DigitalOut  *__dir;
        PwmOut      *__step;
        DigitalOut  *__cfg1;
        DigitalOut  *__cfg2;
        DigitalOut  *__cfg3;

    public:
        /**
        * @brief Simple constructor of the StepMotor_TMC2100 class.
        * @details Create a StepMotor_TMC2100 object with
        *    an enable pin (Digital)
        *    a direction pin (Digital)
        *    a step pin (Pwm)
        * @param en enable pin of the TMC2100 module
        * @param dir direction pin of the TMC2100 module 
        * @param step step pin of the TMC2100 module
        * @param config true if TMC2100 is configurable, false if not
        */
        StepMotor_TMC2100(DigitalOut *en, DigitalOut *dir, PwmOut *step, bool config);

        /**
        * @brief Update the state of the motor.
        */
        void updateMotorState(void);

        /**
        * @brief Rotation of the motor in the clockwise direction.
        * @param stepsPerSeconds Speed in steps per seconds
        */
        void goForward(float stepsPerSeconds);

        /**
        * @brief Rotation of the motor in the anticlockwise direction.
        * @param stepsPerSeconds Speed in steps per seconds
        */        
        void goBackward(float stepsPerSeconds);

        /**
        * @brief Stop the motor.
        */
        void stop(void);

};

#endif