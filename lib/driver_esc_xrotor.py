"""
ESC (Electronic Speed Control) Driver For XRotor (40A test OK)
"""
from machine import PWM
from machine import Pin
import time
from config import config


class PACDriverESCXRotor:
    def __init__(self, freq=500, duty_max=1023, duty_min=400):
        pins_num = config['ESC_CONFIG']['PINS']
        self.pins = []
        self.number_of_axles = config['NUM_OF_CHANNEL']
        self.freq = freq
        self.duty_max = duty_max
        self.duty_min = duty_min
        self.pwms = []
        # create Pin objects
        for i in pins_num:
            self.pins.append(Pin(i))
        # init PWM with Pin objects
        for i in range(0, self.number_of_axles):
            self.pwms.append(PWM(self.pins[i], freq=freq, duty=0))

    def trc(self):
        """ Throttle Range Calibration """
        number_of_axles = self.number_of_axles
        freq = self.freq
        duty_max = self.duty_max
        duty_min = self.duty_min

        print("calibrating throttle range <param: freq=%d, duty_max=%d, duty_min=%d>" % (freq, duty_max, duty_min))
        pwms_val_temp = []
        for i in range(0, number_of_axles):
            pwms_val_temp.append(duty_max)
        self.update_current_pwm_values(pwms_val_temp)
        time.sleep(3)
        for i in range(0, number_of_axles):
            pwms_val_temp[i] = duty_min
        self.update_current_pwm_values(pwms_val_temp)
        time.sleep(3)
        print("throttle range calibration done")

    def esc_programing(self):
        """ ESC Programming """
        pass

    def get_duty_max(self):
        """ Get MAX_DUTY """
        return self.duty_max

    def get_duty_min(self):
        """ Get MIN_DUTY """
        return self.duty_min

    def get_pwms(self):
        """ Get the PWM objects : machine.PWM """
        return self.pwms

    def update_current_pwm_values(self, pwms_val):
        """

        :param pwms_val:
        :return:
        """
        number_of_axles = self.number_of_axles
        duty_max = self.duty_max
        duty_min = self.duty_min
        pwms = self.pwms
        # update self pwms_val and limit with duty_max, duty_min
        for i in range(0, number_of_axles):
            if pwms_val[i] > duty_max:
                pwms_val[i] = duty_max
            elif pwms_val[i] < duty_min:
                pwms_val[i] = duty_min

        # write pwms_val to output
        for i in range(0, number_of_axles):
            pwms[i].duty(int(pwms_val[i]))
