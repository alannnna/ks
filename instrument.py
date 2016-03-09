#!/usr/bin/env python

from __future__ import division
from time import sleep
import atexit
import RPi.GPIO as gpio
import pygame
from pygame.mixer import pre_init

from capsense import CapRead as cap_read
from note import Note
from chord_progression import get_next_chord, get_next_note


SENSOR_PINS = [17, 21]
OUT_PIN = 18


class TouchInstrument(object):
    def __init__(self):
        self.smooth_factor = 500
        self.calibrate_amount = 30
        self.max_notes = 16
        self.notes = []
        self.last_level = 0
        self.chord = 1
        self.key = 69  # Midi value for A4; key of A
        self.calibration_factors = [0] * len(SENSOR_PINS)

    def get_sound_level(self, return_totals=False):
        '''
        Returns an integer value for sound level, to be translated to
        chord complexity or something.
        '''
        totals = [0]*len(SENSOR_PINS)
        levels = [0]*len(SENSOR_PINS)
        for i in range(0, self.smooth_factor):
            for i, sensor_pin in enumerate(SENSOR_PINS):
                totals[i] += cap_read(sensor_pin=sensor_pin, out_pin=OUT_PIN)

        if return_totals:
            return totals

        for i in range(len(SENSOR_PINS)):
            levels[i] = max(totals[i] - self.calibration_factors[i] * self.smooth_factor, 0) // self.smooth_factor
        return sum(levels)

    def add_note(self):
        print "adding note"

        if len(self.notes) == self.max_notes:
            return
        notes = [note.midi for note in self.notes]
        next_note = get_next_note(notes, self.chord, key=self.key)
        n = Note(next_note, volume=.05)
        n.play(-1, fade_ms=500)
        self.notes.append(n)

    def remove_note(self):
        print "removing note"

        try:
            n = self.notes.pop()
        except IndexError:
            return
        n.stop()
        if len(self.notes) == 0:
            self.chord = get_next_chord(self.chord)

    def set_sound(self, level):
        if level > self.last_level:
            for i in range(level - self.last_level):
                self.add_note()
        else:
            for i in range(self.last_level - level):
                self.remove_note()
        self.last_level = level

    def run(self):
        print "Starting TouchInstrument..."

        # rpi gpio setup
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)  # TODO try without this line
        print "RPi GPIO initialized."

        # Sound setup (pygame)
        pre_init(44100, -16, 1, 1024)
        pygame.init()
        pygame.mixer.set_num_channels(self.max_notes)
        print "Sound initialized."

        # Calibrate; find what should be sound level zero and give a self.smooth_factor/2 buffer
        print "Calibrating..."
        totals = [0] * len(SENSOR_PINS)
        # Get the average of several reads
        for i in range(self.calibrate_amount):
            new_totals = self.get_sound_level(return_totals=True)
            for i in range(len(totals)):
                totals[i] += new_totals[i]
        totals = [total / self.calibrate_amount for total in totals]
        # Set calibration factors based on smooth factor
        for i, total in enumerate(totals):
            self.calibration_factors[i] = int((total + self.smooth_factor / 2) // self.smooth_factor)
        print self.calibration_factors
        print "Calibrated."

        print "TouchInstrument is ready."

        try:
            while True:
                level = self.get_sound_level()
                self.set_sound(level)
        except KeyboardInterrupt:
            print "Cleaning up."
            gpio.cleanup()
            pygame.quit()
            return

    def test_run(self):
        print "Starting TouchInstrument test..."

        # Sound setup (pygame)
        pre_init(44100, -16, 1, 1024)
        pygame.init()
        pygame.mixer.set_num_channels(self.max_notes)
        print "Sound initialized."

        levels = [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 3, 4, 5, 4, 2, 1, 0, 0, 3, 6, 5, 4, 3, 1, 0, 2, 1, 0, 20, 25, 30, 0]
        counter = 0
        try:
            while True:
                self.set_sound(levels[counter])
                counter += 1
                if counter == len(levels):
                    counter = 0
                sleep(0.5)
        except KeyboardInterrupt:
            print "Cleaning up."
            pygame.quit()
            return


if __name__ == "__main__":
    ti = TouchInstrument()
    ti.run()
    # ti.test_run()
