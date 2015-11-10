# -*- coding: utf-8 -*-
import time
from android_device import connect
from interpolate import interpolate


__EVENT_REGISTERING_TIME = 0.03


class DeviceInitializer(object):
    __device = None

    @classmethod
    def device(cls):
        if not cls.__device:
            cls.__device = connect()
        return cls.__device


def touch(x, y):
    """ タッチする（押して離す）
      touch(x, y) == [touch_down(x, y), touch_up(x, y)]
    """
    device = DeviceInitializer.device()
    device.touch(x, y)
    time.sleep(__EVENT_REGISTERING_TIME)


def touch_up(x, y):
    """ タッチを離す """
    device = DeviceInitializer.device()
    device.touch_up(x, y)
    time.sleep(__EVENT_REGISTERING_TIME)


def touch_down(x, y):
    """ タッチする（離さない） """
    device = DeviceInitializer.device()
    device.touch_down(x, y)
    time.sleep(__EVENT_REGISTERING_TIME)


def touch_move(start, end, duration, step):
    """ タッチした状態で移動する """
    device = DeviceInitializer.device()
    positions = interpolate(start, end, step)
    sleep_per_move = max(
            float(duration) / step, __EVENT_REGISTERING_TIME)

    for pos in positions[1:]:
        device.touch_move(*pos)
        time.sleep(sleep_per_move)


def swipe(start, end, duration, step):
    """ スワイプする """
    device = DeviceInitializer.device()
    device.swipe(start, end, duration, step)
    time.sleep(__EVENT_REGISTERING_TIME)

