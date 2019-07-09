import network


class PACModuleWifi:
    def __init__(self):
        self.ap_if = network.WLAN(network.AP_IF)
        if not self.ap_if.active():  # 检查是否开启
            self.ap_if.active(True)  # 开启网络
