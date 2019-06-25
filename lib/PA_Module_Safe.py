"""Safe Module

"""


class PA_Module_Safe:
    def __init__(self):
        print("Safe Module initializing")
        # 未处于飞行状态才可以上锁, 默认启动时处于上锁状态
        self.lock = True
        self.pre_check_finish = False
        #
        print("Safe Module initialization done.")
        pass

    def __call__(self, *args, **kwargs):
        pass

    def pre_check(self):
        """
        Do complete check before takeoff
        :param sensor:
        :return:
        """
        print("do pre check...")
        # 传感器检查
        # sensor.pre_check()
        # 电压检查

        # 参数检查

        # 电机，油门检查

        self.pre_check_finish = True
        print("check done.")
        pass

    def unlock(self):
        if not self.pre_check_finish:
            raise Exception("pre check not finished")
        self.lock = False

    def is_lock(self):
        return self.lock
