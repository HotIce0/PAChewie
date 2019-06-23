"""
ESC (Electronic Speed Control) Driver For XRotor (40A test OK)
"""
from machine import PWM
import time


class PA_Driver_ESC_XRotor:
    def __init__(self, pins, freq=500, duty_max=1023, duty_min=400):
        self.pins = pins
        self.number_of_axles = len(pins)
        self.freq = freq
        self.duty_max = duty_max
        self.duty_min = duty_min
        self.pwms = []

    def trc(self):
        """ Throttle Range Calibration """
        pins = self.pins
        number_of_axles = self.number_of_axles
        freq = self.freq
        duty_max = self.duty_max
        duty_min = self.duty_min
        pwms = self.pwms

        print("calibrating throttle range <param: freq=%d, duty_max=%d, duty_min=%d>" % (freq, duty_max, duty_min))
        for i in range(0, number_of_axles):
            pwms.append(PWM(pins[i], freq=freq, duty=duty_max))
        time.sleep(3)
        for i in range(0, number_of_axles):
            pwms[i].duty(duty_min)
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
