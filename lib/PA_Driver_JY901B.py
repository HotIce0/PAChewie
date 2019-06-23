# import ustruct
import struct

class PA_Driver_JY901B:
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

    def parse(self, data):
        """
        parse the IMU data from buffer
        :param data:
        :return:
        """
        length = len(data)
        index = 0
        while True:
            pos = data.find(0x55, index)
            if pos == -1 or length - index < 11:
                break
            sig = data[pos + 1]
            if sig == 0x50:  # stcTime
                self.time_year, self.time_month, self.time_day, \
                self.time_minute, self.time_second, self.time_milisecond \
                    = struct.unpack_from("BBBBBBH", data, pos + 2)
            elif sig == 0x51:  # stcAcc
                self.acc_a0, self.acc_a1, self.acc_a2, self.acc_T = struct.unpack_from("hhhh", data, pos + 2)
            elif sig == 0x52:  # stcGyro
                self.gyro_w0, self.gyro_w1, self.gyro_w2, self.gyro_T = struct.unpack_from("hhhh", data, pos + 2)
            elif sig == 0x53:  # stcAngle
                self.angle_0, self.angle_1, self.angle_2, self.angle_T = struct.unpack_from("hhhh", data, pos + 2)
            elif sig == 0x54:  # stcMag
                self.mag_h0, self.mag_h1, self.mag_h2, self.mag_T = struct.unpack_from("hhhh", data, pos + 2)
            elif sig == 0x55:  # stcDStatus
                self.status0, self.status1, self.status2, self.status3 = struct.unpack_from("hhhh", data, pos + 2)
            elif sig == 0x56:  # stcPress
                self.press_pressure, self.press_altitude = struct.unpack_from("ll", data, pos + 2)
            elif sig == 0x57:  # stcLonLat
                self.pos_lon, self.pos_lat = struct.unpack_from("LL", data, pos + 2)
            elif sig == 0x58:  # stcGPSV
                self.gps_height, self.gps_yaw, self.gps_velocity = struct.unpack_from("ssl", data, pos + 2)
            index = pos + 11

# Test Code
# str_temp = ""
# buf = b'UQ\xdf\x00S\x00\x0f\x08\x1f\x0f\x1dUR\x00\x00\x00\x00\x00\x00\x1f\x0f\xd5US\xa0\x01\xa0\xfb\xf0\x00\r)\nUT\xe7\xffy\x00\xfb\xfe\x1f\x0f/UQ\xde\x00T\x00\x10\x08\x1f\x0f\x1eUR\x00\x00\x00\x00\x00\x00\x1f\x0f\xd5US\xa0\x01\xa0\xfb\xf5\x00\r)\x0fUT\xe8\xff}\x00\xfc\xfe\x1f\x0f5UQ\xe0\x00S\x00\x11\x08%\x0f&UR\x00\x00\x00\x00\x00\x00%\x0f\xdbUS\xa0\x01\xa0\xfb\xee\x00\r)\x08UT\xe7\xffy\x00\xfd\xfe%\x0f7UQ\xe0\x00R\x00\x11\x08&\x0f&UR\x00\x00\x00\x00\x00\x00&\x0f\xdcUS\xa0\x01\xa0\xfb\xe4\x00\r)\xfeUT\xe7\xffy\x00\xfd\xfe&\x0f8UQ\xe0\x00R\x00\x11\x08&\x0f&UR\x00\x00\x00\x00\x00\x00&\x0f\xdcUS\xa0\x01\xa0\xfb\xde\x00\r)\xf8UT\xea\xffz\x00\x00\xff&\x0f@UQ\xe1\x00R\x00\x11\x08&\x0f\'UR\x00\x00\x00\x00\x00\x00&\x0f\xdcUS\xa0\x01\x9f\xfb\xe0\x00\r)\xf9UT\xe6\xff|\x00\xfd\xfe&\x0f:'
# for c in buf:
#     str_temp += (str(hex(c)) + " ")
# print(str_temp)
#
# jy901b = PA_Driver_JY901B()
# jy901b.parse(buf)
# print(jy901b.__dict__)
#
# # 0xa5 0xf9 0x7c 0xfc 0x63 0x1 0x8f 0xf
#
# sao = bytes([0xa4, 0xf9])
# print(sao)
# print(struct.unpack_from("h", sao))
# print(-1628 / 32768 * 16)
