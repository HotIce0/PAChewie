from driver_config import driver_config
from lib.PAC_DriverInterface_ESC import PAC_DriverInterface_ESC
from lib.PAC_LIB_PID import PAC_LIB_PID
import time


class PAC_Module_Control:
    """
    Control Module (控制模块)

    This module will integrate all sensor data to control the power system with PID cascade.(Hotice0)
    """
    def __init__(self):
        print("Control Module initializing")
        # 1. init esc interface
        esc_driver = driver_config['ESC']()
        self.esc = PAC_DriverInterface_ESC(esc_driver)
        # do throttle range calibration (进行行程校准)
        # self.esc.trc()
        # 2. 目标状态, angle_roll 横滚x, angle_pitch 俯仰y, angle_yaw 偏航z
        self.sp_angle_roll = 180
        self.sp_angle_pitch = -9
        self.sp_angle_yaw = -87
        #
        self.angle_pid = PAC_LIB_PID(PAC_LIB_PID.PID_MODE_PID)
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
        pass
        # angle_x, angle_y, angle_z = module_sensor.imu.get_angles()
        # output_roll = self.angle_pid.calc(self.sp_angle_roll, angle_x)
        # output_pitch = self.angle_pid.calc(self.sp_angle_pitch, angle_y)
        # output_yaw = self.angle_pid.calc(self.sp_angle_yaw, angle_z)

        # print("pid output==", output_roll, output_pitch, output_yaw)

    def test(self):
        print("start test")
        for pwm in self.esc.get_pwms():
            pwm.duty(int(self.esc.get_duty_min() + (self.esc.get_duty_max() - self.esc.get_duty_min()) * 0.07))
            # time.sleep(2)
            pwm.duty(self.esc.get_duty_min())
        print("finish test")
