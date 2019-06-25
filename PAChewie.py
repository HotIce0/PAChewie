from config import config
from lib.PA_Module_Safe import PA_Module_Safe
from lib.PA_Module_Cmd import PA_Module_Cmd
from lib.PA_Module_Sensor import PA_Module_Sensor
from lib.PA_Module_Control import PA_Module_Control


class PAChewie:
    def __init__(self):
        # get config
        num_of_channel = config['NUM_OF_CHANNEL']
        esc_config = config['ESC_CONFIG']
        esc_pin_num_arr = esc_config['PINS']

        self.num_of_channel = num_of_channel
        # ESC PWM Pin
        self.esc_pin_num_arr = esc_pin_num_arr
        # ESC PWM Duty
        self.effective_pwms = [0, 0, 0, 0]

        if len(esc_pin_num_arr) != num_of_channel:
            raise Exception("please check the config.py -> PIN_CONFIGS -> ESC_PINS: %s is right" % str(esc_pin_num_arr))
        print("vehicle info : {num_of_channel: %d, esc_pin_num_arr: %s}" % (num_of_channel, str(esc_pin_num_arr)))

        # load module
        self.module_control = PA_Module_Control()
        self.module_sensor = PA_Module_Sensor()
        self.module_safe = PA_Module_Safe()
        self.module_cmd = PA_Module_Cmd()

    def run(self):
        # pre_check
        self.module_safe.pre_check()

        # unlock
        self.module_safe.unlock()

        # recv task

        # do task
        self.module_control.test()

        while True:
            self.module_safe()
            self.module_cmd()
            self.module_sensor()
            self.module_control()
