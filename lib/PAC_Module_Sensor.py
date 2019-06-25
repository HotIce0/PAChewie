from lib.PAC_DriverInterface_IMU import PAC_DriverInterface_IMU
from driver_config import driver_config


class PAC_Module_Sensor:
    def __init__(self):
        print("Sensor Module initializing")
        imu_driver = driver_config['IMU']()
        self.imu = PAC_DriverInterface_IMU(imu_driver)
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
