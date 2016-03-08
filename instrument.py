#!/usr/bin/env python

from __future__ import division
import RPi.GPIO as gpio
from capsense import CapRead as cap_read


SENSOR_PIN = 17
OUT_PIN = 18


class TouchInstrument(object):
    def __init__(self):
        self.smooth_factor = 500

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

    def get_sound_level(self):
        ''' Returns an integer value for sound level '''
        total = 0
        for i in range(0, self.smooth_factor):
            total += cap_read(sensor_pin=SENSOR_PIN, out_pin=OUT_PIN)
        return max(total-4*self.smooth_factor, 0) // self.smooth_factor

    def run(self):
        while True:
            print "."*self.get_sound_level()


if __name__ == "__main__":
    ti = TouchInstrument()
    ti.run()

