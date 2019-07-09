"""
This library is used to operate the config file with json format (/config_json/*.json).
"""

from config import config
import ujson


def read_config_json_obj(filename):
    path = config['PROJECT_BASE_PATH'] + "/config_json/" + filename
    with open(path, 'r') as f:
        pid_config = ujson.loads(f.read())
        return pid_config


def write_config_json_obj(filename, config_json_obj):
    path = config['PROJECT_BASE_PATH'] + "/config_json/" + filename
    with open(path, 'w') as f:
        f.write(ujson.dumps(config_json_obj))
