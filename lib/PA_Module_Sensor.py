from lib.PA_DriverInterface_IMU import PA_DriverInterface_IMU
from driver_config import driver_config


class PA_Module_Sensor:
    def __init__(self):
        imu_driver = driver_config['IMU']()
        self.imu = PA_DriverInterface_IMU(imu_driver)

    def __call__(self, *args, **kwargs):
        """
        Update sensor data
        :param args:
        :param kwargs:
        :return:
        """
        self.imu.update()
