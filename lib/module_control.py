from driver_config import driver_config
from lib.driver_interface_esc import PACDriverInterfaceESC
from lib.lib_pid import PACLibPID
import time


class PACModuleControl:
    """
    Control Module (控制模块)

    This module will integrate all sensor data to control the power system with PID cascade.(Hotice0)
    """
    def __init__(self):
        print("Control Module initializing")
        # 1. init esc interface
        esc_driver = driver_config['ESC']()
        self.esc = PACDriverInterfaceESC(esc_driver)
        # do throttle range calibration (进行行程校准)
        self.esc.trc()
        # 2. 目标状态, angle_roll 横滚x, angle_pitch 俯仰y, angle_yaw 偏航z
        self.sp_angle_roll = 0
        self.sp_angle_pitch = 0
        self.sp_angle_yaw = 0
        #
        self.angle_pid = PACLibPID(PACLibPID.PID_MODE_PID)
        self.angle_pid.set_param(0.05, 0, 0, 9999, 9999)
        print("Control Module initialization done.")
        pass

    def __call__(self, *args, **kwargs):
        self.attitude_control(module_sensor=kwargs['module_sensor'])
        pass

    def attitude_control(self, module_sensor):
        """
        attitude_control (姿态控制)
        :return:
        """
        angle_x, angle_y, angle_z = module_sensor.imu.get_angles()
        output_roll = self.angle_pid.calc(self.sp_angle_roll, angle_x)
        output_pitch = self.angle_pid.calc(self.sp_angle_pitch, angle_y)
        output_yaw = self.angle_pid.calc(self.sp_angle_yaw, angle_z)

        print("pid output==", output_roll, output_pitch, output_yaw)
        print("angle=======", angle_x, angle_y, angle_z)
        # time.sleep(0.5)
        duty_max = self.esc.get_duty_max()
        duty_min = self.esc.get_duty_min()
        duty_max = duty_max - 200

        # 1    2
        #   --
        # 3    4
        # 1,4 CW
        # 2,3 CCW
        # four axles
        pwms_val = self.esc.get_current_pwm_values()
        pwms_val[0] = pwms_val[0] + output_roll + output_pitch - output_yaw
        pwms_val[1] = pwms_val[1] - output_roll + output_pitch + output_yaw
        pwms_val[2] = pwms_val[2] + output_roll - output_pitch + output_yaw
        pwms_val[3] = pwms_val[3] - output_roll - output_pitch - output_yaw
        for i in range(0, 4):
            if pwms_val[i] > duty_max:
                pwms_val[i] = duty_max
            elif pwms_val[i] < duty_min:
                pwms_val[i] = duty_min
        # effect on esc output value
        self.esc.update_current_pwm_values(pwms_val)

    def test(self):
        print("start test")
        for pwm in self.esc.get_pwms():
            pwm.duty(int(self.esc.get_duty_min() + (self.esc.get_duty_max() - self.esc.get_duty_min()) * 0.07))
            # time.sleep(2)
            pwm.duty(self.esc.get_duty_min())
        print("finish test")
