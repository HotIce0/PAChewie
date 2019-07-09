config = {
    "PROJECT_BASE_PATH": "/sd",
    "LOG_FILENAME": "log.txt",
    # The number of channel. OPTIONS:{4}
    "NUM_OF_CHANNEL": 4,
    # ESC config
    "ESC_CONFIG": {
        "PINS": [
            14, 27, 33, 32,
        ],
    },
    # IMU config
    "IMU_CONFIG": {
        "BAUDRATE": 115200,
        "TX": 12,
        "RX": 13,
    },
    # Wifi config
    "STATION_CONFIG": {
        "WIFI_SSID": "Hotice0-ip",
        "WIFI_PASSWORD": "987654321",
        "WEBSOCKET_PORT": 5174
    }
}
