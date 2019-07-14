import ujson
from config import config
from lib import lib_config_operate
import network
try:
    import usocket as socket
except ImportError:
    import socket


class PACModuleStation:
    """
    Station Module
    """
    station_protocol = {
        "SP_READ_CURRENT_PID_CONFIG_ACTION": 0,
        "SP_WRITE_CURRENT_PID_CONFIG_ACTION": 1,
        "SP_READ_FLASH_PID_CONFIG_ACTION": 2,
        "SP_WRITE_FLASH_PID_CONFIG_ACTION": 3,
        "SP_REMOTE_CONTROL_THROTTLE_ACTION": 4,
        "SP_REMOTE_CONTROL_YAW_ACTION": 5,
    }

    def __init__(self, pachewie):
        # wlan sta_if mode
        self.nic = network.WLAN(network.STA_IF)
        # socket
        self.listen_s = None
        self.client_s = None
        self.pachewie = pachewie

        # connect to wifi
        self.connect_to_wifi()
        # # start server
        # self.start_server()

    def connect_to_wifi(self):
        station_config = config['STATION_CONFIG']
        if not self.nic.active():  # check wlan is active
            self.nic.active(True)  # active wlan
        # connect to the wifi that station connected to.
        self.nic.connect(station_config['WIFI_SSID'], station_config['WIFI_PASSWORD'])
        # check connect success
        while not self.nic.isconnected():
            pass

    def start_server(self):
        station_config = config['STATION_CONFIG']
        ai = socket.getaddrinfo("0.0.0.0", station_config['WEBSOCKET_PORT'])
        addr = ai[0][4]
        self.listen_s = socket.socket()
        self.listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_s.bind(addr)
        self.listen_s.listen(1)
        for i in (network.AP_IF, network.STA_IF):
            iface = network.WLAN(i)
            if iface.active():
                print("PAChewieStation started on %s:%d" % (iface.ifconfig()[0], station_config['WEBSOCKET_PORT']))

        self.__accept_conn()

    def stop_server(self):
        """
        stop server and close connection
        :return:
        """
        if self.client_s:
            self.client_s.close()
            self.client_s = None
        if self.listen_s:
            self.listen_s.close()
            self.listen_s = None

    def __accept_conn(self):
        """
        accept connection loop
        :return:
        """
        while True:
            cl, remote_addr = self.listen_s.accept()
            # close prev client
            if self.client_s:
                self.client_s.close()
            self.client_s = cl
            cl.setblocking(False)

            print("PACHewieStation connection from:", remote_addr)
            while True:
                data = cl.readline()
                if isinstance(data, bytes):
                    if len(data) == 0:
                        break
                    data = data.decode('utf-8')
                    print("recv from station: " + data)
                    self.parse_protocol(data)
            cl.close()

    def parse_protocol(self, data):
        """
        parse the data from station
        :param data:
        :return:
        """
        data_obj = ujson.loads(data)
        action = data_obj['action']
        param = data_obj['param']
        if action == PACModuleStation.station_protocol['SP_READ_CURRENT_PID_CONFIG_ACTION']:
            # Read PID Config
            module_control = self.pachewie.module_control
            pids = {
                "ANGLE_ROLL": module_control.angle_roll_pid.get_param(),
                "ANGLE_PITCH": module_control.angle_pitch_pid.get_param(),
                "ANGLE_YAW": module_control.angle_yaw_pid.get_param(),
                "GYROS_ROLL": module_control.gyros_roll_pid.get_param(),
                "GYROS_PITCH": module_control.gyros_pitch_pid.get_param(),
                "GYROS_YAW": module_control.gyros_yaw_pid.get_param(),
            }
            response_obj = {
                "code": 0,
                "action": action,
                "data": pids
            }
            response = ujson.dumps(response_obj) + "\n"
            self.client_s.write(response)
        elif action == PACModuleStation.station_protocol['SP_WRITE_CURRENT_PID_CONFIG_ACTION']:
            module_control = self.pachewie.module_control
            angle_roll = param['ANGLE_ROLL']
            angle_pitch = param['ANGLE_PITCH']
            angle_yaw = param['ANGLE_YAW']
            gyros_roll = param['GYROS_ROLL']
            gyros_pitch = param['GYROS_PITCH']
            gyros_yaw = param['GYROS_YAW']
            # Write current PID config
            module_control.angle_roll_pid.update_pid_settings(
                angle_roll[0], angle_roll[1], angle_roll[2], angle_roll[3], angle_roll[4]
            )
            module_control.angle_pitch_pid.update_pid_settings(
                angle_pitch[0], angle_pitch[1], angle_pitch[2], angle_pitch[3], angle_pitch[4]
            )
            module_control.angle_yaw_pid.update_pid_settings(
                angle_yaw[0], angle_yaw[1], angle_yaw[2], angle_yaw[3], angle_yaw[4]
            )
            module_control.gyros_roll_pid.update_pid_settings(
                gyros_roll[0], gyros_roll[1], gyros_roll[2], gyros_roll[3], gyros_roll[4]
            )
            module_control.gyros_pitch_pid.update_pid_settings(
                gyros_pitch[0], gyros_pitch[1], gyros_pitch[2], gyros_pitch[3], gyros_pitch[4]
            )
            module_control.gyros_yaw_pid.update_pid_settings(
                gyros_yaw[0], gyros_yaw[1], gyros_yaw[2], gyros_yaw[3], gyros_yaw[4]
            )
            response_obj = {
                "code": 0,
                "action": action,
                "data": "write current pid config success"
            }
            response = ujson.dumps(response_obj) + "\n"
            self.client_s.write(response)
        elif action == PACModuleStation.station_protocol['SP_READ_FLASH_PID_CONFIG_ACTION']:
            pids = lib_config_operate.read_config_json_obj('pid.json')
            response_obj = {
                "code": 0,
                "action": action,
                "data": pids
            }
            response = ujson.dumps(response_obj) + "\n"
            self.client_s.write(response)
        elif action == PACModuleStation.station_protocol['SP_WRITE_FLASH_PID_CONFIG_ACTION']:
            pids = param
            lib_config_operate.write_config_json_obj('pid.json', pids)
            response_obj = {
                "code": 0,
                "action": action,
                "data": "write pid config in FLASH success"
            }
            response = ujson.dumps(response_obj) + "\n"
            self.client_s.write(response)
        elif action == PACModuleStation.station_protocol['SP_REMOTE_CONTROL_THROTTLE_ACTION']:
            throttle_value = param
            print("油门值: " + str(throttle_value))
            self.pachewie.module_control.set_throttle(int(throttle_value))
        elif action == PACModuleStation.station_protocol['SP_REMOTE_CONTROL_YAW_ACTION']:
            yaw = param
            self.pachewie.module_control.set_yaw(int(yaw))









    # def start_websocket_server(self):
    #     self.stop_websocekt_server()
    #
    #     station_config = config['STATION_CONFIG']
    #     self.listen_s = socket.socket()
    #     # create websocket server
    #     self.listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     ai = socket.getaddrinfo("0.0.0.0", station_config['WEBSOCKET_PORT'])
    #     addr = ai[0][4]
    #     self.listen_s.bind(addr)
    #     self.listen_s.listen(1)
    #     for i in (network.AP_IF, network.STA_IF):
    #         iface = network.WLAN(i)
    #         if iface.active():
    #             print("PAChewieStation started on ws://%s:%d" % (iface.ifconfig()[0], station_config['WEBSOCKET_PORT']))
    #
    # def stop_websocekt_server(self):
    #     """
    #     stop websocket server and close connection
    #     :return:
    #     """
    #     if self.listen_s:
    #         self.listen_s.close()
    #         self.listen_s = None
    #     if self.client_s:
    #         self.client_s.close()
    #         self.client_s = None
    #
    # def accept_conn(self):
    #     """
    #     accpet websocket connnection of client and create websocket io buffer
    #     blocking
    #     :return:
    #     """
    #     cl, remote_addr = self.listen_s.accept()
    #     # close prev client
    #     if self.client_s:
    #         self.client_s.close()
    #     self.client_s = cl
    #     cl.setblocking(False)
    #     print("PACHewieStation connection from:", remote_addr)
    #     try:
    #         lib_websocket.server_handshake(cl)
    #         self.ws_io = uwebsocket.websocket(cl, True)
    #     except OSError:
    #         self.accept_conn()
    #
    # def read(self, *args):
    #     self.ws_io.read(*args)
    #
    # def readline(self):
    #     self.ws_io.readline()
    #
    # def write(self, data):
    #     self.ws_io.write(data)
