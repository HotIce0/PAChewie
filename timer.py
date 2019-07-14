from machine import Timer


flag_attitude_ctrl = False
flag_imu_update = False


def callback_attitude_ctrl(t):
    global flag_attitude_ctrl
    flag_attitude_ctrl = True


def callback_imu_update(t):
    global flag_imu_update
    flag_imu_update = True


def init_timers():
    timer_attitude_ctrl = Timer(1)
    timer_attitude_ctrl.init(period=50, mode=Timer.PERIODIC, callback=callback_attitude_ctrl)
    timer_imu_update = Timer(2)
    timer_imu_update.init(period=200, mode=Timer.PERIODIC, callback=callback_imu_update)
