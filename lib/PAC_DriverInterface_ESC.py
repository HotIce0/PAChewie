"""动力模块
ESC (Electronic Speed Control)

The ESC Driver must implement below function

trc()
esc_programing()
get_duty_max()
get_duty_min()
get_pwms()

"""


class PAC_DriverInterface_ESC:
    """
    ESC (Electronic Speed Control) is used to init, config, control (speed) the motor.
    (电调模块被用于初始化，配置，控制(转速) 电机)
    """
    def __init__(self, driver):
        self.driver = driver

    def trc(self):
        """ Throttle Range Calibration (行程校准) """
        self.driver.trc()

    def esc_programing(self):
        """ ESC Programming (ESC配置编程) """
        self.driver.esc_programing()

    def get_duty_max(self):
        """ Get MAX_DUTY (获取空占比最大值) """
        return self.driver.get_duty_max()

    def get_duty_min(self):
        """ Get MIN_DUTY (获取空占比最小值) """
        return self.driver.get_duty_min()

    def get_pwms(self):
        """ Get the list of PWM objects : machine.PWM (获取PWM对象列表) """
        return self.driver.get_pwms()

    def get_current_pwm_values(self):
        """
        Get current PWM values

        return value like (400, 400, 400, 400)
        :return:
        """
        return self.driver.get_current_pwm_values()

    def update_current_pwm_values(self, pwms_val):
        """
        Update current PWM values

        1. save pwms_val (and limit with max_output_value, min_output_value)
        2. write pwms_val to output
        :return:
        """
        return self.driver.update_current_pwm_values(pwms_val)
