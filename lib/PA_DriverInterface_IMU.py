class PA_DriverInterface_IMU:
    """
    acc: 加速度
    gyro: 陀螺仪
    angle: 角度
    magnet: 电子罗盘
    pressure: 气压
    """

    def __init__(self, driver):
        self.driver = driver

    def update(self):
        """
        Update sensor data
        :return:
        """
        self.driver.update()

    def get_angles(self):
        """
        Get all angle
        (X, Y ,Z)
        :return:
        """
        return self.driver.get_angles()
