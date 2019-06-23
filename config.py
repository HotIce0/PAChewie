config = {
    # The number of channel. OPTIONS:{4}
    "NUM_OF_CHANNEL": 4,
    # Pin config
    "PIN_CONFIGS": {
        "ESC_PINS": [    # 0: rt, 1: lb, 2: lt, 3: rb
            4, 5, 12, 13
        ],
        "IMU_PIN": {
            "TX": 12,
            "RX": 13
        }
        # {
        #     "left_top_0": 4,
        #     "right_top_1": 5,
        #     "left_bottom_2": 12,
        #     "right_bottom_3": 13,
        # }
    }
}
