import time
import datetime


class CalTime(object):
    """docstring for ClassName"""
    sta_time = datetime.datetime
    end_time = datetime.datetime
    used_time = datetime.datetime

    def __init__(self):
        pass

    def start(self):
        self.sta_time = time.time()
        return self.sta_time

    def end(self):
        self.end_time = time.time()
        return self.end_time

    def last_time(self):
        self.used_time = self.end_time - self.sta_time
        return self.used_time


def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def time_format(t_str):
    num = int(t_str)
    return num if t_str >= 10 else "0%s" % num


def time_transfer(time_stamp):
    if time_stamp < 24 * 3600:
        pass
    hour = time_stamp // 3600
    minute = time_stamp % 60 // 60
    second = time_stamp % 60
    return "%s:%s:%s" % (time_format(hour), time_format(minute), time_format(second))


if __name__ == '__main__':
    # ct = CalTime()
    # print(ct.start())
    # for i in range(1, 2):
    #     time.sleep(1)
    #     print(i)
    # print(ct.end())
    #
    # print(ct.last_time())
    pass
