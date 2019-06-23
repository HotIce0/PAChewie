from driver_config import driver_config
from lib.PA_DriverInterface_ESC import PA_DriverInterface_ESC
import time


class PA_Module_Control:
    def __init__(self):
        esc_driver = driver_config['ESC']()
        self.esc = PA_DriverInterface_ESC(esc_driver)
        self.esc.trc()
        pass

    def __call__(self, *args, **kwargs):
        pass

    def test(self):
        print("start test")
        for pwm in self.esc.get_pwms():
            pwm.duty(int((self.esc.get_duty_max() - self.esc.get_duty_min()) * 0.07))
            time.sleep(2)
            pwm.duty(self.esc.get_duty_min())
        print("finish test")
