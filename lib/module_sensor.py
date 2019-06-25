from lib.driver_interface_imu import PACDriverInterfaceIMU
from driver_config import driver_config


class PACModuleSensor:
    def __init__(self):
        print("Sensor Module initializing")
        imu_driver = driver_config['IMU']()
        self.imu = PACDriverInterfaceIMU(imu_driver)
        self.imu.set_angle_zero_bias()
        print("Sensor Module initialization done.")

    def __call__(self, *args, **kwargs):
        """
        Update sensor data
        :param args:
        :param kwargs:
        :return:
        """
        self.imu.update()
