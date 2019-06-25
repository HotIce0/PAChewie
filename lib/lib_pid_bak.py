from micropython import const
import math


class PACLibPID:
    """
    Implementation of generic PID controller.
    """
    # Use PID_MODE_DERIVATIV_NONE for a PI controller (vs PID)
    PID_MODE_DERIVATIV_NONE = const(0)
    # PID_MODE_DERIVATIV_CALC calculates discrete derivative from previous error, val_dot in pid_calculate() will be
    # ignored
    PID_MODE_DERIVATIV_CALC = const(1)
    # PID_MODE_DERIVATIV_CALC_NO_SP calculates discrete derivative from previous value
    # setpoint derivative will be ignored, val_dot in pid_calculate() will be ignored
    PID_MODE_DERIVATIV_CALC_NO_SP = const(2)
    # Use PID_MODE_DERIVATIV_SET if you have the derivative already (Gyros, Kalman)
    PID_MODE_DERIVATIV_SET = const(3)

    SIGMA = const(float(0.000001))

    def __init__(self, pid_mod, dt_min):
        self.pid_mod = pid_mod
        self.dt_min = dt_min
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.integral = 0.0
        self.integral_limit = 0.0
        self.output_limit = 0.0
        self.error_previous = 0.0
        self.last_output = 0.0

    def set_parameters(self, kp, ki, kd, integral_limit, output_limit):
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

    def calculate(self, sp, val, val_dot, dt):
        output_limit = self.output_limit
        ki = self.ki
        kd = self.kd
        kp = self.kp

        pid_mod = self.pid_mod
        if not math.isfinite(sp) or not math.isfinite(val) or not math.isfinite(val_dot) or not math.isfinite(dt):
            return self.last_output

        # current error value
        error = sp - val

        # current error derivative
        if pid_mod == PACLibPID.PID_MODE_DERIVATIV_CALC:
            d = (error - self.error_previous) / max(dt, self.dt_min)
            self.error_previous = error
        elif pid_mod == PACLibPID.PID_MODE_DERIVATIV_CALC_NO_SP:
            d = (-val - self.error_previous) / max(dt, self.dt_min)
            self.error_previous = -val
        elif pid_mod == PACLibPID.PID_MODE_DERIVATIV_SET:
            d = -val_dot
        else:
            d = 0.0

        if not math.isfinite(d):
            d = 0.0

        # calculate PD output
        output = (error * kp) + (d * kd)

        if ki > PACLibPID.SIGMA:
            # Calculate the error integral and check for saturation
            i = self.integral + (error * dt)

            # check for saturation
            if math.isfinite(i):
                if (output_limit < PACLibPID.SIGMA or (math.fabs(output + (i * ki)) <= output_limit)) \
                        and (math.fabs(i) <= self.integral_limit):
                    # not saturated, use new integral value
                    self.integral = i

            # add I component to output
            output += self.integral * ki

        # limit output
        if math.isfinite(output):
            if output_limit > PACLibPID.SIGMA:
                if output > output_limit:
                    output = output_limit
                elif output < -output_limit:
                    output = -output_limit

            self.last_output = output

        return self.last_output

    def reset_integral(self):
        self.integral = 0.0
