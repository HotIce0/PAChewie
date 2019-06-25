import time


def retry(retry_time, function, delay=0, pre_delay=0, **kwargs):
    count = 0
    time.sleep(pre_delay)
    while count < retry_time:
        try:
            res = function(kwargs)
            time.sleep(delay)
            return res
        except Exception as e:
            count += 1
            if not count < retry_time:
                raise e
