from config import config
from PA_Module_Safe import PA_Module_Safe
from PA_Module_Cmd import PA_Module_Cmd
from  PA_Module_Sensor import PA_Module_Sensor


class PyAutopilot:
    def __init__(self):
        pin_configs = config['PIN_CONFIGS']
        num_of_channel = config['NUM_OF_CHANNEL']
        esc_pin_num_arr = pin_configs['PIN_CONFIGS']

        self.num_of_channel = num_of_channel
        # ESC PWM Pin
        self.esc_pin_num_arr = esc_pin_num_arr
        # ESC PWM Duty
        self.effective_pwms = [0, 0, 0, 0]

        if len(esc_pin_num_arr) != num_of_channel:
            raise Exception("please check the config.py -> PIN_CONFIGS -> ESC_PINS: %s is right" % str(esc_pin_num_arr))
        print("vehicle info : {num_of_channel: %d, esc_pin_num_arr: %s}" % (num_of_channel, str(esc_pin_num_arr)))

        # load all module
        self.module_safe = PA_Module_Safe()
        self.module_cmd = PA_Module_Cmd()
        self.module_sensor = PA_Module_Sensor()

        self.run()
        pass

    def run(self):
        # pre_check
        self.module_safe.pre_check(self.module_sensor)

        # unlock
        self.module_safe.unlock()


