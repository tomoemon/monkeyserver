# -*- coding: utf-8 -*-
import math
import time
import java
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from com.android.monkeyrunner import MonkeyRunnerExt
from com.android.ddmlib import TimeoutException


def connect():
    return AndroidDevice(MonkeyRunner.waitForConnection())


class AndroidDevice(object):
    def __init__(self, monkey_device):
        self.monkey_device = monkey_device
        self.__width = None
        self.__height = None

    @property
    def width(self):
        if not self.__width:
            self.__width = int(self.monkey_device.getProperty('display.width'))
        return self.__width

    @property
    def height(self):
        if not self.__height:
            self.__height = int(self.monkey_device.getProperty('display.height'))
        return self.__height

    def __invoke(self, func, args=()):
        # コマンド送信時に java.net.SocketException が発生する場合がある
        # スクリーンショット取得時に TimeoutException が発生する場合がある
        # スクリーンショット取得時に NullPointerException が発生する場合がある
        last_exception = None
        for i in range(3):
            try:
                return func(*args)
            except java.io.IOException, e: # old style
                last_exception = e
            except TimeoutException, e: # old style
                last_exception = e
            except java.lang.NullPointerException, e: # old style
                last_exception = e
            time.sleep(1)

        if last_exception:
            raise last_exception

    def touch(self, x, y):
        return self.__invoke(
                self.monkey_device.touch, (x, y, MonkeyDevice.DOWN_AND_UP))

    def touch_up(self, x, y):
        return self.__invoke(
                self.monkey_device.touch, (x, y, MonkeyDevice.UP))

    def touch_down(self, x, y):
        return self.__invoke(
                self.monkey_device.touch, (x, y, MonkeyDevice.DOWN))

    def touch_move(self, x, y):
        return self.__invoke(
                MonkeyRunnerExt.touchMove, (self.monkey_device, x, y))

    def swipe(self, start_pos, end_pos, duration, steps=1):
        return self.__invoke(
                self.monkey_device.drag, (start_pos, end_pos, duration, steps))

    def screen(self):
        return AndroidImage(self.__invoke(
                MonkeyRunnerExt.takeSnapshotArray, (self.monkey_device,)),
                self.width,
                self.height)

    def save_screen(self, filename, format):
        return self.__invoke(self.monkey_device.takeSnapshot, ()).writeToFile(filename, format)

    def wake(self):
        return self.__invoke(self.monkey_device.wake)


class AndroidImage(object):
    def __init__(self, image_array, width, height):
        self.image = image_array
        self.width = width
        self.height = height

    def pixel(self, x, y):
        pos = (y * self.width + x) * 4
        return tuple(self.image[pos:pos+4])


def record():
    from com.android.monkeyrunner.recorder import MonkeyRecorder
    recorder = MonkeyRecorder()
    recorder.start(MonkeyRunner.waitForConnection())


if __name__ == '__main__':
    device = connect()

