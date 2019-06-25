from config import config
from lib.PAC_Module_Safe import PAC_Module_Safe
from lib.PAC_Module_Cmd import PAC_Module_Cmd
from lib.PAC_Module_Sensor import PAC_Module_Sensor
from lib.PAC_Module_Control import PAC_Module_Control


class PAChewie:
    def __init__(self):
        # get config
        num_of_channel = config['NUM_OF_CHANNEL']
        esc_config = config['ESC_CONFIG']
        esc_pin_num_arr = esc_config['PINS']

        self.num_of_channel = num_of_channel

        if len(esc_pin_num_arr) != num_of_channel:
            raise Exception("please check the config.py -> PIN_CONFIGS -> ESC_PINS: %s is right" % str(esc_pin_num_arr))
        print("vehicle info : {num_of_channel: %d, esc_pin_num_arr: %s}" % (num_of_channel, str(esc_pin_num_arr)))

        # load module
        self.module_control = PAC_Module_Control()
        self.module_sensor = PAC_Module_Sensor()
        self.module_safe = PAC_Module_Safe()
        self.module_cmd = PAC_Module_Cmd()

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
            self.module_control(module_sensor=self.module_sensor)
