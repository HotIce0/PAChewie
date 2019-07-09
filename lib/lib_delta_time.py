import time


class PACLibDeltaTime:
    def __init__(self):
        self.last_update_at = 0
        self.update()

    def update(self):
        self.last_update_at = time.ticks_ms()

    def get_diff(self):
        """

        unit: ms
        :return:
        """
        return time.ticks_diff(time.ticks_ms(), self.last_update_at)
