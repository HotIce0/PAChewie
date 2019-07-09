from machine import Timer
import micropython

micropython.alloc_emergency_exception_buf(100)

time_reference_timer = None
loop500HzFlag = 0
loop500HzCnt = 0
loop200HzFlag = 0
loop200HzCnt = 0
loop100HzFlag = 0
loop100HzCnt = 0
loop50HzFlag = 0
loop50HzCnt = 0
loop20HzFlag = 0
loop20HzCnt = 0
loop10HzFlag = 0
loop10HzCnt = 0


def time_reference_callback(t):
    global loop500HzCnt, loop500HzFlag, loop200HzCnt, loop200HzFlag, loop100HzCnt, loop100HzFlag, \
        loop50HzCnt, loop50HzFlag, loop20HzCnt, loop20HzFlag, loop10HzCnt, loop10HzFlag

    loop500HzCnt += 1
    loop200HzCnt += 1
    loop100HzCnt += 1
    loop50HzCnt += 1
    loop20HzCnt += 1
    loop10HzCnt += 1

    if loop500HzCnt * 500 >= 1000:
        loop500HzFlag = 1
        loop500HzCnt = 0
    if loop200HzCnt * 200 >= 1000:
        loop200HzFlag = 1
        loop200HzCnt = 0
    if loop100HzCnt * 100 >= 1000:
        loop100HzFlag = 1
        loop100HzCnt = 0
    if loop50HzCnt * 50 >= 1000:
        loop50HzFlag = 1
        loop50HzCnt = 0
    if loop20HzCnt * 20 >= 1000:
        loop20HzFlag = 1
        loop20HzCnt = 0
    if loop10HzCnt * 10 >= 1000:
        loop10HzFlag = 1
        loop10HzCnt = 0


def init_time_reference_timer():
    """
    init time reference timer

    MODE: PERIODIC
    CYCLE : 1ms
    :return:
    """
    global time_reference_timer
    time_reference_timer = Timer(0)
    time_reference_timer.init(period=1, mode=Timer.PERIODIC, callback=time_reference_callback)


def init_timers():
    init_time_reference_timer()
