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
        "BAUDRATE": 921600,
        "TX": 12,
        "RX": 13,
    },
    # Wifi config
    "STATION_CONFIG": {
        "WIFI_SSID": "5214",
        "WIFI_PASSWORD": "52145214A",
        "WEBSOCKET_PORT": 5174
    }
}
