from config import config


class PACModuleLog:
    def __init__(self):
        self.filename = config['LOG_FILENAME']
        self.time = lambda: "2019-11-18 10:20:10"  # wait update

    def _write_msg(self, sign, msg):
        with open(self.filename, 'a') as f:
            f.write(sign + " : " + self.time() + " " + msg + "\n")

    def info(self, msg):
        self._write_msg("info", msg)

    def error(self, msg):
        self._write_msg("error", msg)
