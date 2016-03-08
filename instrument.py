#!/usr/bin/env python

from __future__ import division
import RPi.GPIO as gpio
import pygame
from pygame.mixer import pre_init
from time import sleep

from capsense import CapRead as cap_read
from note import Note


SENSOR_PIN = 17
OUT_PIN = 18


class TouchInstrument(object):
    def __init__(self):
        self.smooth_factor = 500
        self.max_notes = 16
        self.notes = []
        self.last_level = 0

    def get_sound_level(self):
        ''' Returns an integer value for sound level '''
        total = 0
        for i in range(0, self.smooth_factor):
            total += cap_read(sensor_pin=SENSOR_PIN, out_pin=OUT_PIN)
        return max(total-4*self.smooth_factor, 0) // self.smooth_factor

    def add_note(self, freq):
        print "adding note"
        # TODO self-determine frequency based on preexisting notes??

        if len(self.notes) == self.max_notes:
            return
        n = Note(freq, volume=.01).play(-1)
        self.notes.append(n)

    def remove_note(self):
        print "removing note"

        try:
            n = self.notes.pop()
        except IndexError:
            return
        n.stop()

    def set_sound(self, level):
        if level > self.last_level:
            for i in range(level - self.last_level):
                self.add_note(440)
        else:
            for i in range(self.last_level - level):
                self.remove_note()

    def run(self):
        print "Starting TouchInstrument..."

        # rpi gpio setup
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        print "RPi GPIO initialized."

        # Sound setup (pygame)
        pre_init(44100, -16, 1, 1024)
        pygame.init()
        pygame.mixer.set_num_channels(self.max_notes)
        print "Sound initialized."
        print "TouchInstrument is ready."

        while True:
            level = self.get_sound_level()
            self.set_sound(level)
            self.last_level = level


if __name__ == "__main__":
    ti = TouchInstrument()
    ti.run()

