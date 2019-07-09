from config import config
from lib.module_safe import PACModuleSafe
from lib.module_cmd import PACModuleCmd
from lib.module_sensor import PACModuleSensor
from lib.module_control import PACModuleControl
from lib.module_station import PACModuleStation
import timer
import _thread


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
        self.module_control = PACModuleControl()
        self.module_sensor = PACModuleSensor()
        self.module_safe = PACModuleSafe()
        self.module_cmd = PACModuleCmd()
        # station module
        self.module_sation = PACModuleStation(self)

    def run(self):
        # pre_check
        self.module_safe.pre_check()

        # unlock
        self.module_safe.unlock()

        # recv task

        # do task
        self.module_control.test()

        while True:

            # self.module_safe()
            # self.module_cmd()
            if timer.loop100HzFlag:
                timer.loop100HzFlag = 0

                self.module_sensor()

            if timer.loop200HzFlag:
                timer.loop200HzFlag = 0

                self.module_control(module_sensor=self.module_sensor)


