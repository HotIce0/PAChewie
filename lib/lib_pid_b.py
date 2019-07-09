from micropython import const
import math


class PACLibPID:
    PID_MODE_PID = const(0)

    def __init__(self, pid_mode):
        self.pid_mod = pid_mode
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.integral = 0.0
        self.integral_limit = 0.0
        self.output_limit = 0.0
        self.error_previous = 0.0
        self.last_output = 0.0

    def set_param(self, kp, ki, kd, integral_limit, output_limit):
        if math.isfinite(kp):
            self.kp = kp
        if math.isfinite(ki):
            self.ki = ki
        if math.isfinite(kd):
            self.kd = kd
        if math.isfinite(integral_limit):
            self.integral_limit = integral_limit
        if math.isfinite(output_limit):
            self.output_limit = output_limit

    def reset_integral(self):
        self.integral = 0.0

    def calc(self, sp, val):
        """
        calculate PID value
        :param sp:
        :param val:
        :return:
        """
        output_limit = self.output_limit
        ki = self.ki
        kd = self.kd
        kp = self.kp
        pid_mod = self.pid_mod

        # validate parameter
        if not math.isfinite(sp) or not math.isfinite(val):
            return self.last_output

        # P current error value
        error = sp - val

        # D current error derivative
        if pid_mod == PACLibPID.PID_MODE_PID:
            d = error - self.error_previous
            self.error_previous = error
        else:
            d = 0.0

        if not math.isfinite(d):
            d = 0.0

        # calculate PD output
        output = (error * kp) + (d * kd)
        # I
        i = self.integral + error
        if math.isfinite(i):
            # validate saturation
            if (math.fabs(output + (i * ki)) <= output_limit) and (math.fabs(i) <= self.integral_limit):
                self.integral = i

        output += self.integral * ki

        # limit output
        if math.isfinite(output):
            if output > output_limit:
                output = output_limit
            elif output < -output_limit:
                output = -output_limit

            self.last_output = output

        return self.last_output
