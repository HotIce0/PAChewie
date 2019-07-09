from driver_config import driver_config
from lib.driver_interface_esc import PACDriverInterfaceESC
from lib.lib_pid import PACLibPID
from lib.lib_delta_time import PACLibDeltaTime
from lib import lib_config_operate
import time
from lib.module_debug import write_to_file


class PACModuleControl:
    """
    Control Module (控制模块)

    This module will integrate all sensor data to control the power system with PID cascade.(Hotice0)
    """

    def __init__(self):
        # Read PID config
        config_pid = lib_config_operate.read_config_json_obj("pid.json")
        print("Control Module initializing")
        self.lib_delta_time = PACLibDeltaTime()
        # 1. init esc interface
        esc_driver = driver_config['ESC']()
        self.esc = PACDriverInterfaceESC(esc_driver)
        # DEBUG ======== START
        self.esc.update_current_pwm_values([400, 400, 400, 400])  # after trc was done.
        # DEBUG ======== END
        # do throttle range calibration (进行行程校准)
        # self.esc.trc()
        time.sleep(1)
        # 2. target status(目标状态) : angle_roll 横滚x, angle_pitch 俯仰y, angle_yaw 偏航z
        self.sp_angle_roll = 0
        self.sp_angle_pitch = 0
        self.sp_angle_yaw = 0

        self.sp_gyros_roll = 5
        self.sp_gyros_pitch = 5
        self.sp_gyros_yaw = 5
        # Init PID calc obj
        angle_roll_pid_config = config_pid['ANGLE_ROLL']
        angle_pitch_pid_config = config_pid['ANGLE_PITCH']
        angle_yaw_pid_config = config_pid['ANGLE_YAW']
        gyros_roll_pid_config = config_pid['GYROS_ROLL']
        gyros_pitch_pid_config = config_pid['GYROS_PITCH']
        gyros_yaw_pid_config = config_pid['GYROS_YAW']

        # Roll
        self.angle_roll_pid = PACLibPID(PACLibPID.PID_MODE_DERIVATIV_CALC)
        self.angle_roll_pid.set_param(
            angle_roll_pid_config[0],
            angle_roll_pid_config[1],
            angle_roll_pid_config[2],
            angle_roll_pid_config[3],
            angle_roll_pid_config[4]
        )
        # Pitch
        self.angle_pitch_pid = PACLibPID(PACLibPID.PID_MODE_DERIVATIV_CALC)
        self.angle_pitch_pid.set_param(
            angle_pitch_pid_config[0],
            angle_pitch_pid_config[1],
            angle_pitch_pid_config[2],
            angle_pitch_pid_config[3],
            angle_pitch_pid_config[4]
        )
        # Yaw
        self.angle_yaw_pid = PACLibPID(PACLibPID.PID_MODE_DERIVATIV_CALC)
        self.angle_yaw_pid.set_param(
            angle_yaw_pid_config[0],
            angle_yaw_pid_config[1],
            angle_yaw_pid_config[2],
            angle_yaw_pid_config[3],
            angle_yaw_pid_config[4]
        )
        # 0.85
        self.gyros_roll_pid = PACLibPID(PACLibPID.PID_MODE_DERIVATIV_CALC)
        self.gyros_roll_pid.set_param(
            gyros_roll_pid_config[0],
            gyros_roll_pid_config[1],
            gyros_roll_pid_config[2],
            gyros_roll_pid_config[3],
            gyros_roll_pid_config[4]
        )

        self.gyros_pitch_pid = PACLibPID(PACLibPID.PID_MODE_DERIVATIV_CALC)
        self.gyros_pitch_pid.set_param(
            gyros_pitch_pid_config[0],
            gyros_pitch_pid_config[1],
            gyros_pitch_pid_config[2],
            gyros_pitch_pid_config[3],
            gyros_pitch_pid_config[4]
        )

        self.gyros_yaw_pid = PACLibPID(PACLibPID.PID_MODE_DERIVATIV_CALC)
        self.gyros_yaw_pid.set_param(
            gyros_yaw_pid_config[0],
            gyros_yaw_pid_config[1],
            gyros_yaw_pid_config[2],
            gyros_yaw_pid_config[3],
            gyros_yaw_pid_config[4]
        )

        print("Control Module initialization done.")
        pass

    def __call__(self, *args, **kwargs):
        delta_time = self.lib_delta_time.get_diff()
        self.attitude_control(module_sensor=kwargs['module_sensor'], delta_time=delta_time)
        self.lib_delta_time.update()
        pass

    def attitude_control(self, module_sensor, delta_time):
        """
        attitude_control (姿态控制)
        :return:
        """
        # print("delta_time ", delta_time)
        # get angle data from sensor
        angle_x, angle_y, angle_z = module_sensor.imu.get_angles()
        print(angle_x, angle_y, angle_z)
        # get gyros data from sensor
        gyros_x, gyros_y, gyros_z = module_sensor.imu.get_gyros()

        # control of angle
        # outer
        angle_pid_output_roll = self.angle_roll_pid.calc(self.sp_angle_roll, angle_x, delta_time)
        angle_pid_output_pitch = self.angle_pitch_pid.calc(self.sp_angle_pitch, angle_y, delta_time)
        angle_pid_output_yaw = self.angle_yaw_pid.calc(self.sp_angle_yaw, angle_z, delta_time)

        print("angle pid output==", angle_pid_output_roll, angle_pid_output_pitch, angle_pid_output_yaw)
        # inner
        gyros_pid_output_roll = self.gyros_roll_pid.calc(angle_pid_output_roll, gyros_x, delta_time)
        gyros_pid_output_pitch = self.gyros_pitch_pid.calc(angle_pid_output_pitch, gyros_y, delta_time)
        gyros_pid_output_yaw = self.gyros_yaw_pid.calc(self.sp_gyros_yaw, gyros_z, delta_time)

        print("gyros pid output==", gyros_pid_output_roll, gyros_pid_output_pitch, gyros_pid_output_yaw)

        # print("angle=======", angle_x, angle_y, angle_z)
        # time.sleep(0.5)
        duty_max = self.esc.get_duty_max()
        duty_min = self.esc.get_duty_min()

        duty_mid = (duty_max + duty_min) / 2

        # 1    2
        #   --
        # 3    4
        # 1,4 CW
        # 2,3 CCW
        # four axles
        pwms_val = [0, 0, 0, 0]
        pwms_val[0] = duty_mid + gyros_pid_output_roll + gyros_pid_output_pitch - gyros_pid_output_yaw
        pwms_val[1] = duty_mid - gyros_pid_output_roll + gyros_pid_output_pitch + gyros_pid_output_yaw
        pwms_val[2] = duty_mid + gyros_pid_output_roll - gyros_pid_output_pitch + gyros_pid_output_yaw
        pwms_val[3] = duty_mid - gyros_pid_output_roll - gyros_pid_output_pitch - gyros_pid_output_yaw
        for i in range(0, 4):
            if pwms_val[i] > duty_max:
                pwms_val[i] = duty_max
            elif pwms_val[i] < duty_min:
                pwms_val[i] = duty_min
        print("pwms output : ", pwms_val[0], pwms_val[1], pwms_val[2], pwms_val[3])
        # DEBUG ===== START
        write_to_file(
            "/sd/pid.txt",
            str(delta_time) + "," +
            str(gyros_pid_output_roll) + "," +
            str(gyros_pid_output_pitch) + "," +
            str(gyros_pid_output_yaw) + "," +
            str(pwms_val[0]) + "," +
            str(pwms_val[1]) + "," +
            str(pwms_val[2]) + "," +
            str(pwms_val[3])
        )
        # DEBUG ===== END
        # effect on esc output value
        self.esc.update_current_pwm_values(pwms_val)

    def test(self):
        print("start test")
        for pwm in self.esc.get_pwms():
            pwm.duty(int(self.esc.get_duty_min() + (self.esc.get_duty_max() - self.esc.get_duty_min()) * 0.07))
            # time.sleep(2)
            pwm.duty(self.esc.get_duty_min())
        print("finish test")
