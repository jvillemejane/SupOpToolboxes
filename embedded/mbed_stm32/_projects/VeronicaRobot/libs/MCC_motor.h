/**
 * FILENAME :        MCC_motor.h          
 *
 * DESCRIPTION :
 *       Direct Current Motor control library (with Half-Bridge).
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    13/mar/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#ifndef     __MCC_MOTOR_H_HEADER_H__
#define     __MCC_MOTOR_H_HEADER_H__

#include    "mbed.h"



/**
 * @class MCC_motor
 * @brief Class for controlling a Direct Current motor
 */
class MCC_motor{
    private:
        /// Enable pin of the Half-Bridge
        DigitalOut      *_en;
        /// Enable pin is common to different motors (true = yes)
        bool            _enGlobal;
        /// Enable boolean
        bool            _enable;
        /// Clockwise rotation pin
        PwmOut          *_D1;
        /// Anticlockwise rotation pin
        PwmOut          *_D2;
        /// PWM Period in us
        int         _period_us;
        /// PWM duty cycle value
        float       _rc;

        /// Coder used or no
        bool            _coder;
        /// Counter for the coder
        int             _cnt_coder;
        /// Counter incrementation direction.
        bool            _inc_cnt;

        /// Coder A channel input pin
        InterruptIn     *_cA;
        /// Coder B channel input pin
        InterruptIn     *_cB;
        /// tik number per tour value for CPR encoder
        int             tik_per_tour;
        /// state of the encoder
        uint8_t         _coder_new_state;
        uint8_t         _coder_old_state;
        const       uint8_t         _coder_anticlockwise[4] = {1, 3, 0, 2};
        const       uint8_t         _coder_clockwise[4] = {2, 0, 3, 1};


    public:
        /**
        * @brief Simple constructor of the MCC_motor class.
        * @details Create a MCC_motor controller for Half-Bridge
        * @param D1 clockwize pin of the motor 
        * @param D2 anticlockwize pin of the motor 
        */
        MCC_motor(PwmOut *D1, PwmOut *D2);

        /**
        * @brief Update enable pin.
        * @param en DigitalOut pin 
        * @param global true if the enable pin is common, false if not
        */
        void setEnablePin(DigitalOut *en, bool global);

        /**
        * @brief Activate the motor.
        * @details if global, activate all the motors
        */
        void setEnable(void);

        /**
        * @brief Desactivate the motor.
        * @details if global, desactivate all the motors
        */
        void setDisable(void);

        /**
        * @brief Return the status of the motor.
        * @return true if motor is enabled, else false
        */
        bool isEnabled(void);

        /**
        * @brief Stop the motor.
        */
        void stop(void);       

        /**
        * @brief Rotate the motor in the clockwise direction.
        * @param rel_speed relative speed between 0 to 1 (float)
        */
        void goForward(float rel_speed);

        /**
        * @brief Rotate the motor in the anticlockwise direction.
        * @param rel_speed relative speed between 0 to 1 (float)
        */
        void goBackward(float rel_speed);

        /**
        * @brief Rotate the motor in the good direction depending on the sign of the speed.
        * @param rel_speed relative speed between -1 to 1 (float)
        * @return true if clockwise direction, else false
        */
        bool rotate(float rel_speed);

        /**
        * @brief Set the PWM period (in us).
        * @param per_us value in us
        */
        void setPwmPeriod_us(int per_us);

        /**
        * @brief Set the coder pins for channel A and B.
        * @param cA channel A pin
        * @param cB channel B pin
        * @param inc if true counter increments in clockwise direction
        */
        void setCoderPin(InterruptIn *cA, InterruptIn *cB, bool inc = false);

        /**
        * @brief Return the value of the counter associated to the coder.
        * @return counter value
        */
        int getCoderCnt(void);

        /**
        * @brief Interrupt SubRoutine for coder event detection.
        */        
        void ISR_coder_counter(void);
};

#endif