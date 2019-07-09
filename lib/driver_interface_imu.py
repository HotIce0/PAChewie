class PACDriverInterfaceIMU:
    """
    acc: 加速度
    gyro: 陀螺仪
    angle: 角度
    magnet: 电子罗盘
    pressure: 气压
    """

    def __init__(self, driver):
        self.driver = driver

    def set_angle_zero_bias(self):
        """
        set the current ange to 0 degree as a reference
        :return:
        """
        self.driver.set_angle_zero_bias()

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

    def get_gyros(self):
        """
        Get all gyros
        (X, Y, Z)
        :return:
        """
        return self.driver.get_gyros()

    def get_acc(self):
        return self.driver.get_acc()
