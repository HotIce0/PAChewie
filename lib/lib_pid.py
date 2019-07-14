import time
from math import pi, isnan


class PACLibPID:
    """
    Implementation of generic PID controller.
    """
    _kp = _ki = _kd = _integrator = _imax = 0
    _last_error = _last_derivative = _last_t = 0
    _RC = 1 / (2 * pi * 20)  # low pass filter at 20Hz

    def __init__(self, p=0, i=0, d=0, imax=0, output_max=0):
        self._kp = float(p)
        self._ki = float(i)
        self._kd = float(d)
        self._imax = abs(imax)
        self._last_derivative = float('nan')
        self.output_max = output_max

    def get_pid(self, desired, current, scaler=1):
        output = 0
        error = desired - current
        tnow = time.ticks_ms()
        dt = tnow - self._last_t
        if self._last_t == 0 or dt > 1000:
            dt = 0
            self.reset_I()
        self._last_t = tnow
        dt = dt / 1000
        delta_time = float(dt) / float(1000)
        output += error * self._kp

        if abs(self._kd) > 0 and dt > 0:
            if isnan(self._last_derivative):
                derivative = 0
                self._last_derivative = 0
            else:
                derivative = (error - self._last_error) / delta_time

            derivative = self._last_derivative + \
                         ((delta_time / (self._RC + delta_time)) * (derivative - self._last_derivative))
            self._last_error = error
            self._last_derivative = derivative
            output += self._kd * derivative
        output *= scaler

        if abs(self._ki) > 0 and dt > 0:
            self._integrator += (error * self._ki) * scaler * delta_time
            if self._integrator < -self._imax:
                self._integrator = -self._imax
            elif self._integrator > self._imax:
                self._integrator = self._imax
            output += self._integrator
        if output > self.output_max:
            output = self.output_max
        return output

    def reset_I(self):
        self._integrator = 0
        self._last_derivative = float('nan')

    def update_pid_settings(self, kp, ki, kd, imax, output_max):
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._imax = imax
        self.output_max = output_max
        self.reset_I()

    def get_param(self):
        return self._kp, self._ki, self._kd, self._imax, self.output_max
    # # Use PID_MODE_DERIVATIV_NONE for a PI controller (vs PID)
    # PID_MODE_DERIVATIV_NONE = const(0)
    # # PID_MODE_DERIVATIV_CALC calculates discrete derivative from previous error, val_dot in pid_calculate() will be
    # # ignored
    # PID_MODE_DERIVATIV_CALC = const(1)
    # # PID_MODE_DERIVATIV_CALC_NO_SP calculates discrete derivative from previous value
    # # setpoint derivative will be ignored, val_dot in pid_calculate() will be ignored
    # PID_MODE_DERIVATIV_CALC_NO_SP = const(2)
    # # Use PID_MODE_DERIVATIV_SET if you have the derivative already (Gyros, Kalman)
    # PID_MODE_DERIVATIV_SET = const(3)
    #
    # SIGMA = float(0.000001)
    #
    # def __init__(self, pid_mod, dt_min=0.01):
    #     self.pid_mod = pid_mod
    #     self.dt_min = dt_min
    #     self.kp = 0.0
    #     self.ki = 0.0
    #     self.kd = 0.0
    #     self.integral = 0.0
    #     self.integral_limit = 0.0
    #     self.output_limit = 0.0
    #     self.error_previous = 0.0
    #     self.last_output = 0.0
    #     self._last_t = 0.0
    #
    # def set_param(self, kp, ki, kd, integral_limit, output_limit):
    #     self.error_previous = 0.0
    #     self.last_output = 0.0
    #     if math.isfinite(kp):
    #         self.kp = kp
    #     if math.isfinite(ki):
    #         self.ki = ki
    #     if math.isfinite(kd):
    #         self.kd = kd
    #     if math.isfinite(integral_limit):
    #         self.integral_limit = integral_limit
    #     if math.isfinite(output_limit):
    #         self.output_limit = output_limit
    #
    # def get_param(self):
    #     return self.kp, self.ki, self.kd, self.integral_limit, self.output_limit
    #
    # def calc(self, sp, val, val_dot=0):
    #     tnow = time.ticks_ms()
    #     dt = tnow - self._last_t
    #     if self._last_t == 0 or dt > 1000:
    #         dt = 0
    #         self.reset_integral()
    #     self._last_t = tnow
    #     dt = dt / 1000
    #
    #     output_limit = self.output_limit
    #     ki = self.ki
    #     kd = self.kd
    #     kp = self.kp
    #
    #     pid_mod = self.pid_mod
    #     if not math.isfinite(sp) or not math.isfinite(val) or not math.isfinite(val_dot) or not math.isfinite(dt):
    #         return self.last_output
    #
    #     # current error value
    #     error = sp - val
    #
    #     # current error derivative
    #     if pid_mod == PACLibPID.PID_MODE_DERIVATIV_CALC:
    #         d = (error - self.error_previous) / max(dt, self.dt_min)
    #         self.error_previous = error
    #     elif pid_mod == PACLibPID.PID_MODE_DERIVATIV_CALC_NO_SP:
    #         d = (-val - self.error_previous) / max(dt, self.dt_min)
    #         self.error_previous = -val
    #     elif pid_mod == PACLibPID.PID_MODE_DERIVATIV_SET:
    #         d = -val_dot
    #     else:
    #         d = 0.0
    #
    #     if not math.isfinite(d):
    #         d = 0.0
    #
    #     # calculate PD output
    #     output = (error * kp) + (d * kd)
    #
    #     if ki > PACLibPID.SIGMA:
    #         # Calculate the error integral and check for saturation
    #         i = self.integral + (error * dt)
    #
    #         # check for saturation
    #         if math.isfinite(i):
    #             if (output_limit < PACLibPID.SIGMA or (math.fabs(output + (i * ki)) <= output_limit)) \
    #                     and (math.fabs(i) <= self.integral_limit):
    #                 # not saturated, use new integral value
    #                 self.integral = i
    #
    #         # add I component to output
    #         output += self.integral * ki
    #
    #     # limit output
    #     if math.isfinite(output):
    #         if output_limit > PACLibPID.SIGMA:
    #             if output > output_limit:
    #                 output = output_limit
    #             elif output < -output_limit:
    #                 output = -output_limit
    #
    #         self.last_output = output
    #
    #     return self.last_output
    #
    # def reset_integral(self):
    #     self.integral = 0.0
