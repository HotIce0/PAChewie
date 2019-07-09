import ustruct
from machine import UART
from config import config
import time
from lib.lib_retry import retry


class PACDriverIMUJY901B:
    """

    printf("Time:20%d-%d-%d %d:%d:%.3f\r\n",(short)JY901.stcTime.ucYear,(short)JY901.stcTime.ucMonth,(short)JY901.stcTime.ucDay,(short)JY901.stcTime.ucHour,(short)JY901.stcTime.ucMinute,(float)JY901.stcTime.ucSecond+(float)JY901.stcTime.usMiliSecond/1000);
    printf("Acc:%.3f %.3f %.3f\r\n",(float)JY901.stcAcc.a[0]/32768*16,(float)JY901.stcAcc.a[1]/32768*16,(float)JY901.stcAcc.a[2]/32768*16);
    printf("Gyro:%.3f %.3f %.3f\r\n",(float)JY901.stcGyro.w[0]/32768*2000,(float)JY901.stcGyro.w[1]/32768*2000,(float)JY901.stcGyro.w[2]/32768*2000);
    printf("Angle:%.3f %.3f %.3f\r\n",(float)JY901.stcAngle.Angle[0]/32768*180,(float)JY901.stcAngle.Angle[1]/32768*180,(float)JY901.stcAngle.Angle[2]/32768*180);
    printf("Mag:%d %d %d\r\n",JY901.stcMag.h[0],JY901.stcMag.h[1],JY901.stcMag.h[2]);
    printf("Pressure:%lx Height%.2f\r\n",JY901.stcPress.lPressure,(float)JY901.stcPress.lAltitude/100);
    printf("DStatus:%d %d %d %d\r\n",JY901.stcDStatus.sDStatus[0],JY901.stcDStatus.sDStatus[1],JY901.stcDStatus.sDStatus[2],JY901.stcDStatus.sDStatus[3]);
    printf("Longitude:%ldDeg%.5fm Lattitude:%ldDeg%.5fm\r\n",JY901.stcLonLat.lLon/10000000,(double)(JY901.stcLonLat.lLon % 10000000)/1e5,JY901.stcLonLat.lLat/10000000,(double)(JY901.stcLonLat.lLat % 10000000)/1e5);
    printf("GPSHeight:%.1fm GPSYaw:%.1fDeg GPSV:%.3fkm/h\r\n\r\n",(float)JY901.stcGPSV.sGPSHeight/10,(float)JY901.stcGPSV.sGPSYaw/10,(float)JY901.stcGPSV.lGPSVelocity/1000);
    """

    def __init__(self):
        imu_config = config['IMU_CONFIG']
        self.uart = UART(1, imu_config['BAUDRATE'], tx=imu_config['TX'], rx=imu_config['RX'])
        # do pre imu data receive check
        print("do imu pre check")
        self.imu_recv_check(pre=True)
        print("imu pre check done")

        self.time_year = None
        self.time_month = None
        self.time_day = None
        self.time_minute = None
        self.time_second = None
        self.time_milisecond = None

        self.acc_a0 = None
        self.acc_a1 = None
        self.acc_a2 = None
        self.acc_T = None

        self.gyro_w0 = None
        self.gyro_w1 = None
        self.gyro_w2 = None
        self.gyro_T = None

        self.angle_0 = None
        self.angle_1 = None
        self.angle_2 = None
        self.angle_T = None

        self.mag_h0 = None
        self.mag_h1 = None
        self.mag_h2 = None
        self.mag_T = None

        self.status0 = None
        self.status1 = None
        self.status2 = None
        self.status3 = None

        self.press_pressure = None
        self.press_altitude = None

        self.pos_lon = None
        self.pos_lat = None

        self.gps_height = None
        self.gps_yaw = None
        self.gps_velocity = None

    def set_angle_zero_bias(self):
        """
        set the current ange to 0 degree as a reference
        0xff 0xaa 0x01 0x08 0x00
        :return:
        """
        # unlock register
        self.uart.write(b'\xff\xaa\x69\x88\xb5')
        time.sleep(1)
        # do
        self.uart.write(b'\xff\xaa\x01\x08\x00')
        time.sleep(1)
        # lock register
        self.uart.write(b'\xff\xaa\x69\x77\xA5')

    def imu_recv_check(self, pre=False):
        """
        imu data recv check
        :param pre: is pre check
        :return:
        """
        i = 0
        while True:
            if self.uart.any() < 50:
                if pre:
                    i += 1
                    print("imu pre check retrying.%d" % i)
                    time.sleep(1)
                    continue
                else:
                    pass
            else:
                break

    def update(self):
        """
        Read from IMU and Parse data
        :return:
        """
        data = self.uart.read()
        if data:
            self.parse(data)
            # print(self.get_angles())
            # print(self.get_gyros())
            # print(self.get_acc())

    def parse(self, data):
        """
        Parse the IMU data from buffer
        :param data:
        :return:
        """
        length = len(data)
        index = 0
        data = bytes(data)
        while True:
            pos = data.find(b'\x55', index)
            if pos == -1 or length - index < 11:
                break
            # check sum
            calc_sum = 0
            for i in range(0, 10):
                calc_sum += int(data[pos + i])
            if data[pos + 10] != (calc_sum & 0xff):
                index = pos + 1
                continue

            sig = data[pos + 1]
            data_temp = data[pos + 2: pos + 10]
            if sig == 0x50:  # stcTime
                self.time_year, self.time_month, self.time_day, \
                self.time_minute, self.time_second, self.time_milisecond \
                    = ustruct.unpack("BBBBBBH", data_temp)
            elif sig == 0x51:  # stcAcc
                self.acc_a0, self.acc_a1, self.acc_a2, self.acc_T = ustruct.unpack("hhhh", data_temp)
            elif sig == 0x52:  # stcGyro
                self.gyro_w0, self.gyro_w1, self.gyro_w2, self.gyro_T = ustruct.unpack("hhhh", data_temp)
            elif sig == 0x53:  # stcAngle
                self.angle_0, self.angle_1, self.angle_2, self.angle_T = ustruct.unpack("hhhh", data_temp)
            elif sig == 0x54:  # stcMag
                self.mag_h0, self.mag_h1, self.mag_h2, self.mag_T = ustruct.unpack("hhhh", data_temp)
            elif sig == 0x55:  # stcDStatus
                self.status0, self.status1, self.status2, self.status3 = ustruct.unpack("hhhh", data_temp)
            elif sig == 0x56:  # stcPress
                self.press_pressure, self.press_altitude = ustruct.unpack("ll", data_temp)
            elif sig == 0x57:  # stcLonLat
                self.pos_lon, self.pos_lat = ustruct.unpack("LL", data_temp)
            elif sig == 0x58:  # stcGPSV
                self.gps_height, self.gps_yaw, self.gps_velocity = ustruct.unpack("ssl", data_temp)
            index = pos + 11

    def get_angles(self):
        return self.angle_0 / 32768 * 180, self.angle_1 / 32768 * 180, self.angle_2 / 32768 * 180

    def get_gyros(self):
        return self.gyro_w0 / 32768 * 2000, self.gyro_w1 / 32768 * 2000, self.gyro_w2 / 32768 * 2000

    def get_acc(self):
        return self.acc_a0 / 32768 * 16, self.acc_a1 / 32768 * 16, self.acc_a2 / 32768 * 16
