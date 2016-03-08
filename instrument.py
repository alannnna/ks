#!/usr/bin/env python

from __future__ import division
import RPi.GPIO as gpio
from capsense import CapRead as cap_read


if __name__ == "__main__":
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    SMOOTH_FACTOR = 500

    while True:
        total = 0
        for j in range(0,SMOOTH_FACTOR):
            val = cap_read(17, 18)
            total += val
        print "."*(max(total-4*SMOOTH_FACTOR, 0)//SMOOTH_FACTOR)

    # clean before you leave
    gpio.cleanup()
